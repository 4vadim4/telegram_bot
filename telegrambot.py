# -*- coding: utf-8 -*-
import os
import ast
import time
import json
import telepot
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler
from config import token, update_id, chat_id, msg_error, msg_activity, day, week


class ActivityInfo(object):

    def __init__(self, token):
        self.sum_line = 0
        self.users_dict_activity = dict()
        self.activity_percent = dict()
        self.bot = telepot.Bot(token)

    @staticmethod
    def remove_history(file):
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

# Not uses
    # def get_stat_begin_data(self):
    #     with open('history.txt', 'r') as tmp_file:
    #         first_line = tmp_file.readline()
    #
    #     record = ast.literal_eval(first_line)
    #     if 'edited_message' in record.keys():
    #         record['message'] = record.pop('edited_message')
    #     begin_data = time.ctime(record['message']['date'])
    #     begin_data_time = time.strptime(begin_data)
    #     begin_data_str = time.strftime("%d %B %Y - %H:%M:%S", begin_data_time)
    #
    #     return begin_data_str

    def get_group_history(self, update_id):
        tmp_history = self.bot.getUpdates(update_id, timeout=60)
        length_tmp_history = len(tmp_history)
        next_update_id = tmp_history[-1]['update_id'] + 1 if length_tmp_history != 0 else 0

        with open('history.txt', 'a') as tmp_file:
            for record in tmp_history:
                tmp_file.write(str(record) + '\n')

        self.get_group_history(next_update_id) if length_tmp_history == 100 else self.parse_history()

    def parse_history(self, period=day):
        with open('history.txt', 'r') as tmp_file:
            for line in tmp_file.readlines():
                self.sum_line += 1
                record = ast.literal_eval(line)

                if 'edited_message' in record.keys():
                    record['message'] = record.pop('edited_message')
                user = record['message']['from']['id']

                if user not in self.users_dict_activity:
                    self.users_dict_activity[user] = 1
                else:
                    self.users_dict_activity[user] += 1

        self.get_activity_persent(self.users_dict_activity, period)
        self.accumulate_weekly_stat()

    def get_activity_persent(self, data_for_percent, period):
        for key, value in data_for_percent.items():
            percent = value * 100 / self.sum_line
            self.activity_percent[key] = percent

        self.build_stat_message(period)

    def build_stat_message(self, period):
        user_sort_by_activity = sorted(self.activity_percent.items(), key=lambda kv: kv[1])
        user_sort_by_activity.reverse()
        self.msg = msg_activity % (self.sum_line, period)

        for user_stat in user_sort_by_activity:
            user_data = self.bot.getChatMember(chat_id=chat_id, user_id=user_stat[0])
            extra_msg = '- %s %s -> %d сообщений ( %.2f %% )\n' % (user_data['user']['first_name'], user_data['user'].get('last_name', 'Unknown'),
                                                                   self.users_dict_activity.get(user_data['user']['id']), user_stat[1])
            self.msg += extra_msg

        self.print_msg()

    def print_msg(self):
        self.bot.sendMessage(chat_id=chat_id, text=self.msg)

    def adding_stat_info_to_file(self, stat_data):
        with open('week_stat.json', 'w') as file:
            json.dump(stat_data, file)

    @staticmethod
    def get_stat_info_from_file():
        with open('week_stat.json', 'r') as json_data:
            stat_data = json.load(json_data)
            return stat_data

    def accumulate_weekly_stat(self):
        try:
            interim_stat_data = defaultdict(int, activity.get_stat_info_from_file())
            for k, v in self.users_dict_activity.items():
                interim_stat_data[k] += v
            self.adding_stat_info_to_file(interim_stat_data)
        except FileNotFoundError:
            self.adding_stat_info_to_file(self.users_dict_activity)


    def week_stat(self):
        weekly_stat_data = activity.get_stat_info_from_file()
        self.sum_line = sum(weekly_stat_data.values())
        self.get_activity_persent(weekly_stat_data, period=week)
        time.sleep(5)
        activity.remove_history('week_stat.json')


if __name__ == '__main__':
    activity = ActivityInfo(token)
    sched = BackgroundScheduler()

    sched.add_job(activity.get_group_history, 'cron', [update_id], hour=6)
    sched.add_job(activity.remove_history, 'cron', ['history.txt'], hour=6, minute=15)
    sched.add_job(activity.week_stat, 'cron', day_of_week='mon', hour=6, minute=30)
    sched.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        activity.bot.sendMessage(chat_id=chat_id, text=msg_error)
