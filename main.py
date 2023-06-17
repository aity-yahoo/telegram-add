from scraper import scraper
from setup import bot
from keep_alive import keep_alive

keep_alive()

if __name__ == "__main__":
    scraper()
    bot.polling()
