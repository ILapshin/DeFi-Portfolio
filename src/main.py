import os
import logging

from bot import PortfolioBot
from portfolio import Portfolio

from dotenv import load_dotenv
from chains import CHAINS_CONFIG

load_dotenv()

JSON_USERS_PATH = './data/users.json'
BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    # filename='./logs/portfoliobot.log', filemode='w', 
    format='%(asctime)s | %(levelname)s | %(message)s', 
    level=logging.INFO)

portfolio = Portfolio(CHAINS_CONFIG, JSON_USERS_PATH)

bot = PortfolioBot(BOT_TOKEN, portfolio)
