import os

from dotenv import load_dotenv

from coinlist import *

load_dotenv()

ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
POLYGONSCAN_API_KEY = os.environ.get('POLYGONSCAN_API_KEY')
BSCSCAN_API_KEY = os.environ.get('BSCSCAN_API_KEY')

CHAINS_CONFIG = {

    btc: {
        'name': btc,
        'chain_type': btc,
        'address_regex': ['^1[a-zA-Z0-9]{27,34}', '^3[a-zA-Z0-9]{27,34}', '^bc1[a-zA-Z0-9]{27,34}'],
        'decimals': 8, 
        'request_template': 'https://blockchain.info/rawaddr/{address}',
        'tokens_json': None,
        'result_key': ['final_balance'],
        'coin_name': BTC,
        'api_key': None,
        'hex_result': False,
        'web3_provider_url': None,
        'multicall_chain_name': None
    },

    eth: {
        'name': eth,
        'chain_type': erc20,
        'address_regex': ['^0x[a-zA-Z0-9]{38}'],
        'decimals': 18, 
        'request_template': 'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}',
        'tokens_json': 'eth_tokens.json',
        'result_key': ['result'],
        'coin_name': ETH,
        'api_key': ETHERSCAN_API_KEY,
        'hex_result': False,
        'web3_provider_url': 'https://rpc.ankr.com/eth', 
        'multicall_chain_name': 'mainnet'
    },

    bsc: {
        'name': bsc,
        'chain_type': erc20,
        'address_regex': ['^0x[a-zA-Z0-9]{38}'],
        'decimals': 18, 
        'request_template': 'https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey={api_key}',
        'tokens_json': 'bsc_tokens.json',
        'result_key': ['result'],
        'coin_name': BNB,
        'api_key': BSCSCAN_API_KEY,
        'hex_result': False,
        'web3_provider_url': 'https://bsc-dataseed.binance.org/',
        'multicall_chain_name': 'bsc-mainnet'
    },

    polygon: {
        'name': polygon,
        'chain_type': erc20,
        'address_regex': ['^0x[a-zA-Z0-9]{38}'],
        'decimals': 18, 
        'request_template': 'https://api.polygonscan.com/api?module=account&action=balance&address={address}&apikey={api_key}',
        'tokens_json': 'polygon_tokens.json',
        'result_key': ['result'],
        'coin_name': MATIC,
        'api_key': POLYGONSCAN_API_KEY,
        'hex_result': False,
        'web3_provider_url': 'https://polygon-rpc.com', 
        'multicall_chain_name': 'polygon'
    },

    etc: {
        'name': etc,
        'chain_type': erc20,
        'address_regex': ['^0x[a-zA-Z0-9]{38}'],
        'decimals': 18, 
        'request_template': 'https://blockscout.com/etc/mainnet/api?module=account&action=eth_get_balance&address={address}',
        'tokens_json': None,
        'result_key': ['result'],
        'coin_name': ETC,
        'api_key': None,
        'hex_result': True,
        'web3_provider_url': None,
        'multicall_chain_name': None
    },
    
    flux: {
        'name': flux,
        'chain_type': flux,
        'address_regex': ['^t1[a-zA-Z0-9]'],
        'decimals': 8, 
        'request_template': 'https://api.runonflux.io/explorer/balance?address={address}',
        'tokens_json': None,
        'result_key': ['data'],
        'coin_name': FLUX,
        'api_key': None,
        'hex_result': False,
        'web3_provider_url': None,
        'multicall_chain_name': None
    },

    rvn: {
        'name': rvn,
        'chain_type': rvn,
        'address_regex': ['^R[a-zA-Z0-9]'],
        'decimals': 0, 
        'request_template': 'https://rvn.cryptoscope.io/api/getbalance/?address={address}',
        'tokens_json': None,
        'result_key': ['balance'],
        'coin_name': RVN,
        'api_key': None,
        'hex_result': False,
        'web3_provider_url': None,
        'multicall_chain_name': None
    },

    ton: {
        'name': ton,
        'chain_type': ton,
        'address_regex': ['^E[a-zA-Z0-9]'],
        'decimals': 9, 
        'request_template': 'https://api.ton.sh/getAddressInformation?address={address}',
        'tokens_json': None,
        'result_key': ['result', 'balance'],
        'coin_name': TON,
        'api_key': None,
        'hex_result': False,
        'web3_provider_url': None,
        'multicall_chain_name': None
    },

    ergo: {
        'name': ergo,
        'chain_type': ergo,
        'address_regex': ['^9[a-zA-Z0-9]'],
        'decimals': 9, 
        'request_template': 'https://ergo.watch/api/v0/addresses/{address}/balance',
        'tokens_json': None,
        'result_key': [],
        'coin_name': ERG,
        'api_key': None,
        'hex_result': False,
        'web3_provider_url': None,
        'multicall_chain_name': None
    },

    firo: {
        'name': firo,
        'chain_type': firo,
        'address_regex': ['^a[a-zA-Z0-9]'],
        'decimals': 0, 
        'request_template': 'https://chainz.cryptoid.info/firo/api.dws?q=addressinfo&a={address}',
        'tokens_json': None,
        'result_key': ['balance'],
        'coin_name': FIRO,
        'api_key': None,
        'hex_result': False,
        'web3_provider_url': None,
        'multicall_chain_name': None
    }
}