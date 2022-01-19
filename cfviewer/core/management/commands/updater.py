from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from django.db import connection

# User defined
from core.models import Contests, Problems

# Python library
import requests
import json
import tqdm
from multiprocessing import Pool
import time


def executeSQL(query, mapfn = None):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchall()
    
    if mapfn:
        row = map(mapfn, row)
    
    return row    

def update(contid):
    tsum = 0
    try:
        s = requests.get('https://codeforces.com/api/contest.standings?contestId={}&from=1&count=1'.format(contid)).json()
    except:
        print(f"Fetch for id {contid} failed")
    
    if s['status'] == "OK":
        for x in s['result']['problems']:
            tsum += x.get('rating',0)
    return tsum

def fetchcontests(self):
    '''
        @type: adminfunction;
        @returns: redirect to contests page;
        @description:
            This function fetches contests list from codeforces,
            parses it and if any contest has been added to the list,
            it adds the same into the database.
            Can be used only by admin or any staff member
        @errorhandling:
            If codeforces is unavailable or return status is not ok,
            it redirects to home page with corresponding error.
    '''
    try:
        r = requests.get('https://codeforces.com/api/contest.list?gym=false')
        jsond = r.json()
    except:
        self.stdout.write(self.style.ERROR('Codeforces unavailable'))

    if jsond['status'] == "OK":
        results = jsond['result']

        contids = set(executeSQL("SELECT contid FROM core_contests",lambda x : x[0]))

        for res in tqdm.tqdm(results):

            if res['id'] in contids:
                continue

            Contests.objects.create(
                contid = res['id'],
                name = res['name'],
                conttype = res['type'],
                duration = res['durationSeconds'],
                url = "codeforces.com/contest/{}".format(res['id']),
                difficulty = update(res['id'])
            )
        
        Contests.objects.filter(phase="BEFORE").delete()
        
        self.stdout.write(self.style.SUCCESS('Contests list Successfully updated'))
    else:
        self.stdout.write(self.style.ERROR('Status Not Ok'))

def fetchproblems(self):
    '''
        @type: adminfunction ;
        @return: redirect to problems page ;
        @description:
            This function fetches json from api call to codeforces problemset.
            Then parses it, if any new problem has been added on codeforces, 
            it will add the same to the database;
        @errorhandling:
            If codeforces is unavailable or status is not "OK",
            it returns redirect to home page with corressponding error;
    '''
    try:
        r = requests.get('https://codeforces.com/api/problemset.problems')
        json1 = r.json()
    except:
        self.stdout.write(self.style.ERROR('Codeforces unavailable'))
        return
    
    results = json1.get('result')
    problems = results['problems']
    problemsstats = results['problemStatistics']
    probnames = set(executeSQL("SELECT name FROM core_problems", lambda x : x[0]))
    
    for (x,y) in tqdm.tqdm(zip(problems,problemsstats)):
        # print("{} out of {}".format(i,len(problems)))
        if x['name'] in probnames:
            continue

        probnames.add(x['name'])
        prb = Problems()
        prb.name = x['name']
        prb.contestId = x['contestId']
        prb.index = x['index']
        try:
            prb.rating = x['rating']
        except:
            prb.rating = -1
        
        prb.tags = json.dumps(x['tags'])
        prb.userssolved = y['solvedCount']
        prb.save()

    self.stdout.write(self.style.SUCCESS('Problems list Successfully updated'))

class Command(BaseCommand):
    help = "Updates Problems List and Contests List"

    # @atomic()
    def handle(self, *args, **options):
        print("Adding Problems")
        fetchproblems(self)
        print("Adding Contests")
        fetchcontests(self)
    
