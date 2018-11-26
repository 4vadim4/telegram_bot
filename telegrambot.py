# -*- coding: utf-8 -*-
import os
import ast
import telepot


token = '709434769:AAHiglAptFiOEELiwfkbLcF4xWcyvqUUJeo'
UPDATE_ID = 0
TelegramBot = telepot.Bot(token)


def get_group_history(UPDATE_ID):
    tmp_file = open('history.txt', 'a')
    tmp_history = TelegramBot.getUpdates(offset=UPDATE_ID)
    length_tmp_history = len(tmp_history)
    UPDATE_ID = tmp_history[-1]['update_id']

    for record in tmp_history:
        tmp_file.write(str(record) + '\n')
    tmp_file.close()

    if length_tmp_history == 100:
        get_group_history(UPDATE_ID + 1)
    else:
        parse_history()


def parse_history():
    sum_line = 0
    users_dict_activity = dict()
    tmp_file = open('history.txt', 'r')
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
    tmp_file.close()
    os.remove('history.txt')

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
    msg = ' активность в чате за последние 24 (в тест режиме меньше) часа:\n -= %d сообщений =-\n' % sum_line

    for user_stat in user_sort_by_activity:
        user_data = TelegramBot.getChatMember(chat_id='-1001138432342', user_id=user_stat[0])
        extra_msg = '- %s %s -> %d сообщений ( %.2f %% )\n' % (user_data['user']['first_name'], user_data['user'].get('last_name', 'Unknown'), users_dict_activity.get(user_data['user']['id']), user_stat[1])
        msg += extra_msg

    print_msg(msg)


def print_msg(msg):
    TelegramBot.sendMessage(chat_id='-1001138432342', text=msg)



get_group_history(UPDATE_ID)
