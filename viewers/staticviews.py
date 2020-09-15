# Django Libraries
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib import messages

# User defines
from core.viewers.helperviews import userinfo

def home(request):
    '''
        @type: StaticPageRender ;
        @return:  renders homepage;
        @description:
            Simple page render for home page;
        @errorhandling:
            None ;
    '''
    return render(request,"home.html",context=None)

def showbooks(request):
    '''
        @type: StaticRenderFunction ;
        @return: renders books page ;
        @description:
            Simple rendering of books;
        @errorhandling:
            Silent. Supports anonymous view;
    '''
    try:
        handle = request.GET['handle']
    except:
        handle=""
    
    user = userinfo(request,handle)
    
    return render(request,"books.html",context={"user":user})

def error_404_view(request, exception):
    '''
        @type: PagenotFoundrender ;
        @return: 404 page ;
        @description:
            Simple rendering of 404 not found page;
        @errorhandling:
            None.;
    '''
    # messages.error(request,exception)
    return render(request,"404.html",context=None)


# def adspage(request):
#     '''
#         @type: staticpagerender ;
#         @return: renders page ;
#         @description:
#             A page which shows different types of ads;
#         @errorhandling:
#             ;
#     '''
#     try:
#         handle = request.GET['handle']
#     except:
#         handle =""
    
#     user = userinfo(request,handle)
#     messages.success(request,"Thanks for clicking on this button. Now you will see an ads page. Please read the information before clicking anywhere.")
#     return render(request,"adspage.html",context={"user":user})