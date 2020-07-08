from core.models import *
from core.viewers.renderviews import *
from core.viewers.helperviews import *

from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

import requests
import string
import datetime


    
def setpassword(request,handle,token):
    '''
        @type:  Render function;\n
        @return:  HTML page;\n
        @description:\n
            Sets password for User's account using the link sent in email;
        @errorhandling:\n
            Checks for various conflicts;
    '''
    # Checks if handle is present
    if handle == "":
        messages.error(request,"Please enter your handle to continue")
        return redirect("/cfviewer/")

    # user is a query set here
    user = User.objects.filter(username=handle)
    if len(user) == 0:
        # User not registered as no User object has been created
        messages.error(request,"No tokens found for this username")
        return redirect(f"/cfviewer/dashboard/?handle={handle}")
    else:
        # User registered
        # If user exists , proxy object also must exists because of register function
        proxy = Coderproxy.objects.get(username=handle)

        if proxy.register_token == token:
            # Valid token and user
            user = user[0]

            if request.method == "POST":
                # Password form handling
                form = SetPasswordForm(user,request.POST)
                
                if form.is_valid():
                    # Delete proxy, as it was for one-time use only
                    proxy.delete()
                    user = form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request,"Registration successfull. Please login to continue.")
                    return redirect(f"/cfviewer/pvplogin/{handle}/")
                
                else:
                    # Dont delete proxy, because the form will be resubmitted
                    messages.error(request,"Please follow the suggested guidelines for password")
            
            # Render page along with user and form
            form = SetPasswordForm(user)
            return render(request,"setpassword.html",context={"user":userinfo(request,handle),"form":form})
        
        else:
            # Invalid token
            messages.error(request,"Incorrect token provided")
            return redirect(f"/cfviewer/dashboard/?handle={handle}")

def pvplogin(request,handle):
    '''
        @type: Render function ;\n
        @return:  HTML Page;\n
        @description:\n
            Renders the login page and call registration if required;
        @errorhandling:\n
            Yes;
    '''
    # Checks if handle is present in the request
    if handle == "":
        messages.error(request,"Please enter your handle to continue")
        return redirect("/cfviewer/")
    
    # user is a query set here
    user = User.objects.filter(username=handle)

    if len(user) == 0:
        # User not registered. Send email with set password link
        messages.error(request,"You are not registered with us.\\nA link will be sent on your email-id registered with Codeforces.\\n\\nNOTE: MAKE SURE YOU HAVE CONTACT SHARING VISIBILITY TURNED ON IN CODEFORCES SETTINGS.")
        return pvpregistration(request,handle)

    else:
        # User already registered

        if request.method == "POST":
            # Login form request handling

            password = request.POST.get('password')
            user = authenticate(username=handle, password=password)

            if user is not None:
                # Authenticated User
                login(request, user)
                messages.success(request,"You are now logged in")
                return redirect(f"/cfviewer/pvpinvite/{handle}/")

            else:
                # User not registered, or something's wrong
                messages.error(request,"You are not registered with us. A link will be sent on your email-id registered with Codeforces.\\n\\nNOTE: MAKE SURE YOU HAVE CONTACT SHARING VISIBILITY TURNED ON IN CODEFORCES SETTINGS.")
                return pvpregistration(request,handle)
        
        else:
            # Login Page rendering 
            return render(request,"pvplogin.html",context={"user":userinfo(request,handle)})

def pvpregistration(request,handle):
    '''
        @type: Render function ;\n
        @return:  redirects to other pages;\n
        @description:\n
            Checks if handle exists on CF
            Creates a coder-proxy object and
            Sends an email to the coder;
        @errorhandling:\n
            Yes;
    '''
    
    # Checks if handle is present on codeforces or not
    try:
        r = requests.get('https://codeforces.com/api/user.info?handles={}'.format(handle)).json()
    except:
        # No response from cf server
        messages.error(request,"Codeforces unavailable")
    else:
        # Response status 200
        if r['status'] == "OK":
            res = r['result'][0]

            # Checks if email is visible in public on codeforces.
            emailid = ""
            try:
                emailid = res['email']
            except:
                messages.error(request,"Please change your email visibility to public in your codeforces account.\\nIt helps us to verify that you yourself are trying to register on our platform. You can change it later.\\nPlease try again, after turning it on.")
                return redirect(f"/cfviewer/dashboard/?handle={handle}")
            
            # Create a token, User and a proxy object to analyse usage afterwards
            token = createRandomToken(request)
            user = User(username=handle,email=emailid)
            user.save()
            proxy = Coderproxy(username=handle,register_token=token,email=emailid,time_registered=now())
            proxy.save()

            # Send email to the obtained email id
            message = f"Hello {handle},\\nThanks for participating!.\\n\\nPlease click on this link to continue.\\n NOTE: This is a one-time valid link only. \\n\\n Link : http://www.rudradesai.in/cfviewer/setpassword/{handle}/{token}/"
            subject = "Registration for PvP battle on Codeforces"
            status = emailsend(request,emailid,message,subject)
            
            if status:
                # Mail sent successfully
                # if debug=True, this mail can be seen in terminal
                messages.success(request,f"Login details has been sent on {emailid}")
                return redirect(f"/cfviewer/pvplogin/{handle}/")
            else:
                # Depends on many reason
                messages.error(request,"Something went wrong. Please contact admin.")
        
        else:
            # Error reported by CF server
            messages.error(request,request['comment'])
    
    # Error case redirecting
    return redirect(f"/cfviewer/dashboard/?handle={handle}")

