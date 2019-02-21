import os


token = os.environ.get('BOT_TOKEN')

chat_id = os.environ.get('CHAT_ID')

appid = 'c387e9eac059a7bf80345a729f18ea9c'

update_id = 0

weather_json = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s'

msg_weather = '%s, температура: %.1f \N{DEGREE SIGN}C, влажность: %d %%, скорость ветра: %d м/с, давление: %.2f мм.рт.ст., %s'

msg_error = 'ВНИМАНИЕ!!!\n Принудительное завершение или сбой на платформе Heroku.'

day = '24 часа'

week = 'неделю'

msg_activity = 'зафиксировано %d сообщений за %s\n'