#!/usr/bin/env python3

import subprocess

import schedule
import time


def import_and_update():
    subprocess.call(['python3', 'manage.py', 'geovite_import'])

# schedule.every().day.at("0:02").do(import_and_update)
schedule.every().day.at("15:42").do(import_and_update)
# schedule.every().second.do(import_and_update)


def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
