# -*- coding: utf-8 -*-
import os
import ast
import time
import telepot
from apscheduler.schedulers.background import BackgroundScheduler
from config import token, update_id, chat_id, msg_error, msg_activity


class ActivityInfo(object):

    def __init__(self, token):
        self.sum_line = 0
        self.users_dict_activity = dict()
        self.activity_percent = dict()
        self.bot = telepot.Bot(token)

    def get_stat_begin_data(self):
        with open('history.txt', 'r') as tmp_file:
            first_line = tmp_file.readline()

        record = ast.literal_eval(first_line)
        begin_data = time.ctime(record['message']['date'])
        begin_data_time = time.strptime(begin_data)
        begin_data_str = time.strftime("%d %B %Y - %H:%M:%S", begin_data_time)

        return begin_data_str

    def get_group_history(self, update_id):
        tmp_history = self.bot.getUpdates(update_id, timeout=60)
        length_tmp_history = len(tmp_history)
        next_update_id = tmp_history[-1]['update_id'] + 1 if length_tmp_history != 0 else 0

        with open('history.txt', 'a') as tmp_file:
            for record in tmp_history:
                tmp_file.write(str(record) + '\n')

        self.get_group_history(next_update_id) if length_tmp_history == 100 else self.parse_history()

    def parse_history(self):
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

        self.get_activity_persent()

    def get_activity_persent(self):
        for key, value in self.users_dict_activity.items():
            percent = value * 100 / self.sum_line
            self.activity_percent[key] = percent

        self.build_stat_message()

    def build_stat_message(self):
        user_sort_by_activity = sorted(self.activity_percent.items(), key=lambda kv: kv[1])
        user_sort_by_activity.reverse()
        self.msg =  msg_activity % (self.get_stat_begin_data() if self.sum_line != 0 else '- нет активности -', self.sum_line)
        os.remove('history.txt')

        for user_stat in user_sort_by_activity:
            user_data = self.bot.getChatMember(chat_id='-1001138432342', user_id=user_stat[0])
            extra_msg = '- %s %s -> %d сообщений ( %.2f %% )\n' % (user_data['user']['first_name'], user_data['user'].get('last_name', 'Unknown'), self.users_dict_activity.get(user_data['user']['id']), user_stat[1])
            self.msg += extra_msg

        self.print_msg()

    def print_msg(self):
        self.bot.sendMessage(chat_id='-1001138432342', text=self.msg)


if __name__ == '__main__':
    activity = ActivityInfo(token)
    sched = BackgroundScheduler()

    sched.add_job(activity.get_group_history, 'cron', [update_id], hour=14, minute=25)
    sched.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        activity.bot.sendMessage(chat_id=chat_id, text=msg_error)
