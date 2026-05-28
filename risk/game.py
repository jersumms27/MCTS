from enum import Enum
from typing import Any
from dataclasses import dataclass
from collections import deque
from itertools import combinations
import random
from mcts.state import State
from copy import deepcopy

class Color(Enum):
    BLACK = 'black'
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    PURPLE = 'purple'
    YELLOW = 'yellow'


class Territory(Enum):
    AFGHANISTAN = 'Afghanistan'
    ALASKA = 'Alaska'
    ALBERTA = 'Alberta'
    ARGENTINA = 'Argentina'
    BRAZIL = 'Brazil'
    CENTRAL_AMERICA = 'Central America'
    CHINA = 'China'
    CONGO = 'Congo'
    EAST_AFRICA = 'East Africa'
    EASTERN_AUSTRALIA = 'Eastern Australia'
    EASTERN_UNITED_STATES = 'Eastern United States'
    EGYPT = 'Egypt'
    GREAT_BRITAIN = 'Great Britain'
    GREENLAND = 'Greenland'
    ICELAND = 'Iceland'
    INDIA = 'India'
    INDONESIA = 'Indonesia'
    IRKUTSK = 'Irkutsk'
    JAPAN = 'Japan'
    KAMCHATKA = 'Kamchatka'
    MADAGASCAR = 'Madagascar'
    MIDDLE_EAST = 'Middle East'
    MONGOLIA = 'Mongolia'
    NEW_GUINEA = 'New Guinea'
    NORTH_AFRICA = 'North Africa'
    NORTHERN_EUROPE = 'Northern Europe'
    NORTHWEST_TERRITORY = 'Northwest Territory'
    ONTARIO = 'Ontario'
    PERU = 'Peru'
    QUEBEC = 'Quebec'
    SCANDINAVIA = 'Scandinavia'
    SIAM = 'Siam'
    SIBERIA = 'Siberia'
    SOUTH_AFRICA = 'South Africa'
    SOUTHERN_EUROPE = 'Southern Europe'
    UKRAINE = 'Ukraine'
    URAL = 'Ural'
    VENEZUELA = 'Venezuela'
    WESTERN_AUSTRALIA = 'Western Australia'
    WESTERN_EUROPE = 'Western Europe'
    WESTERN_UNITED_STATES = 'Western United States'
    YAKUTSK = 'Yakutsk'


class Continent(Enum):
    NORTH_AMERICA = ('North America', 5, frozenset({
        Territory.ALASKA, Territory.ALBERTA, Territory.CENTRAL_AMERICA,
        Territory.EASTERN_UNITED_STATES, Territory.GREENLAND, Territory.NORTHWEST_TERRITORY,
        Territory.ONTARIO, Territory.QUEBEC, Territory.WESTERN_UNITED_STATES,
    }))
    SOUTH_AMERICA = ('South America', 2, frozenset({
        Territory.ARGENTINA, Territory.BRAZIL, Territory.PERU, Territory.VENEZUELA,
    }))
    EUROPE = ('Europe', 5, frozenset({
        Territory.GREAT_BRITAIN, Territory.ICELAND, Territory.NORTHERN_EUROPE,
        Territory.SCANDINAVIA, Territory.SOUTHERN_EUROPE, Territory.UKRAINE,
        Territory.WESTERN_EUROPE,
    }))
    AFRICA = ('Africa', 3, frozenset({
        Territory.CONGO, Territory.EAST_AFRICA, Territory.EGYPT,
        Territory.MADAGASCAR, Territory.NORTH_AFRICA, Territory.SOUTH_AFRICA,
    }))
    ASIA = ('Asia', 7, frozenset({
        Territory.AFGHANISTAN, Territory.CHINA, Territory.INDIA,
        Territory.IRKUTSK, Territory.JAPAN, Territory.KAMCHATKA,
        Territory.MIDDLE_EAST, Territory.MONGOLIA, Territory.SIAM,
        Territory.SIBERIA, Territory.URAL, Territory.YAKUTSK,
    }))
    AUSTRALIA = ('Australia', 2, frozenset({
        Territory.EASTERN_AUSTRALIA, Territory.INDONESIA,
        Territory.NEW_GUINEA, Territory.WESTERN_AUSTRALIA,
    }))

    @property
    def full_name(self) -> str:
        return self.value[0]

    @property
    def bonus(self) -> int:
        return self.value[1]

    @property
    def territories(self) -> frozenset[Territory]:
        return self.value[2]


