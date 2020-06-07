# Django Libraries
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib import messages

# Python Libraries 
import requests
from collections import OrderedDict
import time

def userinfo(request,handle):
    '''
        @type: Helper function;
        @returns: user objects;
        @description:
            If codeforces is not available or if return status of user is not ok, then
            it will return an guest user object.;
        @errorhandling:
            Because of anonymous link, it wont give any error if handle is not found.
            Error needs to be taken care in callee function;
    '''
    try:
        # print(handle)
        r = requests.get('https://codeforces.com/api/user.info?handles={}'.format(handle)).json()
    except:
        messages.error(request,"Codeforces unavailabe")
        return {"firstName":"Guest","handle":"Guest","maxRating":0,"minRating":0,"titlePhoto":"/static/assets/images/users/d3.jpg"}
    else:
        # print("good")
        if r['status'] == "OK":
            res = r['result'][0]
            x = ""
            try:
                x = res['firstName']
            except:
                res['firstName'] = res['handle']
            return res
        else:
            return {"firstName":"Guest","maxRating":0,"minRating":0,"handle":"Guest","titlePhoto":"/static/assets/images/users/d3.jpg"}

def ratingchange(request,handle):
    '''
        @type: Helper function;
        @return: ranklist, contestids;
        @description:
            This function parses rating change objects for the given handle,
            and returns ranklist(sorted) and contestids list.
        @errorhandling
            If codeforces is unavailable or handle not found ,
            it returns two empty lists;
    '''
    try:
        r = requests.get('https://codeforces.com/api/user.rating?handle={}'.format(handle)).json()
    except:
        return [],[],[]
    else:
        if r['status'] == "OK":
            res = r['result']
            ranks = []
            contids = []
            days = OrderedDict()
            for x in res:
                contids.append(x['contestId'])
                ranks.append(x['newRating'])
                a = str(time.strftime("%y/%m/%d",time.localtime(int(x['ratingUpdateTimeSeconds']))))
                days[a] = x['newRating']
            # sorted(ranks)
            return ranks,contids,days
        else:
            return [],[],[]

def submissiongen(request,handle):
    '''
        @type: Helper function;
        @return: categorymap, tagsmap, verdictmap, problemscount, correctsubmisisons;
        @description:
            this function parses status api call of codeforces, and evaluates
            categorymap -       Map of problem category to number of problems solved
            tagsmap -           Map of problem tags to number of problems soved
            verdictmap -        Map of problem verdicts to number of problems solved
            problemscount -     number of "OK" verdict
            correctsubmissions -List of "OK" verdict submissions;
        @errorhandling:
            if codeforces is unavailable or return status is not "OK",
            it returns 3 empty dictionaries, zero value, and an empty list;
    '''
    try:
        r = requests.get('https://codeforces.com/api/user.status?handle={}&from=1'.format(handle)).json()
    except:
        return ({},{},{},0,[])
    if r['status'] == 'OK':
        res = r['result']
        L = []
        prbcnt = 0
        m = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0}
        mt = {}
        ms = {
            "FAILED":0,
            "OK":0,
            "PARTIAL":0,
            "COMPILATION_ERROR":0,
            "RUNTIME_ERROR":0,
            "WRONG_ANSWER":0,
            "PRESENTATION_ERROR":0,
            "TIME_LIMIT_EXCEEDED":0,
            "MEMORY_LIMIT_EXCEEDED":0,
            "IDLENESS_LIMIT_EXCEEDED":0,
            "SECURITY_VIOLATED":0,
            "CRASHED":0,
            "INPUT_PREPARATION_CRASHED":0,
            "CHALLENGED":0,
            "SKIPPED":0,
            "TESTING":0,
            "REJECTED":0
        }
        # Storing problems with OK verdict
        probnames = set()
        for x in res:
            if x['problem']['name'] not in probnames:
                if x['verdict'] == "OK":
                    L.append(x)
                probnames.add(x['problem']['name'])
            ms[x['verdict']] += 1
                
        # L = set(L)
        for x in L:
            try:
                m[x['problem']['index'][0]] += 1
                for y in x['problem']['tags']:
                    try:
                        mt[y] += 1
                    except:
                        mt[y] = 1
            except:
                pass
        
        prbcnt = len(L)

        return m,mt,ms,prbcnt,L
    else:
        return ({},{},{},0,[])

def getcharts(request,handle):
    user = userinfo(request,handle)
    m,mtag,msubs,prbcnt,_ = submissiongen(request,handle)
    ranklist,contids,days = ratingchange(request,handle)
    return (user,m,mtag,msubs,prbcnt,ranklist,contids,days)