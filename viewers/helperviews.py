# Django Libraries
from django.shortcuts import render,redirect, HttpResponseRedirect
<<<<<<< HEAD
from django.http import JsonResponse
from django.contrib import messages
from core.models import Contests, Problems
=======
from django.contrib import messages
>>>>>>> fc6335a1eca36dc9a1435209dc5a0961955b6f84

# Python Libraries 
import requests
from collections import OrderedDict
import time
<<<<<<< HEAD
import random
import numpy
=======
>>>>>>> fc6335a1eca36dc9a1435209dc5a0961955b6f84

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
<<<<<<< HEAD
    return (user,m,mtag,msubs,prbcnt,ranklist,contids,days)

def suggestor_helper(request,slug, handle):
    '''
        @type: helperfunction ;
        @return: renders suggest pages for problems and contests ;
        @description:
            This page takes in an additional param slug, which decides
            problems or contests type of view. User info is taken and api calls are made
            to codeforces . returned objects are based on user ratings and submissions history.;
        @errorhandling:
            If slug is not 'problem' or 'contest' then redirects to home page 
            with error message. Else silent error handling. Supports anonymous views;
    '''

    if slug == "problem":
        user = userinfo(request,handle)
        try:
            ratingmax = min(user['maxRating'] + 300,3500)
        except:
            ratingmax = 1000
        try:
            ratingmin = max(min(user['maxRating'] - 100,3000),0)
        except:
            ratingmin = 500
        try:
            m,_,_,prbcnt,L = submissiongen(request,handle)
            rats = []
            prbnames = []
            for x in L:
                prbnames.append(x['problem']['name'])
                try:
                    rats.append(x['problem']['rating'])
                except:
                    pass
            rats = sorted(rats)
            valr = (4*prbcnt)/5
            temp = 0
            for x in m.keys():
                if (temp + m[x]) > valr:
                    ind = x
                    break
                else:
                    temp += m[x]
            
            maxindex=chr(min(ord(ind) + 1,ord("H")))
            minindex=ind
            # ratingmax = rats[-1]+100
            ratingmin = rats[int((4*len(rats))/5) - 1]
        except:
            user = userinfo(request,handle)
            prbnames = []
            minindex = "A"
            maxindex = "B"
        ratingmax = ratingmin + 500
        prbs = Problems.objects.filter(rating__gte=ratingmin,rating__lte=ratingmax,index__isnull=False,index__lte=maxindex,index__gte=minindex)
        for x in prbnames:
            prbs.exclude(name=x)
        prbs = list(prbs)
        random.shuffle(prbs)
        prbs = prbs[0:min(10,len(prbs))]
        context={"user":user,"prbs":prbs,"minindex":minindex,"maxindex":maxindex,"ratingmax":ratingmax,"ratingmin":ratingmin}
        return ("success",context)
    elif slug == "contest":
            user=userinfo(request,handle)
            try:
                _,contids,_ = ratingchange(request,handle)

                diffs = []
                for x in contids:
                    try:
                        diffs.append(Contests.objects.get(contid=x).difficulty)
                    except:
                        pass

                if len(diffs) != 0:
                    diffs = numpy.array(diffs)
                    mindiff = int(numpy.mean(diffs))
                    maxdiff = int(min(mindiff + 2,10))
                else:
                    mindiff = 0
                    maxdiff = 10
                if len(contids) != 0:
                    nids = set(contids)
                else:
                    nids = []
            except:
                contids = []
                mindiff = 0
                maxdiff = 10
                nids = []
            c = Contests.objects.filter(difficulty__gte=mindiff,difficulty__lte=maxdiff)
            for x in nids:
                try:
                    c.exclude(contid=x)
                except:
                    pass
            c = list(c)
            random.shuffle(c)
            c = c[:min(10,len(c))]
            context={"contests":c,"user":user,"mindiff":mindiff,"maxdiff":maxdiff}
            return ("success",context)

    errmsg = "URL error. Please try again"
    context={"msg":errmsg}
    return ("error",context)

def plugin_load(request,slug,handle):
    status, context = suggestor_helper(request,slug,handle)
    result = {}
    result['status'] = status
    if(status == "success"):
        if(slug == "problem"):
            result['minindex'] = context['minindex']
            result['maxindex'] = context['maxindex']
            result['ratingmin'] = context['ratingmin']
            result['ratingmax'] = context['ratingmax']
            for x in context['prbs']:
                result['url'] = "https://codeforces.com/contest/{}/problem/{}".format(x.contestId,x.index)
                break
        elif(slug == "contest"):
            result['mindiff'] = context['mindiff']
            result['maxdiff'] = context['maxdiff']
            for x in context['contests']:
                result['url'] = "https://" + x.url
                break
                    
    # print(result)
    return JsonResponse(result)
=======
    return (user,m,mtag,msubs,prbcnt,ranklist,contids,days)
>>>>>>> fc6335a1eca36dc9a1435209dc5a0961955b6f84
