from scraper import scraper
from setup import bot

if __name__ == "__main__":
    scraper()
    bot.polling()
