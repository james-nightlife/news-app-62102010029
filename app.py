from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
OPEN_WEATHER_KEY = '39651ccc3ceaae76eb16278b5d85d88b'

OPEN_NEWS_URL = "http://newsapi.org/v2/everything?q={0}&sortBy=publishedAt&apiKey={1}"
OPEN_NEWS_KEY = '148d88bf010d41efabbef9caadb8a4f3'

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    covid = get_news("coronavirus", OPEN_NEWS_KEY)

    return render_template("home.html", weather=weather, covid=covid)

@app.route("/newssearch")
def newssearch():
    keyword = request.args.get('keyword')
    if not keyword:
        keyword = 'coronavirus'
    news = get_news(keyword, OPEN_NEWS_KEY)

    return render_template("newssearch.html", news=news, keyword=keyword)

@app.route("/aboutme")
def aboutme():
    return render_template("aboutme.html")

def get_weather(city,API_KEY):
    query = quote(city)
    url = OPEN_WEATHER_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):

        description = parsed['weather'][0]['description']
        icon = parsed['weather'][0]['icon']
        temperature = parsed['main']['temp']
        city = parsed['name']
        country = parsed['sys']['country']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        windspeed = parsed['wind']['speed']
        direction = get_direction(parsed['wind']['deg'])

        weather = {'description': description,
                   'temperature': temperature,
                   'city': city,
                   'country': country,
                   'pressure' : pressure,
                   'humidity' : humidity,
                   'windspeed' : windspeed,
                   'icon' : icon,
                   'direction' : direction
                   }

    return weather

def get_news(keyword, API_KEY):
    query = quote(keyword)
    url = OPEN_NEWS_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = []
    if parsed.get('articles'):
        for x in parsed['articles']:
            news.append(x)
    
    return news

def get_direction(degree):
    if (degree>337.5):
        return 'Northerly'
    if (degree>292.5):
        return 'North Westerly'
    if(degree>247.5):
        return 'Westerly'
    if(degree>202.5):
        return 'South Westerly'
    if(degree>157.5):
        return 'Southerly'
    if(degree>122.5):
        return 'South Easterly'
    if(degree>67.5):
        return 'Easterly'
    if(degree>22.5):
        return 'North Easterly'
    return 'Northerly'