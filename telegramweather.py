import time
import telepot
from telepot.loop import MessageLoop
import requests


TOKEN = '709434769:AAHiglAptFiOEELiwfkbLcF4xWcyvqUUJeo'
APPID = 'c387e9eac059a7bf80345a729f18ea9c'

bot = telepot.Bot(TOKEN)


def get_data(city):
    request_str = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=c387e9eac059a7bf80345a729f18ea9c' % city
    response = requests.get(request_str).json()
    weather_msg = '%s, температура: %.1f \N{DEGREE SIGN}C, влажность: %d %%, скорость ветра: %d м/с, давление: %.2f мм.рт.ст., %s' % (
        response['name'], response['main']['temp'] - 273.15, response['main']['humidity'],
        response['wind']['speed'], response['main']['pressure'] * 0.75, response['weather'][0]['description'])

    return weather_msg


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text' and msg['text'].lower() == '.погода':
        weather_msg = get_data('Minsk')
        bot.sendMessage(chat_id, weather_msg)

    elif content_type == 'text' and msg['text'].lower() == '.погодам':
        weather_msg = get_data('Moscow')
        bot.sendMessage(chat_id, weather_msg)

    elif content_type == 'text' and msg['text'].lower() == '.погодал':
        weather_msg = get_data('Lyubertsy')
        bot.sendMessage(chat_id, weather_msg)



MessageLoop(bot, handle).run_as_thread()

# Keep the program running.
while 1:
    time.sleep(1)