def pvpinvite(request,handle):
    '''
        @type: Render function ;\n
        @return: Rendering page ;\n
        @description:\n
            Lists all the invites received and sent
            Also, handles new invite send request
            Checks if friend is already registered or not;
        @errorhandling:\n
            Yes;
    '''

    # Many chances of user directly accessing this page
    # So, if user not authenticated, redirect to login page
    # Rest all will be handled there
    if not request.user.is_authenticated:
        messages.error(request,"Please login to continue")
        return redirect(f"/cfviewer/pvplogin/{handle}/")
    
    # Checks if the handle obtained and the authenticated user are same
    user = request.user
    if not handle == user.username:
        logout(request)
        messages.error(request,"Please login to continue")
        return redirect(f"/cfviewer/pvplogin/{handle}/")

    # Handles New invite send request
    if request.method == "POST":

        # Check if friend is registered with our platform
        friend = request.POST.get('friend')
        friend_coder = User.objects.filter(username=friend)

        if len(friend_coder) == 0:
            # No such handles found , so not registered
            link = f"http://www.rudradesai.in/cfviewer/pvplogin/{friend}/"
            messages.error(request,f"{friend} has not registered yet.\\nPlease ask {friend} to register first.\\nYou can share this link : {link}\\n\\nYou can try again later.")
            return redirect(f"/cfviewer/pvpinvite/{handle}/")
        
        else:
            # Friend registered, so send an email

            # Email sending
            emailid = friend_coder[0].email
            token = createRandomToken(request)
            message = f"Hello {friend},\\nYour friend {handle} has invited you for a battle. Go to this link to accept the invitation.\\n\\nLink: htt[://www.rudradesai.in/cfviewer/acceptinvite/{friend}/{token}/"
            subject = "Battle inviation by "+handle
            status = emailsend(request,emailid,message,subject)
            
            # Creating an invite object for further check
            inv = Pvpinvite(host=handle,invitee=friend,time=now(),token=token)
            inv.save()

            # Checking if email was successfull
            if status:
                messages.success(request,"An email has been sent on your friend's email id associated with Codeforces. You will be able to start the battle once your friend accepts the invitation.")
                return redirect(f"/cfviewer/pvpbattle/{handle}/{token}/")
            else:
                messages.error(request,"Something went wrong. Please contact admin.")

    context_dict = {
        "user":userinfo(request,handle),
        "received":Pvpinvite.objects.filter(invitee=handle),
        "sent":Pvpinvite.objects.filter(host=handle),
    }

    # Invite Page rendering
    return render(request,"pvpinvite.html",context=context_dict)

def acceptinvite(request,handle,token):
    '''
        @type: Helper function ;\n
        @return:  Redirects to other pages;\n
        @description:\n
            Handles the sent link for battle invites
            Checks if the link and user is legitimate
            Redirects to battle page;
        @errorhandling:\n
            Yes;
    '''

    # Checking if user is present on platform or not
    coder = User.objects.filter(username=handle)

    if len(coder) == 0:
        # Not present, redirect to register
        messages.error(request,"You have not registered, please register to continue.")
        return redirect(f"/cfviewer/pvplogin/{handle}/")

    else:
        # Present, check for the invite and token
        invite = Pvpinvite.objects.filter(invitee=handle,token=token)

        if len(invite) == 0:
            # No such invites , redirect to invites page for all invites
            messages.error(request,"No such invites exist.")
            return redirect(f"/cfviewer/pvplogin/{handle}/")  

        else:
            # Invite found , change the status to accepted and redirect to the battle page
            invite[0].status = "accepted"
            invite[0].save()
            messages.success(request,"Invite has been accepted. A contest will be created in a few minutes.")
            return redirect(f"/cfviewer/pvpbattle/{handle}/{token}/")
       
def pvpbattle(request,handle,token):
    '''
        @type: Render function ;\n
        @return:  Render page;\n
        @description:\n
            Yet to be implemented;
        @errorhandling:\n
            Yes;
    '''
    if handle == "":
        messages.error(request,"Please enter your handle to continue")
        return redirect("/cfviewer/")
    
    user = User.objects.filter(username=handle)
    if len(user) == 0:
        messages.error(request,"Please register to continue")
        return redirect(f"/cfviewer/pvplogin/{handle}/")
    
    context_dict = {
        "user":userinfo(request,handle),
        "token":token,
    }
    return render(request,"pvpbattle.html",context=context_dict)