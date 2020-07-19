# Django Libraries
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib import messages

# User Defined
from core.models import Contests, Problems, Invitees
from core.forms import ProblemFilterForm, InviteForm
from core.viewers.helperviews import *

#Python Libraries
import random
import json
import requests
from collections import OrderedDict

def dashboard(request):
    '''
        @type: renderfunction ;
        @return: renders dashboards page ;
        @description:
            Calls helper functions and provides data for chart display on 
            dashboards page.;
        @errorhandling:
            Silent error handling. Supports anonymous views;
    '''
    try:
        handle = request.GET['handle']
        user,m,mtag,msubs,prbcnt,ranklist,_,days  = getcharts(request,handle)    
    except: 
        messages.error(request,"Please enter a handle to view dashboard")
        m={}
        user=None
        mtag={}
        msubs={}
        prbcnt=0
        ranklist={}
        days = []
    return render(request,"dashboard.html",context={
        "user":user,
        "ProbCat":m,
        "ProbTags":mtag,
        "SubsInfo":msubs,
        "probsolved":prbcnt,
        "contcount":len(ranklist),
        "ranklist":ranklist,
        "days":days
        })

def contests(request):
    '''
        @type: renderfunction ;
        @return: renders contests page ;
        @description:
            This page collects userinfo and Contests from dataset,
            then handles api call to codeforces user status,
            and returns contests for particular user;
        @errorhandling:
            Silent error handling,
            no error message given, substitutes guest everywhere.
            Supports anonymous views also;
    '''
    try:
        handle = request.GET['handle']
    except:
        handle = ""

    user = userinfo(request,handle)

    ress = Contests.objects.all()
    subs = requests.get('https://codeforces.com/api/user.status?handle={}'.format(handle)).json()
    if subs['status'] != "OK":
        subs['result'] = []
    
    nids = []
    
    for x in subs['result']:
        try:
            nids.append(x['contestId'])
        except:
            pass

    nids = set(nids)
    subs = []
    for x in ress:
        if x.contid in nids:
            subs.append(1)
        else:
            subs.append(0)
            
    ress = zip(ress,subs)

    return render(request, 'contests.html', {'ress':ress,'user':user})

def problems(request):
    '''
        @type: renderfunction ;
        @return: renders problems page ;
        @description:
            calls userinfo and codeforces user status api
            handles POST data of filterform on problems page.
            By default returns problems from difficulty of 
            [(maxRating+300),(maxrating-100)];
        @errorhandling:
            silent error handling.
            Supports anonymous views also;
    '''
    try:
        handle = request.GET['handle']
    except:
        handle = ""

    user = userinfo(request,handle)
    
    solved = []
    unsolved = []
    
    try:
        subs = requests.get('https://codeforces.com/api/user.status?handle={}'.format(handle)).json()['result']
    except:
        subs = []
    for x in subs:
        if x['verdict'] == "OK":
            solved.append(x['problem']['name'])
        else:
            unsolved.append(x['problem']['name'])
    prbs = []
    index = None
    try:
        ratingmax = min(user['maxRating'] + 300,3500)
    except:
        ratingmax = 1000
    try:
        ratingmin = max(min(user['maxRating'] - 100,3000),0)
    except:
        ratingmin = 0
    show_tags = False
    taglist = None
    filterform = ProblemFilterForm()
    if request.method == "POST":
        filterform = ProblemFilterForm(request.POST)
        if filterform.is_valid():
            index = filterform.cleaned_data.get('category')
            ratingmin = filterform.cleaned_data.get('ratingmin')
            ratingmax = filterform.cleaned_data.get('ratingmax')
            tags = filterform.cleaned_data.get('tags')
            taglist = tags.split(',')
            show_tags = filterform.cleaned_data.get('show_tags')
        else:
            print(filterform.errors)
            messages.error(request,"Invalid values provided")
            # return redirect("/cfviewer/")
    

    if (ratingmax == None) and (ratingmin == None):
        try:
            ratingmax = min(user['maxRating'] + 300,3500)
        except:
            ratingmax = 1000
        try:
            ratingmin = max(min(user['maxRating'] - 100,3000),0)
        except:
            ratingmin = 0
    else:
        if(ratingmax == None):
            ratingmax = 3800
        if(ratingmin == None):
            ratingmin = 0

    problems = Problems.objects.filter(rating__lte=ratingmax,rating__gte=ratingmin,index__isnull=False)
    if(index)and(index!="None"):
        problems = problems.filter(index__startswith=index)
    if not ((taglist == None) or (taglist[0] == '')):
        for b in taglist:
            problems =problems.filter(tags__contains=str(b.strip()))
            
    prbs = problems
    final = []
    color = []
    types = []
    for x in problems:
        if x.name in solved:
            color.append("#a8eabe")
            types.append("solved")
        elif x.name in unsolved:
            color.append('#ff9292')
            types.append("wrong")
        else:
            color.append("white")
            types.append("unsolved")
        final.append(x)
    prbs = zip(final,color,types)
    print(show_tags)
    return render(request,"problems.html",context={"problems":prbs,'filterform':filterform,'user':user,'show_tags':show_tags})

