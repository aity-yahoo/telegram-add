from flask import Flask
import setup
import scraper

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/setup')
def run_setup():
    setup.setup()
    return "Setup process started."

@app.route('/scraper')
def run_scraper():
    scraper.scraper()
    return "Scraper process started."

if __name__ == '__main__':
    app.run()
