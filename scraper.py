from __future__ import unicode_literals, print_function, division
# This Python file uses the following encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from lib_minscrapers import scrapejobs, scrapepages
from datetime import datetime

now = datetime.now()

__author__ = 'petrbouchal'

# Basic infomration: name, proper abbreviation, top url and jobs url
ministerstva = {
    'MZP' : ['MŽP','Ministerstvo životního prostředí','http://www.mzp.cz','http://mzp.cz/cz/volna_mista'],
    'MZV' : ['MZV','Ministerstvo zahraničních věcí','http://www.mzv.cz','http://www.mzv.cz/jnp/cz/o_ministerstvu/zamestnani/aktualni_nabidky_zamestnani/index.html'],
}

# Parameters for scraping job pages of each department
# list of dicts: level1, level2, items, subitems + T/F whether going through subitems is needed
minparameters = {
    'MZP' : [False,
            {'name':'div', 'id':'content','class':None},  # based on current HTML
             {'name':'div','id':None,'class':'contentMain'},  # based on current HTML
             {'name': 'a', 'id': None, 'class': None}],  # needs updating when info becomes available
    'MZV' : [True,
            {'name':'div', 'id':None,'class':'article_list'},  # based on current HTML
             {'name':'div','id':None,'class':'article_content'},  # based on current HTML
             {'name': 'h2', 'id': None, 'class': 'article_title'},  # needs updating when info becomes available
             {'name': 'a', 'id': None, 'class': None}],  # needs updating when info becomes available
}

import json
minparameters = json.load(open('./bodiesdata.py'))

# Loop

# activedepts = ['MPO','MPSV','UV','MZd','MSMT','MF','MMR','MV','MZe','MK','MSp','MO','MD','MZV','CSSZ','FS','UP']
activedepts = ['MMR']

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

if len(cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='data';""").fetchall()) == 0:
    cursor.execute("""CREATE TABLE data
                        (jobtitle, joburl, dept, datetime timestamp)
                    """)
db.commit()
db.close()

db = litepiesql.Database('data.sqlite')
for row in jobsallbodies:
    db.insert('data',row)
    print(row)