def friendsunsolved(request):
    '''
        @type: renderfunction ;
        @return: renders friends page ;
        @description:
            calls userinfo for the viewer, also 3 api calls to codeforces for user and friends status.
            It gives color to submissions which are solved/unsolved by user accordingly ;
        @errorhandling:
            Silent error handling. Supports anonymous views.
            No messages given;
    '''
    try:
        handle = request.GET['handle']
    except:
        handle =""

    if handle == "":
        messages.error(request,"Please enter your handle to continue")
        return redirect("/cfviewer/")

    user = userinfo(request,handle)
    try:
        x = user['firstName']
    except:
        x = user['handle']
    if x == "Guest":
        messages.error(request,"You need to login in before comparing")
        return redirect("/cfviewer/") 
    
    friend = request.GET['friend']
    friendinf = requests.get('https://codeforces.com/api/user.info?handles={}'.format(friend)).json()
    if(friendinf['status'] == "OK"):
        user,m,mtag,_,prbcnt,ranklist,_,_  = getcharts(request,handle)
        fuser,fm,fmtag,_,fprbcnt,franklist,_,_ = getcharts(request,friend)

        Probcat = {}
        for x,y in m.items():
            Probcat[x] = [y]
        for x,y in fm.items():
            Probcat[x].append(y)
        
        ProbTags = {}
        for x in mtag:
            ProbTags[x] = [0,0]
        for x in fmtag:
            ProbTags[x] = [0,0]
        for x,y in mtag.items():
            ProbTags[x][0] = y
        for x,y in fmtag.items():
            ProbTags[x][1] = y
        
        try:
            user['minRating'] =  min(ranklist)
            fuser['minRating'] = min(franklist)
        except:
            pass
        # ranklist = {}
        days = {}
        fdays = {}
        # ranklist = OrderedDict()
        # for x,y in days.items():
        #     # print(x)
        #     ranklist[x] = [0,0]
        # for x,y in fdays.items():
        #     ranklist[x] = [0,0]
        # prev1 = 0
        # for x,y in ranklist.items():
        #     if x in days:
        #         ranklist[x][0] = days[x]
        #         prev1 = days[x]
        #     else:
        #         ranklist[x][0] = prev1
        # prev2 = 0
        # for x in ranklist:
        #     if x in fdays:
        #         ranklist[x][1] = fdays[x]
        #         prev2 = fdays[x]
        #     else:
        #         ranklist[x][1] = prev2
        # contextdict = {"user":user,"m":m,"mtag":mtag,"msubs":msubs,"prbcnt":prbcnt,"ranklist":ranklist,"fuser":fuser,"fm":fm,"fmtag":fmtag,"fmsubs":fmsubs,"fprbcnt":fprbcnt,"franklist":franklist}
        contextdict = {
            "user":user,
            "fuser":fuser,
            "Probcat":Probcat,
            "ProbTags":ProbTags,
            "ranklist":ranklist,
            "probsolved":prbcnt,
            "fprobsolved":fprbcnt,
            "contcount":len(ranklist),
            "fcontcount":len(franklist)
        }
        # comp = zip(s1,s2)

        mysubs = requests.get('https://codeforces.com/api/user.status?handle={}'.format(handle)).json()['result']
        friendssubs = requests.get('https://codeforces.com/api/user.status?handle={}'.format(friend)).json()['result']
        
        # Creating a dictionary with friends unsolved problems
        friendsunsolved = {}
        for x in friendssubs:
            if(x['verdict'] != "OK"):
                friendsunsolved[x['problem']['name']] = x
        for x in friendssubs:
            if(x['verdict'] == "OK"):
                if(x['problem']['name'] in friendsunsolved):
                    friendsunsolved.pop(x['problem']['name'])
        
        # Creating my solutions dictionary to give color
        mysols = {}
        for x in mysubs:
            if(x['verdict']!="OK"):
                mysols[x['problem']['name']] = x
        for x in mysubs:
            if(x['verdict']=="OK"):
                mysols[x['problem']['name']] = x

        unsolved = 0
        for x in mysols:
            if(mysols[x]['verdict'] != "OK"):
                unsolved += 1

        substogo = []
        color = []
        types = []
        
        for x,y in friendsunsolved.items():
            if x in mysols:
                if mysols[x]['verdict'] == "OK":
                    color.append("#a8eabe")
                    types.append("solved")
                else:
                    color.append("#ff9292")
                    types.append("wrong")
            else:
                color.append("white")
                types.append("unsolved")
            substogo.append(y)
        
        substogo = zip(substogo,color,types)
        contextdict["user"]=user
        contextdict["subs"]=substogo
        contextdict["friend"]=friend
        contextdict["unsolved"] = unsolved
        contextdict["funsolved"] = len(friendsunsolved)

        return render(request,"friends.html",context=contextdict)
    else:    
        messages.error(request,"{} Handle not found".format(friend))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def suggestor(request,slug):
    '''
        @type: renderfunction ;
        @return: renders suggest pages for problems and contests ;
        @description:
            This page takes in an additional param slug, which decides
            problems or contests type of view. User info is taken and api calls are made
            to codeforces . returned objects are based on user ratings and submissions history.;
        @errorhandling:
            If slug is not 'problem' or 'contest' then redirects to home page 
            with error message. Else silent error handling. Supports anonymous views;
    '''
    try:
        handle = request.GET['handle']
    except:
        handle=""

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
        return render(request,"suggestprobs.html",context={"user":user,"prbs":prbs,"minindex":minindex,"maxindex":maxindex,"ratingmax":ratingmax,"ratingmin":ratingmin})
    else:
        if slug == "contest":
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
            return render(request,"suggestconts.html",context={"contests":c,"user":user,"mindiff":mindiff,"maxdiff":maxdiff})
        else:
            messages.error(request,"URL error. Please try again")
            return redirect("/cfviewer/")

