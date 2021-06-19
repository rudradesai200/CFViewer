from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic

# User defined
from core.models import Contests, Problems

# Python library
import requests
import json
import tqdm
from multiprocessing import Pool
import time

def update(cont):
    tsum = 0
    try:
        s = requests.get('https://codeforces.com/api/contest.standings?contestId={}&from=1&count=1'.format(cont.contid)).json()
    except:
        print(f"Fetch for id {cont.contid} failed")
        return cont
    
    if s['status'] == "OK":
        for x in s['result']['problems']:
            tsum += x.get('rating',0)
    cont.difficulty = tsum
    cont.save()
    return cont
        
def fetchfirst(self):
    try:
        r = requests.get('https://codeforces.com/api/contest.list?gym=false')
        jsond = r.json()
    except:
        self.stdout.write(self.style.ERROR('Codeforces unavailable'))
        return

    if jsond['status'] == "OK":
        results = jsond['result']
        i = 1
        for res in tqdm.tqdm(results):
            # print("Storing contest {} out of {}".format(i,len(results)))
            i += 1
            cont = Contests()
            cont.contid = res['id']
            cont.name = res['name']
            cont.phase = res['phase']
            cont.conttype = res['type']
            cont.duration = res['durationSeconds']
            cont.url = "codeforces.com/contest/{}".format(cont.contid)
            cont.difficulty = res.get('difficulty',1)
            cont.save()
        Contests.objects.filter(phase="BEFORE").delete()

        # with Pool(8) as p:
            # p.map(update, Contests.objects.all())
                
        maxdiff = 0
        for cont in tqdm.tqdm(Contests.objects.all()):
            cont = update(cont)
            maxdiff=max(cont.difficulty,maxdiff)

        for cont in tqdm.tqdm(Contests.objects.all()):    
            cont.difficulty = int((cont.difficulty*10.00)/maxdiff)
            cont.save()

        self.stdout.write(self.style.SUCCESS('Contests list Created Successfully'))
        # return redirect("/cfviewer/contests")
    else:
        self.stdout.write(self.style.ERROR('Status Not Ok'))
        # messages.error(request,"Status not ok")
        # return redirect("/cfviewer/")

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
        # messages.error(request,"Codeforces unavailable")
        self.stdout.write(self.style.ERROR('Codeforces unavailable'))
        # return redirect("/cfviewer/")

    if jsond['status'] == "OK":
        results = jsond['result']
        c = Contests.objects.all()
        Contests.objects.filter(phase="BEFORE").delete()
        obj = c.filter(difficulty=10)[0]
        maxdiff = 0
        s = requests.get('https://codeforces.com/api/contest.standings?contestId={}&from=1&count=1'.format(obj.contid)).json()
        if s['status'] == "OK":
            for x in s['result']['problems']:
                maxdiff += x.get('rating',0)

        else:
            self.stdout.write(self.style.ERROR('10 difficulty level object not found in DB'))
            # messages.error(request,"10 diff object not found")
            # return redirect("/cfviewer/")
        i = 1
        for res in tqdm.tqdm(results):
            # print("Storing contest {} out of {}".format(i,len(results)))
            i += 1
            if(len(c.filter(contid=res['id'])) != 0):
                break
            cont = Contests()
            cont.contid = res['id']
            cont.name = res['name']
            cont.phase = res['phase']
            cont.conttype = res['type']
            cont.duration = res['durationSeconds']
            cont.url = "codeforces.com/contest/{}".format(cont.contid)
            cont.difficulty = -1
            cont.save()
        Contests.objects.filter(phase="BEFORE").delete()

        conts = Contests.objects.filter(difficulty=-1)
        for cont in tqdm.tqdm(conts):
            cont = update(cont)
            cont.difficulty = int((cont.difficulty*10.00)/maxdiff)
            cont.save()
        
        self.stdout.write(self.style.SUCCESS('Contests list Successfully updated'))
        # return redirect("/cfviewer/contests")
    else:
        self.stdout.write(self.style.ERROR('Status Not Ok'))
        # messages.error(request,"Status not ok")
        # return redirect("/cfviewer/")

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
        # messages.error(request,"Codeforces unavailable")
        self.stdout.write(self.style.ERROR('Codeforces unavailable'))
        return
        # return redirect("/cfviewer/")
    
    results = json1.get('result')
    problems = results['problems']
    problemsstats = results['problemStatistics']
    p = Problems.objects.all()
    i = 1
    for (x,y) in tqdm.tqdm(zip(problems,problemsstats)):
        # print("{} out of {}".format(i,len(problems)))
        i += 1
        if(len(p.filter(name=x['name'])) != 0):
            break
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
    # return redirect("/cfviewer/problems")

class Command(BaseCommand):
    help = "Updates Problems List and Contests List"

    @atomic()
    def handle(self, *args, **options):
        if(len(Contests.objects.all()) > 0):
            fetchcontests(self)
        else:
            fetchfirst(self)
        fetchproblems(self)
    
