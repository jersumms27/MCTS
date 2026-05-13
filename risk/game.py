from enum import Enum

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

class Board:
    def __init__(self) -> None:
        self.adj_list: dict[Territory, frozenset[Territory]] = {
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
            Territory.YAKUTSK: frozenset((Territory.IRKUTSK, Territory.KAMCHATKA, Territory.SIBERIA))
        }
