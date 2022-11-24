from enum import Enum

from strings import *

class ResponceAddAddress(Enum):

    # Addresses
    OK = 0
    EXISTS = 1
    INVALID = 2

class ResponceDeleteAddress(Enum):

    # Addresses
    OK = 0
    NOT_FOUND = 1
    INVALID = 2


class ResponceShowAddresses(Enum):

    NOT_FOUND = 1
    INVALID = 2


class ResponcePrice(Enum):

    NO_DATA = 1
    NO_ADDRESS = 2