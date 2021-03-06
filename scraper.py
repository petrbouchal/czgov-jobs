from __future__ import unicode_literals, print_function, division
# This Python file uses the following encoding: utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from lib_minscrapers import scrapejobs, scrapepages
from datetime import datetime

now = datetime.now()

__author__ = 'petrbouchal'

from bodiesdata import paramsjson as minparameters
# Loop

print('Starting scraper...')
import bs4
print(bs4.__version__)

activedepts = ['MPO', 'MPSV', 'UV', 'MSMT', 'MMR-P', 'MMR-S', 'MV', 'MZe',
               'MO', 'MD', 'MZV', 'CSSZ','FS','UP','NKU','CzechInvest','CS-P','CS-S','CS-S2',
               'CSI']
# activedepts = ['UV']

jobsallbodies = []
for dept in activedepts:
    # print(dept)
    jobsallbodies = jobsallbodies + scrapepages(now, minparameters[dept])
print('Celkem nalezeno pozic: ', len(jobsallbodies))

import litepiesql
import sqlite3

db = sqlite3.connect('data.sqlite')
cursor = db.cursor()

if len(cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='data';""").fetchall()) == 0:
    cursor.execute("""CREATE TABLE data
                        (jobtitle, joburl, dept, datetime timestamp)
                    """)
db.commit()
db.close()

db = litepiesql.Database('data.sqlite')
for row in jobsallbodies:
    db.insert('data', row)
    # print(row)
