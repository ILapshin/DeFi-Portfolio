import os
import requests
import json
import re

from dotenv import load_dotenv
from web3 import Web3

from coinlist import *
from enums import *
from erc20_abi import ERC20_ABI
from simple_multicall import Multicall

load_dotenv()

ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
POLYGONSCAN_API_KEY = os.environ.get('POLYGONSCAN_API_KEY')
BSCSCAN_API_KEY = os.environ.get('BSCSCAN_API_KEY')
COINMARKETCAP_API_KEY = os.environ.get('COINMARKETCAP_API_KEY')


class Chain:

    def __init__(
        self, 
        name, 
        chain_type,
        address_regex,
        decimals, 
        request_template, 
        tokens_json,
        result_key, 
        coin_name,
        api_key=None, 
        hex_result=False,
        web3_provider_url=None,
        multicall_chain_name=None
    ):
        self.name = name
        self.chain_type = chain_type
        self.address_regex = address_regex
        self.decimals = decimals
        self.request_template = request_template
        self.tokens_json = tokens_json
        self.result_key = result_key
        self.coin_name = coin_name
        self.api_key = api_key
        self.hex_result = hex_result

        self.web3 = None
        if web3_provider_url:
            self.web3 = Web3(Web3.HTTPProvider(web3_provider_url))
            # print('web3 is connected:', self.web3.isConnected())
        self.multicall = None
        if multicall_chain_name:
            self.multicall = Multicall(
                self.web3, 
                chain=multicall_chain_name
            )

    
    def get_balance_request(self, address):
        if self.api_key:
            return self.request_template.format(address=address, api_key=self.api_key)
        else:
            return self.request_template.format(address=address)



