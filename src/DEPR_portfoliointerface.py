from portfolio import Portfolio
from strings import *
from enums import *

class PortfolioInterface:

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    
    #region Address management

    async def add_address(self, telegram_id, address):

        res = await self.portfolio.add_address(telegram_id, address)

        if res == ResponceAddAddress.INVALID:
            return ADDRESS_INVALID
        if res == ResponceAddAddress.EXISTS:
            return ADDRESS_EXISTS
        if res == ResponceAddAddress.OK:
            return ADDRESS_OK.format(address=address)


    async def delete_address(self, telegram_id, address):

        res = await self.portfolio.delete_address(telegram_id, address)

        if res == ResponceDeleteAddress.INVALID:
            return ADDRESS_INVALID
        if res == ResponceDeleteAddress.NOT_FOUND:
            return USER_NOT_FOUND
        if res == ResponceDeleteAddress.OK:
            return ADDRESS_DELETED.format(address=address)
    

    async def show_addresses(self, telegram_id):
        res = await self.portfolio.show_addresses(telegram_id)

        if res == ResponceShowAddresses.NOT_FOUND:
            msg = NO_ADDRESSES_ADDED
            return msg

        msg = ADDED_ADDRESSES
        for chain, value in res.items():
            msg = msg + f'\n\n*{chain}*: '
            for address in value:
                msg = msg + f'\n★ `{address}`'
            msg = msg + '\n'
            
        return msg

    #endregion


    #region Portfolio
    
    async def get_portfolio(self, telegram_id):
        info = await self.portfolio.get_portfolio(telegram_id)

        msg = PORTFOLIO_SUMM.format(summ=round(info['summ'], 2))

        for chain, value in info['prices'].items():

            if value == ResponcePrice.NO_DATA:
                msg = msg + NO_PRICE_DATA
            else:
                msg = msg + '\n' + PORTFOLIO_PERCENT.format(
                        chain=chain,
                        price = round(value[1], 2),
                        percent = round(value[1] * 100 / info['summ'], 1)
                    )
        
        return msg


    async def get_chain_portfolio(self, telegram_id, chain_name):
        info = await self.portfolio.get_chain_portfolio(telegram_id, chain_name)

        if info == ResponcePrice.NO_ADDRESS:
            return NO_ADDRESSES_ADDED

        msg = CHAIN_PORTFOLIO_MSG.format(
            chain_name=chain_name,
            amount=round(info['amount'], 2),
            coin_name=info['coin'],
            coin_price=info['coin_price'],
            price=round(info['price'], 2)
        )
               
        return msg

    #endregion