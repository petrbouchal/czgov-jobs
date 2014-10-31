from __future__ import unicode_literals, print_function, division
# This Python file uses the following encoding: utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from lib_minscrapers import scrapejobs, scrapepages, savejobsdb
from datetime import datetime

now = datetime.now()

__author__ = 'petrbouchal'

from bodiesdata import paramsjson as minparameters
# Loop

activedepts = ['MPO', 'MPSV', 'UV', 'MZd', 'MSMT', 'MF', 'MMR', 'MV', 'MZe', 'MK', 'MSp',
               'MO', 'MD', 'MZV', 'CSSZ','FS','UP','NKU','CzechInvest','CS-P','CS-S','CS-S2']
# activedepts = ['CS-S','CS-P','CS-S2']

jobsallbodies = []
for dept in activedepts:
    # print(dept)
    jobsallbodies = jobsallbodies + scrapepages(now, minparameters[dept])
print('Celkem nalezeno pozic: ', len(jobsallbodies))
from pprint import pprint
# pprint(jobsall)

import litepiesql
import sqlite3

db = sqlite3.connect('data.sqlite')
cursor = db.cursor()

# Create table if it doesn't exist [can be rewritten to put condition straight into SQL]
cursor.execute("""
                  IF NOT EXISTS data CREATE TABLE data
                  (jobid, jobtitle, joburl, dept, firstseen timestamp, lastseen timestamp)
               """)

db.commit()
db.close()

db = litepiesql.Database('data.sqlite')
for row in jobsallbodies:
    # db.insert('data', row)
    savejobsdb(row, now)
    # print(row)

# possibly add code to mark up whether job is live (will need to read all jobs)
# and if live how many days it's been up