class CardType(Enum):
    INFANTRY = 'Infantry'
    CAVALRY = 'Cavalry'
    ARTILLERY = 'Artillery'
    WILD = 'Wild'


class Card:
    def __init__(self, card_type: CardType, territory: Territory | None = None) -> None:
        self.card_type: CardType = card_type
        self.territory: Territory | None = territory


class Player:
    def __init__(self, name: str, color: Color) -> None:
        self.name: str = name
        self.color: Color = color

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Player):
            return self.name == other.name and self.color == other.color
        return False

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(frozen=True)
class TerritoryState:
    player: Player | None
    num_troops: int


class RiskBoard:
    adj_list: dict[Territory, frozenset[Territory]] = {
            Territory.AFGHANISTAN: frozenset((Territory.CHINA, Territory.INDIA, Territory.MIDDLE_EAST, Territory.UKRAINE, Territory.URAL)),
            Territory.ALASKA: frozenset((Territory.ALBERTA, Territory.KAMCHATKA, Territory.NORTHWEST_TERRITORY)),
            Territory.ALBERTA: frozenset((Territory.ALASKA, Territory.NORTHWEST_TERRITORY, Territory.ONTARIO, Territory.WESTERN_UNITED_STATES)),
            Territory.ARGENTINA: frozenset((Territory.BRAZIL, Territory.PERU)),
            Territory.BRAZIL: frozenset((Territory.ARGENTINA, Territory.NORTH_AFRICA, Territory.PERU, Territory.VENEZUELA)),
            Territory.CENTRAL_AMERICA: frozenset((Territory.EASTERN_UNITED_STATES, Territory.VENEZUELA, Territory.WESTERN_UNITED_STATES)),
            Territory.CHINA: frozenset((Territory.AFGHANISTAN, Territory.INDIA, Territory.MONGOLIA, Territory.SIAM, Territory.SIBERIA, Territory.URAL)),
            Territory.CONGO: frozenset((Territory.EAST_AFRICA, Territory.NORTH_AFRICA, Territory.SOUTH_AFRICA)),
            Territory.EAST_AFRICA: frozenset((Territory.CONGO, Territory.EGYPT, Territory.MADAGASCAR, Territory.MIDDLE_EAST, Territory.NORTH_AFRICA, Territory.SOUTH_AFRICA)),
            Territory.EASTERN_AUSTRALIA: frozenset((Territory.NEW_GUINEA, Territory.WESTERN_AUSTRALIA)),
            Territory.EASTERN_UNITED_STATES: frozenset((Territory.CENTRAL_AMERICA, Territory.ONTARIO, Territory.QUEBEC, Territory.WESTERN_UNITED_STATES)),
            Territory.EGYPT: frozenset((Territory.EAST_AFRICA, Territory.MIDDLE_EAST, Territory.NORTH_AFRICA, Territory.SOUTHERN_EUROPE)),
            Territory.GREAT_BRITAIN: frozenset((Territory.ICELAND, Territory.NORTHERN_EUROPE, Territory.SCANDINAVIA, Territory.WESTERN_EUROPE)),
            Territory.GREENLAND: frozenset((Territory.ICELAND, Territory.NORTHWEST_TERRITORY, Territory.QUEBEC)),
            Territory.ICELAND: frozenset((Territory.GREAT_BRITAIN, Territory.GREENLAND, Territory.SCANDINAVIA)),
            Territory.INDIA: frozenset((Territory.AFGHANISTAN, Territory.CHINA, Territory.MIDDLE_EAST, Territory.SIAM)),
            Territory.INDONESIA: frozenset((Territory.NEW_GUINEA, Territory.SIAM, Territory.WESTERN_AUSTRALIA)),
            Territory.IRKUTSK: frozenset((Territory.KAMCHATKA, Territory.MONGOLIA, Territory.SIBERIA, Territory.YAKUTSK)),
            Territory.JAPAN: frozenset((Territory.KAMCHATKA, Territory.MONGOLIA)),
            Territory.KAMCHATKA: frozenset((Territory.ALASKA, Territory.IRKUTSK, Territory.JAPAN, Territory.MONGOLIA, Territory.YAKUTSK)),
            Territory.MADAGASCAR: frozenset((Territory.EAST_AFRICA, Territory.SOUTH_AFRICA)),
            Territory.MIDDLE_EAST: frozenset((Territory.AFGHANISTAN, Territory.EAST_AFRICA, Territory.EGYPT, Territory.INDIA, Territory.SOUTHERN_EUROPE, Territory.UKRAINE)),
            Territory.MONGOLIA: frozenset((Territory.CHINA, Territory.IRKUTSK, Territory.JAPAN, Territory.KAMCHATKA, Territory.SIBERIA)),
            Territory.NEW_GUINEA: frozenset((Territory.EASTERN_AUSTRALIA, Territory.INDONESIA, Territory.WESTERN_AUSTRALIA)),
            Territory.NORTH_AFRICA: frozenset((Territory.BRAZIL, Territory.CONGO, Territory.EAST_AFRICA, Territory.EGYPT, Territory.SOUTHERN_EUROPE, Territory.WESTERN_EUROPE)),
            Territory.NORTHERN_EUROPE: frozenset((Territory.GREAT_BRITAIN, Territory.SCANDINAVIA, Territory.SOUTHERN_EUROPE, Territory.UKRAINE, Territory.WESTERN_EUROPE)),
            Territory.NORTHWEST_TERRITORY: frozenset((Territory.ALASKA, Territory.ALBERTA, Territory.GREENLAND, Territory.ONTARIO)),
            Territory.ONTARIO: frozenset((Territory.ALBERTA, Territory.EASTERN_UNITED_STATES, Territory.GREENLAND, Territory.NORTHWEST_TERRITORY, Territory.QUEBEC, Territory.WESTERN_UNITED_STATES)),
            Territory.PERU: frozenset((Territory.ARGENTINA, Territory.BRAZIL, Territory.VENEZUELA)),
            Territory.QUEBEC: frozenset((Territory.EASTERN_UNITED_STATES, Territory.GREENLAND, Territory.ONTARIO)),
            Territory.SCANDINAVIA: frozenset((Territory.GREAT_BRITAIN, Territory.ICELAND, Territory.NORTHERN_EUROPE, Territory.UKRAINE)),
            Territory.SIAM: frozenset((Territory.CHINA, Territory.INDIA, Territory.INDONESIA)),
            Territory.SIBERIA: frozenset((Territory.CHINA, Territory.IRKUTSK, Territory.MONGOLIA, Territory.URAL, Territory.YAKUTSK)),
            Territory.SOUTH_AFRICA: frozenset((Territory.CONGO, Territory.EAST_AFRICA, Territory.MADAGASCAR)),
            Territory.SOUTHERN_EUROPE: frozenset((Territory.EGYPT, Territory.MIDDLE_EAST, Territory.NORTH_AFRICA, Territory.NORTHERN_EUROPE, Territory.UKRAINE, Territory.WESTERN_EUROPE)),
            Territory.UKRAINE: frozenset((Territory.AFGHANISTAN, Territory.MIDDLE_EAST, Territory.NORTHERN_EUROPE, Territory.SCANDINAVIA, Territory.SOUTHERN_EUROPE, Territory.URAL)),
            Territory.URAL: frozenset((Territory.AFGHANISTAN, Territory.CHINA, Territory.SIBERIA, Territory.UKRAINE)),
            Territory.VENEZUELA: frozenset((Territory.BRAZIL, Territory.CENTRAL_AMERICA, Territory.PERU)),
            Territory.WESTERN_AUSTRALIA: frozenset((Territory.EASTERN_AUSTRALIA, Territory.INDONESIA, Territory.NEW_GUINEA)),
            Territory.WESTERN_EUROPE: frozenset((Territory.GREAT_BRITAIN, Territory.NORTH_AFRICA, Territory.NORTHERN_EUROPE, Territory.SOUTHERN_EUROPE)),
            Territory.WESTERN_UNITED_STATES: frozenset((Territory.ALBERTA, Territory.CENTRAL_AMERICA, Territory.EASTERN_UNITED_STATES, Territory.ONTARIO)),
            Territory.YAKUTSK: frozenset((Territory.IRKUTSK, Territory.KAMCHATKA, Territory.SIBERIA)),
        }

    def __init__(self) -> None:
        self.reset_board()
        self.card_bonus: int = 4
        self.deck: list[Card] = self._build_deck()
        self.hands: dict[Player, list[Card]] = {}

    def update_board(self, territory: Territory, new_player: Player | None = None, new_troops: int = 0) -> None:
        self.map[territory] = TerritoryState(new_player, new_troops)

    def place_one_troop(self, territory: Territory, player: Player) -> None:
        state: TerritoryState = self.map[territory]
        if state.player == player:
            self.map[territory] = TerritoryState(state.player, state.num_troops + 1)
    
    def transfer_troops(self, source: Territory, dest: Territory, player: Player, num_troops: int = 1) -> None:
        source_state: TerritoryState = self.map[source]
        dest_state: TerritoryState = self.map[dest]

        if source_state.player == player == dest_state.player and source_state.num_troops - num_troops > 0:
            self.map[source] = TerritoryState(player, source_state.num_troops - num_troops)
            self.map[dest] = TerritoryState(player, dest_state.num_troops + num_troops)

    def reset_board(self) -> None:
        self.map: dict[Territory, TerritoryState] = {t: TerritoryState(None, 0) for t in Territory}

    def _build_deck(self) -> list[Card]:
        deck: list[Card] = [Card(CardType.WILD)] * 2
        types: list[CardType] = [CardType.INFANTRY, CardType.CAVALRY, CardType.ARTILLERY]
        for i, territory in enumerate(Territory):
            deck.append(Card(types[i % 3], territory))
        random.shuffle(deck)
        return deck

    def init_player(self, player: Player) -> None:
        self.hands[player] = []

    def draw_card(self, player: Player) -> None:
        if self.deck:
            self.hands[player].append(self.deck.pop())

    def get_valid_trade_sets(self, player: Player) -> list[tuple[Card, Card, Card]]:
        hand: list[Card] = self.hands.get(player, [])
        return [combo for combo in combinations(hand, 3) if self._is_valid_set(combo)]

    def trade_cards(self, player: Player, cards: tuple[Card, Card, Card]) -> int:
        hand: list[Card] = self.hands[player]
        for card in cards:
            hand.remove(card)
        bonus: int = self.card_bonus
        self._increment_card_bonus()
        return bonus

    def get_reinforcement_count(self, player: Player) -> int:
        count: int = max(3, self._get_num_territories(player) // 3)
        count += self._get_continent_bonuses(player)
        return count
    
    def get_territories(self, player: Player) -> set[Territory]:
        territories: set[Territory] = set()
        for territory in Territory:
            if self.map[territory].player == player:
                territories.add(territory)

        return territories
    
    def get_connected_territory_groups(self, player: Player) -> set[frozenset[Territory]]:
        unvisited: set[Territory] = self.get_territories(player)
        groups: set[frozenset[Territory]] = set()

        while unvisited:
            source: Territory = next(iter(unvisited))
            component: set[Territory] = {source}
            queue: deque[Territory] = deque([source])

            while queue:
                current: Territory = queue.popleft()
                for neighbor in self.adj_list[current]:
                    if neighbor in unvisited and neighbor not in component:
                        component.add(neighbor)
                        queue.append(neighbor)

            groups.add(frozenset(component))
            unvisited -= component

        return groups

    def _get_num_territories(self, player: Player) -> int:
        return len(self.get_territories(player))

    def _get_continent_bonuses(self, player: Player) -> int:
        bonus: int = 0
        for continent in Continent:
            if all(self.map[t].player == player for t in continent.territories):
                bonus += continent.bonus
        return bonus
    
    def _is_valid_set(self, cards: tuple[Card, Card, Card]) -> bool:
        types: list[CardType] = [c.card_type for c in cards]
        if CardType.WILD in types:
            return True
        return len(set(types)) == 1 or len(set(types)) == 3

    def _increment_card_bonus(self) -> None:
        if self.card_bonus < 12:
            self.card_bonus += 2
        elif self.card_bonus == 12:
            self.card_bonus += 3
        else:
            self.card_bonus += 5

    def _get_card_bonus(self, cards: tuple[Card, Card, Card]) -> int:
        if self._is_valid_set(cards):
            bonus: int = self.card_bonus
            self._increment_card_bonus()
            return bonus
        return 0
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RiskBoard):
            return self.map == other.map
        return False
    
    def __hash__(self) -> int:
        return hash(frozenset(self.map.items()))