class Portfolio:

    def __init__(self, chains_config, users_file_path): 

        self.chains = {}      

        for chain, value in chains_config.items():

            tokens_json = {}
            if value['tokens_json']:
                with open (value['tokens_json'], 'r') as file:
                    tokens_json = json.load(file)

            self.chains[chain] = Chain(
                    name=value['name'],
                    chain_type=value['chain_type'],
                    address_regex=value['address_regex'],
                    decimals=value['decimals'],
                    request_template=value['request_template'],
                    tokens_json=tokens_json,
                    result_key=value['result_key'],
                    coin_name=value['coin_name'],
                    api_key=value['api_key'],
                    hex_result=value['hex_result'],
                    web3_provider_url=value['web3_provider_url'],
                    multicall_chain_name=value['multicall_chain_name']
                )

        self.users_file_path = users_file_path
        self.users = self.download_users()


    def download_users(self):
        with open(self.users_file_path, 'r') as openfile:    
            try: 
                json_object = json.load(openfile)
            except:
                return {}
        return json_object


    def write_users(self):
        with open(self.users_file_path, "w") as outfile:
            outfile.write(json.dumps(self.users))


    def define_chain_by_address(self, address):
        res = {}

        for chain_name, chain in self.chains.items():
            for address_regex in chain.address_regex:
                match = re.match(address_regex, address) 
                if match:
                    res[chain.chain_type] = address
        
        return res


    async def add_address(self, telegram_id, address):

        user_id = str(telegram_id)

        if user_id not in self.users:
            self.users[user_id] = {}

        chains = self.define_chain_by_address(address)

        if not chains:
            return ResponceAddAddress.INVALID

        for chain_type, address in chains.items():
            if chain_type not in self.users[user_id]:
                self.users[user_id][chain_type] = []
        
            if address in self.users[user_id][chain_type]:
                return ResponceAddAddress.EXISTS

            self.users[user_id][chain_type].append(address)

        self.write_users()

        return ResponceAddAddress.OK


    async def delete_address(self, telegram_id, address):

        user_id = str(telegram_id)

        if user_id not in self.users:
            return ResponceDeleteAddress.NOT_FOUND

        chains = self.define_chain_by_address(address)

        if not chains:
            return ResponceDeleteAddress.INVALID
        
        empty_chains = []
        for chain_type, address in chains.items():
            self.users[user_id][chain_type].remove(address)
            if not self.users[user_id][chain_type]:
                empty_chains.append(chain_type)
        
        for chain_type in empty_chains:
            self.users[user_id].pop(chain_type, None)

        self.write_users()   
        return ResponceDeleteAddress.OK


    async def show_addresses(self, telegram_id):

        user_id = str(telegram_id)

        if user_id not in self.users:
            return ResponceShowAddresses.NOT_FOUND
        
        return self.users[user_id]


    async def get_coin_balance(self, chain_name, address):

        chain = self.chains[chain_name]

        request = chain.get_balance_request(address)

        try:
            res = requests.get(request)
            # print(res.json())
        except:
            return 0

        if res.status_code != 200:
            return 0

        ammount = res.json()
        for key in chain.result_key:
            ammount = ammount[key]

        if chain.hex_result:
            ammount = int(ammount, 16)

        return float(ammount) / 10**chain.decimals


    async def get_all_coin_balances(self, addresses_list):

        balances = {}
        
        for chain_type, addresses in addresses_list.items():
            for chain_name, chain in self.chains.items():
                if chain_type != chain.chain_type:
                    continue
                for address in addresses:
                    balance = await self.get_coin_balance(chain_name, address)
                    # print(chain_name, balance)
                    if balance > 0:
                        #coin_name = self.chains[chain_name].coin_name
                        if chain_name in balances:
                            balances[chain_name] = balances[chain_name] + balance
                        else:
                            balances[chain_name] = balance

        return balances


    async def get_erc20_balance(self, web3, token_address, owner_address):

        token = web3.eth.contract(address=token_address, abi=ERC20_ABI) 
        token_balance = token.functions.balanceOf(owner_address).call()
        
        return Web3.fromWei(token_balance, 'ether')


    async def get_all_erc20_balances(self, addresses_list):

        result = {}

        for chain_name, chain in self.chains.items():

            for address in addresses_list[chain_name]:
                if chain.web3:
                    balances = await self.get_all_erc20_of_chain(chain_name, address)
                    print(balances)
                    
                    result[chain_name] = {}

                    for token_name, token_balance in balances.items():
                        if token_name in result[chain_name]:
                            result[chain_name][token_name] = result[chain_name][token_name] + token_balance
                        else:
                            result[chain_name][token_name] = token_balance                        
        
        # print(result)
        return result
   

    async def get_all_erc20_of_chain(self, chain_name, address):
        
        result = {}
        chain = self.chains[chain_name]

        if not chain.multicall:
            return result

        calls = []

        for token_address in chain.tokens_json.values():
            token = chain.web3.eth.contract(address= Web3.toChecksumAddress(token_address), abi=ERC20_ABI)

            calls.append(chain.multicall.create_call(token, 'balanceOf', [Web3.toChecksumAddress(address)]))
                    
        raw_result = chain.multicall.call(calls)

        # print(raw_result)

        for i in range(len(raw_result[1])):
            balance = int(raw_result[1][i].hex(), 16)

            if balance > 0:
                result[list(chain.tokens_json.keys())[i]] = float(Web3.fromWei(balance, 'ether'))
        
        # print(result)
        return result
        

    async def get_binance_price(self, coin):

        wrapped_coins = (
            'WETH',
            'WBTC',
            'WBNB',

        )

        if coin in wrapped_coins:
            coin = coin[1:]

        # Trying to get price from Binance
        req = f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT'

        try:
            res = requests.get(req)
        except:
            # print(res.status_code)
            return None

        if res.status_code != 200:
            # print(coin)
            return None
         
        return float(res.json()['price'])


    async def get_huobi_price(self, coin):

        wrapped_coins = (
            'WETH',
            'WBTC',
            'WBNB',

        )

        if coin in wrapped_coins:
            coin = coin[1:]
       
        req = f'https://api.huobi.pro/market/trade?symbol={coin.lower()}usdt'

        try:
            res = requests.get(req)
        except:
            # print(res.status_code)
            return None

        if res.status_code != 200:
            # print(coin)
            return None

        if res.json()['status'] != 'ok':
            return None

        return float(res.json()['tick']['data'][0]['price'])


    async def get_asset_price(self, coin):
        
        price = await self.get_binance_price(coin)

        if not price:
            price = await self.get_huobi_price(coin)
        
        if not price:
            return ResponcePrice.NO_DATA

        # print(price)

        return price


    async def get_price_of_ammount(self, coin, ammount):
        
        price = await self.get_asset_price(coin)

        if price == ResponcePrice.NO_DATA:
            return price

        return ammount * price


    async def get_portfolio(self, telegram_id):

        user_id = str(telegram_id)

        addresses_list = self.users[user_id]    

        coin_balances = await self.get_all_coin_balances(addresses_list)

        prices = {}
        summ = 0

        for chain_name, amount in coin_balances.items():
            price = await self.get_price_of_ammount(self.chains[chain_name].coin_name, amount)

            if price == ResponcePrice.NO_DATA:
                continue

            prices[chain_name] = (amount, price)
            summ = summ + price

        return {'summ': summ, 'prices': prices}


    async def get_chain_portfolio(self, telegram_id, chain_name):

        user_id = str(telegram_id)

        try:
            addresses = self.users[user_id][self.chains[chain_name].chain_type]
        except:
            return ResponcePrice.NO_ADDRESS
        
        info = {'amount': 0}

        for address in addresses:
            info['amount'] = info['amount'] + await self.get_coin_balance(chain_name, address)

        info['coin'] = self.chains[chain_name].coin_name

        info['coin_price'] = await self.get_asset_price(info['coin'])

        info['price'] = await self.get_price_of_ammount(info['coin'], info['amount'])

        return info