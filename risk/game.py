from enum import Enum
from typing import Any
from mcts.state import State

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
        self.hand: set[Card] = set()
    
    def add_card(self, card: Card) -> None:
        self.hand.add(card)
    
    def remove_card(self, card: Card) -> Card | None:
        if card in self.hand:
            self.hand.remove(card)
            return card
    
    def remove_cards(self, cards: set[Card]) -> set[Card] | None:
        removed_cards: set[Card] = set()
        for card in cards:
            removed_card: Card | None = self.remove_card(card)
            if removed_card is None:
                return None
        
        return removed_cards
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Player):
            return self.name == other.name and self.color == other.color
        return False
    
    def __hash__(self) -> int:
        return hash(self.name)



class Board:
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
        self.map: dict[Territory, tuple[Player | None, int]]
        self.reset_board()

        self.card_bonus: int = 4
    
    def update_board(self, territory: Territory, new_player: Player | None = None, new_troops: int = 0) -> None:
        self.map[territory] = new_player, new_troops
    
    def reset_board(self) -> None:
        self.map = {t: (None, 0) for t in Territory}
    
    def get_reinforcement_count(self, player: Player, cards: tuple[Card, Card, Card] | None = None) -> int:
        count: int = min(3, self._get_num_territories(player) // 3)
        count += self._get_continent_bonus(player)
    
    def _get_num_territories(self, player: Player) -> int:
        num: int = 0
        for territory in Territory:
            if self.map[territory][0] == player:
                num += 1

        return num

    def _get_continent_bonus(self,  player: Player) -> int:
        bonus: int = 0

        for continent in Continent:
            full: bool = True
            for territory in continent.territories:
                if self.map[territory][0] != player:
                    full = False
                    break
            
            if full:
                bonus += continent.bonus
        
        return bonus
    
    def _increment_card_bonus(self) -> None:
        if self.card_bonus < 12:
            self.card_bonus += 2
        elif self.card_bonus == 12:
            self.card_bonus += 3
        else:
            self.card_bonus += 5
    
    def _get_card_bonus(self, cards: tuple[Card, Card, Card]) -> int:
        pass
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Board):
            return self.map == other.map
        return False
    
    def __hash__(self) -> int:
        return hash(frozenset(sorted(self.map.items())))



class Phase(Enum):
    REINFORCE = 'Reinforce'
    ATTACK = 'Attack'
    ATTACK_RESOLVE = 'Attack Resolve'
    FORTIFY = 'Fortify'


class RiskState(State):
    def __init__(self, representation: Board, num_players: int, player: int = 0, phase: Phase = Phase.REINFORCE) -> None:
        self.phase: Phase = phase
        super().__init__(representation, num_players, player)

    def get_next_states(self) -> set['State']:
        if self.phase == Phase.REINFORCE:



    @property
    def is_chance(self) -> bool:
        return self.phase == Phase.ATTACK_RESOLVE
    
    def get_chance_outcomes(self) -> dict['State', float]:
        pass

    def calculate_value(self, player: int) -> float:
        pass

    def is_terminal_state(self) -> bool:
        pass