@dataclass
class ReinforcePhase:
    troops_remaining: int

@dataclass
class CardTradePhase:
    base_troops: int

@dataclass
class AttackPhase:
    pass

@dataclass
class AttackResolvePhase:
    pass

@dataclass
class FortifyPhase:
    pass

Phase = ReinforcePhase | CardTradePhase | AttackPhase | AttackResolvePhase | FortifyPhase


class RiskState(State):
    def __init__(self, representation: RiskBoard, players: list[Player], player: Player, phase: Phase) -> None:
        self.phase: Phase = phase
        super().__init__(representation, players, player)

    def get_next_states(self) -> set['State']:
        states: set['State'] = set()

        if isinstance(self.phase, ReinforcePhase):
            for territory in self.representation.get_territories(self.player):
                board: RiskBoard = deepcopy(self.representation)
                board.place_one_troop(territory, self.player)

                new_troops_remaining: int = self.phase.troops_remaining - 1
                new_phase: Phase = ReinforcePhase(new_troops_remaining) if new_troops_remaining > 0 else AttackPhase()
                states.add(RiskState(board, self.players, self.player, new_phase))
        elif isinstance(self.phase, AttackPhase):
            pass
        elif isinstance(self.phase, AttackResolvePhase):
            pass
        elif isinstance(self.phase, CardTradePhase):
            hand: list[Card] = self.representation.hands.get(self.player, [])
            must_trade: bool = len(hand) >= 5

            if not must_trade:
                states.add(RiskState(
                    self.representation,
                    self.players,
                    self.player,
                    ReinforcePhase(self.phase.base_troops)
                ))

            for trade_set in self.representation.get_valid_trade_sets(self.player):
                board: RiskBoard = deepcopy(self.representation)
                bonus: int = board.trade_cards(self.player, trade_set)
                total_troops: int = self.phase.base_troops + bonus
                if len(board.hands[self.player]) >= 5:
                    new_phase: Phase = CardTradePhase(total_troops)
                else:
                    new_phase = ReinforcePhase(total_troops)
                states.add(RiskState(board, self.players, self.player, new_phase))

        elif isinstance(self.phase, FortifyPhase):
            next_player: Player = self.players[(self.players.index(self.player) + 1) % len(self.players)]
            base_troops: int = self.representation.get_reinforcement_count(next_player)

            states.add(RiskState(
                self.representation,
                self.players,
                next_player,
                CardTradePhase(base_troops)
            ))

            for group in self.representation.get_connected_territory_groups(self.player):
                for source in group:
                    source_troops: int = self.representation.map[source].num_troops
                    if source_troops < 2:
                        continue

                    for dest in group:
                        if source == dest:
                            continue

                        for num_troops in range(1, source_troops):
                            board: RiskBoard = deepcopy(self.representation)
                            board.transfer_troops(source, dest, self.player, num_troops)
                            states.add(RiskState(board, self.players, next_player, CardTradePhase(board.get_reinforcement_count(next_player))))

        return states

    @property
    def is_chance(self) -> bool:
        return isinstance(self.phase, AttackResolvePhase)
    
    def get_chance_outcomes(self) -> dict['State', float]:
        raise NotImplementedError

    def calculate_value(self, player: Player) -> float:
        raise NotImplementedError

    def is_terminal_state(self) -> bool:
        raise NotImplementedError