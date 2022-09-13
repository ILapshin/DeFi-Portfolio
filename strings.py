from chains import CHAINS_CONFIG

START_MSG = 'Add your wallet address.\n\n'

HELP_MSG = 'Supported chains:\n' + '\n'.join(['★ ' + chain_name for chain_name in CHAINS_CONFIG])

#region Address management

#requests
INPUT_ADDRESS = 'Input your wallet address'
INPUT_ADDRESS_TO_DELETE = 'Input wallet address to delete'

#responces
ADDRESS_OK = 'Address {address} added'
ADDRESS_EXISTS = 'Address already added'
ADDRESS_INVALID = 'Invalid address. Please check and try again.'
ADDRESS_DELETED = 'Address {address} deleted'
USER_NOT_FOUND = 'User not found'

#messages
ADDED_ADDRESSES = 'Added addresses:'
NO_ADDRESSES_ADDED = 'No added addresses'

#endregion


#region Portfolio messages

PORTFOLIO_UPDATING = 'Your DeFi Portfolio is updating...'
PORTFOLIO_SUMM = 'Portfolio: {summ} USD'
PORTFOLIO_PERCENT = '/{chain}: {price} USD | {percent}%'
NO_PRICE_DATA = 'No price data'

CHAIN_PORTFOLIO_MSG = '{chain_name} portfolio:\nCoin price: {coin_price} USD\nBalance: {amount} {coin_name}\nPortfolio price: {price} USD'

#endregion


#region Buttons

ADD_ADDRESS = 'Add address'
DELETE_ADDRESS = 'Delete address'
HELP = 'Help'
SHOW_ADDRESSES = 'Show addresses'
DEFI_PORTFOLIO = 'DeFi Portfolio'

# endregion