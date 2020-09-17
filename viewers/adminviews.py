# Django Libraries
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

# User defined
from core.models import Contests, Problems

# Python library
import requests
import json

# @staff_member_required
# def acceptinvite(request,handle,stat):
#     inv = Invitees.objects.filter(cfhandle=handle)
#     if len(inv) == 0:
#         messages.error(request,"Handle not in db")
#         return redirect("/cfviewer/invite/{}/".format(handle))
#     else:
#         inv[0].status = stat
#         inv[0].save()
#         messages.success(request,"User found and status changed")
#         return redirect("/cfviewer/invite/{}/".format(handle))

