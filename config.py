import os


token = os.environ.get('BOT_TOKEN')

chat_id = os.environ.get('CHAT_ID')

appid = 'c387e9eac059a7bf80345a729f18ea9c'

update_id = 0

weather_json = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s'

msg_weather = '%s, температура: %.1f \N{DEGREE SIGN}C, влажность: %d %%, скорость ветра: %d м/с, давление: %.2f мм.рт.ст., %s'

msg_error = 'ВНИМАНИЕ!!!\n Принудительное завершение или сбой на платформе Heroku.'

msg_activity = 'зафиксировано %d сообщений за последние 24 часа\n ( первое: %s ):\n'

text3 = '3х минутная готовность !'

text2 = '2е минуты, парни, терпите, не нажритесь !'

text1 = 'до Нового Года ОДНА минута ! и все еще пока $1 = 2,1598 BYN'

text = ' С НОВЫМ ГОДОМ парни !!!\n Здоровья и удачи вашим семьям. Достигайте новых вершин и самореализовывайтесь !\n p.s.:Вадим - ты мой создатель и ты лучший ! :)'