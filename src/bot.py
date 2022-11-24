from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.message import ParseMode

from portfolio import Portfolio
from coinlist import *
from strings import *



class PortfolioBot:

    def __init__(self, bot_token, portfolio: Portfolio):

        bot = Bot(bot_token)
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        portfolio = portfolio

        #States

        class AddAddress(StatesGroup):
            requesting_address = State() 

        class DeleteAddress(StatesGroup):
            requesting_address = State() 

        #region Keyboards

        btn_add_address = KeyboardButton(ADD_ADDRESS)
        btn_delete_address = KeyboardButton(DELETE_ADDRESS)
        btn_help = KeyboardButton(HELP)
        btn_show_addresses = KeyboardButton(SHOW_ADDRESSES)
        btn_portfolio = KeyboardButton(DEFI_PORTFOLIO)

        main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        main_keyboard.row(btn_add_address, btn_delete_address)
        main_keyboard.row(btn_show_addresses, btn_help)
        main_keyboard.add(btn_portfolio)

        #endregion


        #region Portfolio Interaction

        def show_addresses_msg(res):
            if res == NO_ADDRESSES_ADDED:
                return msg

            msg = ADDED_ADDRESSES
            for chain, value in res.items():
                msg = msg + f'\n\n*/{chain}*: '
                for address in value:
                    msg = msg + f'\n★ `{address}`'
                msg = msg + '\n'
                
            return msg


        def get_chain_portfolio_msg(res):
            
            answer_msg = ''         

            if res == NO_ADDRESSES_ADDED:
                answer_msg = NO_ADDRESSES_ADDED   

            if res == ERROR:
                answer_msg = SOMETHING_WENT_WRONG

            else:
                answer_msg = CHAIN_PORTFOLIO_MSG.format(
                    chain_name=res['chain_name'],
                    amount=round(res['amount'], 2),
                    coin_name=res['coin'],
                    coin_price=res['coin_price'],
                    price=round(res['price'], 2)
                )
                
            return answer_msg


        def get_portfolio_msg(res):
            
            answer_msg = PORTFOLIO_SUMM.format(summ=round(res['summ'], 2))

            for chain, value in res['prices'].items():

                if value == ERROR:
                    answer_msg = answer_msg + COULD_NOT_GET_DATA
                    continue

                answer_msg = answer_msg + '\n' + PORTFOLIO_PERCENT.format(
                        chain=chain,
                        price = round(value[1], 2),
                        percent = round(value[1] * 100 / res['summ'], 1)
                    )
            
            return answer_msg

        #endregion
               
        
        #region Common

        @dp.message_handler(CommandStart())
        async def process_start_command(message: Message):
            
            await message.reply(START_MSG + HELP_MSG, reply_markup=main_keyboard)

        
        @dp.message_handler(Text(equals=HELP))
        async def get_portfolio(message: Message):

            await message.reply(HELP_MSG)

        #endregion


        #region Address management

        @dp.message_handler(Text(equals=SHOW_ADDRESSES))
        async def show_addresses(message: Message):
            
            res = await portfolio.show_addresses(message.from_user.id)

            msg = show_addresses_msg(res)
           
            await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


        @dp.message_handler(Text(equals=ADD_ADDRESS))
        async def requesting_address(message: Message):

            await AddAddress.requesting_address.set()
            await message.reply(INPUT_ADDRESS)

        
        @dp.message_handler(state=AddAddress.requesting_address)
        async def add_address(message: Message):

            res = await portfolio.add_address(message.from_user.id, message.text)
            await AddAddress.next()
            await message.reply(res)

        
        @dp.message_handler(Text(equals=DELETE_ADDRESS))
        async def requesting_del_address(message: Message):

            await DeleteAddress.requesting_address.set()
            await message.reply(INPUT_ADDRESS_TO_DELETE)

        
        @dp.message_handler(state=DeleteAddress.requesting_address)
        async def delete_address(message: Message):

            res = await portfolio.delete_address(message.from_user.id, message.text)
            await DeleteAddress.next()
            await message.reply(res)

        #endregion


        #region Portfolio

        @dp.message_handler(Text(equals=DEFI_PORTFOLIO))
        async def get_portfolio(message: Message):

            msg = await message.reply(PORTFOLIO_UPDATING)

            res = await portfolio.get_portfolio(message.from_user.id)

            answer_msg = get_portfolio_msg(res)
           
            await bot.edit_message_text(answer_msg, chat_id=message.chat.id, message_id=msg.message_id)


        @dp.message_handler(commands=CHAINS_CONFIG.keys())
        async def get_chain_portfolio(message: Message):
           
            msg = await message.reply(PORTFOLIO_UPDATING)

            res = await portfolio.get_chain_portfolio(message.from_user.id, message.text[1:])

            answer_msg = get_chain_portfolio_msg(res)
           
            await bot.edit_message_text(answer_msg, chat_id=message.chat.id, message_id=msg.message_id)

        #endregion       
        
        executor.start_polling(dp, skip_updates=True)