def submissionsviewer(request,handle,contid):  
    '''
        @type: renderfunction ;
        @return: renders submissions page for contests ;
        @description:
            Takes in handle and contestid, and provides color coded 
            submissions for viewing along with links;
        @errorhandling:
            If codeforces unavailable or status not ok, provides error message
            and redirects to http_referer;
    '''
    user = userinfo(request,handle)
    try:  
        subs = requests.get('https://codeforces.com/api/user.status?handle={}'.format(handle)).json()
    except:
        messages.error(request,"Codeforces unavailable. Please try again later")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if subs['status'] != "OK":
        messages.error(request,"Handle not found. Please provide a proper handle")
        return redirect("/cfviewer/")
    
    nids = []
    for x in subs['result']:
        try:
            if str(x['contestId']) == contid:
                nids.append(x)
        except:
            pass

    return render(request,"submissions.html",context={"handle":handle,"contest":contid,'subs':nids,"user":user})

def foobarinvite(request,handle):
    '''
        @type: render function ;
        @return: render view ;
        @description:
            It is made for foobar invite form acceptance; 
        @errorhandling:
            ;
    '''
    user = userinfo(request,handle)
    if len(Invitees.objects.filter(cfhandle = handle)) == 0:
        inviteform = InviteForm()
    else:
        inviteform = None
    currlist = Invitees.objects.all().order_by("id")
    if request.method == "POST":
        inviteform = InviteForm(request.POST)
        if inviteform.is_valid():
            cfhandle = inviteform.cleaned_data.get("cfhandle")
            if(cfhandle != handle):
                messages.error(request,"You cannot invite other users. You can only add your handle to the list")
                return render(request,"invites.html",context={"user":user,"inviteform":inviteform,"currlist":currlist})

            if(len(Invitees.objects.filter(cfhandle = cfhandle)) != 0):
                messages.error(request,"You are already there on the list")
                return render(request,"invites.html",context={"user":user,"inviteform":inviteform,"currlist":currlist})
            
            r = requests.get('https://codeforces.com/api/user.info?handles={}'.format(cfhandle)).json()
            if(r['status']!="OK"):
                messages.error(request,"User not found. Please try again")
                return render(request,"invites.html",context={"user":user,"inviteform":inviteform,"currlist":currlist})
            if(r['result'][0]['rating'] < 1500):
                messages.error(request,"Your rating needs to be atleast 1500 for getting an invite")
                return render(request,"invites.html",context={"user":user,"inviteform":inviteform,"currlist":currlist})
            inv = inviteform.save(commit=True)
            inv.status = 0
            inv.save()
            messages.success(request,"Added to list")
        else:
            print(inviteform.errors)
            messages.error(request,"Data invalid.Please try again")
            return render(request,"invites.html",context={"user":user,"inviteform":inviteform,"currlist":currlist})
    
    if len(Invitees.objects.filter(cfhandle = handle)) == 0:
        inviteform = InviteForm()
    else:
        inviteform = None
    currlist = Invitees.objects.all().order_by("id")
    return render(request,"invites.html",context={
        "user":user,
        "inviteform":inviteform,
        "currlist":currlist,
    })