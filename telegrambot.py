# -*- coding: utf-8 -*-
import os
import ast
import time
import telepot

from apscheduler.schedulers.background import BackgroundScheduler


token = '709434769:AAHiglAptFiOEELiwfkbLcF4xWcyvqUUJeo'
update_id = 0
TelegramBot = telepot.Bot(token)


def get_stat_begin_data():
    with open('history.txt', 'r') as tmp_file:
        first_line = tmp_file.readline()

    record = ast.literal_eval(first_line)
    begin_data = time.ctime(record['message']['date'])
    begin_data_time = time.strptime(begin_data)
    begin_data_str = time.strftime("%d %B %Y - %H:%M:%S", begin_data_time)

    return begin_data_str


def get_group_history(update_id):
    tmp_history = TelegramBot.getUpdates(offset=update_id, timeout=60)
    length_tmp_history = len(tmp_history)
    next_update_id = tmp_history[-1]['update_id'] + 1 if length_tmp_history != 0 else 0

    with open('history.txt', 'a') as tmp_file:
        for record in tmp_history:
            tmp_file.write(str(record) + '\n')

    get_group_history(next_update_id) if length_tmp_history == 100 else parse_history()


def parse_history():
    sum_line = 0
    users_dict_activity = dict()

    with open('history.txt', 'r') as tmp_file:
        for line in tmp_file.readlines():
            sum_line += 1
            record = ast.literal_eval(line)

            if 'edited_message' in record.keys():
                record['message'] = record.pop('edited_message')
            user = record['message']['from']['id']

            if user not in users_dict_activity:
                users_dict_activity[user] = 1
            else:
                users_dict_activity[user] += 1

    get_activity_persent(users_dict_activity, sum_line)


def get_activity_persent(users_dict_activity, sum_line):
    activity_percent = dict()
    for key, value in users_dict_activity.items():
        percent = value * 100 / sum_line
        activity_percent[key] = percent

    build_stat_message(users_dict_activity, activity_percent, sum_line)


def build_stat_message(users_dict_activity, activity_percent, sum_line):
    user_sort_by_activity = sorted(activity_percent.items(), key=lambda kv: kv[1])
    user_sort_by_activity.reverse()
    msg = ' активность в чате за последние 24 часа ( %s ):\n -= %d сообщений =-\n' % (get_stat_begin_data() if sum_line != 0 else '- нет активности -', sum_line)
    os.remove('history.txt')

    for user_stat in user_sort_by_activity:
        user_data = TelegramBot.getChatMember(chat_id='-1001138432342', user_id=user_stat[0])
        extra_msg = '- %s %s -> %d сообщений ( %.2f %% )\n' % (user_data['user']['first_name'], user_data['user'].get('last_name', 'Unknown'), users_dict_activity.get(user_data['user']['id']), user_stat[1])
        msg += extra_msg

    print_msg(msg)


def print_msg(msg):
    TelegramBot.sendMessage(chat_id='-1001138432342', text=msg)

if __name__ == '__main__':
    sched = BackgroundScheduler()

    sched.add_job(get_group_history, 'cron', [update_id], hour=18, minute=30)
    sched.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        TelegramBot.sendMessage(chat_id='-1001138432342', text='ВНИМАНИЕ!!!\n Принудительное завершение или сбой на платформе Heroku. Сбор статистики остановлен!')
        # print('qqq')
