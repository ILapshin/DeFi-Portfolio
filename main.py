import os

from bot import PortfolioBot
from portfoliointerface import PortfolioInterface
from portfolio import Portfolio

from dotenv import load_dotenv
from chains import CHAINS_CONFIG

load_dotenv()

JSON_USERS_PATH = os.environ.get('JSON_USERS_PATH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')


portfolio = Portfolio(CHAINS_CONFIG, JSON_USERS_PATH)

portfolio_interface = PortfolioInterface(portfolio)

bot = PortfolioBot(BOT_TOKEN, portfolio_interface)
