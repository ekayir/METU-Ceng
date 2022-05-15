"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app import forms, views
from .models import Organizations
from django.contrib.auth.decorators import login_required

from service.userService import UserService
from service.organizationService import OrganizationService
from service.deviceService import DeviceService
from service.partService import PartService

from django.http import HttpResponse
import json
from django.core import serializers

import sys
import os
from socket import *
import asyncio
import websockets
import logging 
import http.cookies
from threading import Thread
from channels.generic.websocket import WebsocketConsumer
from app.consumers import ChatConsumer


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

_organizationService = OrganizationService()
_userService = UserService()
_deviceService = DeviceService()
_partService = PartService()


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })


def lobby(request):
    """Renders the contact page."""
    return render(request,
        'app/lobby.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })

@login_required
def organizations(request):
    organizations = _organizationService.getOrganizations(request.user.id)
    return HttpResponse(json.dumps({'result':'OK','organizations' : convertOrganizationToJson(organizations)}), 'text/json')

@login_required
def addOrganization(request):
    _organizationService.createNewOrganization(request.GET.get("organizationName",""), request.user.id)
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')

def loginCheck(request):

    if request.user == None or request.user.id == None or request.user.id == "":
        return HttpResponse(json.dumps({'isLogin':'False'}), 'text/json')
    
    return HttpResponse(json.dumps({'isLogin':'True', 'userId' :request.user.id}), 'text/json')

@login_required
def shareUnShareOrganization(request):
    organization_id = request.GET.get("organizationId","")
    type = request.GET.get("type","")
    if request.GET.get("submit","") == 'True':
        user_id = request.GET.get("selectedUserId","")
        
        if type == "1":#share
            _organizationService.shareOrganization(organization_id, user_id)
        else:
            _organizationService.unShareOrganization(organization_id, user_id)
        return HttpResponse(json.dumps({'result':'OK'}), 'text/json')
    else:
        if type == "1":
            users = _userService.getAllNotAuthUsers(request.user.id, organization_id)
            return HttpResponse(json.dumps({'result':'OK','users' : convertUserToJson(users), 'organizationId' : organization_id, 'type' : 1 }), 'text/json')
           
        else:
            users = _userService.getAllAuthUsers(request.user.id, organization_id)
            return HttpResponse(json.dumps({'result':'OK','users' : convertUserToJson(users), 'organizationId' : organization_id, 'type' : 2 }), 'text/json')
           

@login_required
def devices(request):
    if request.GET.get("isCatalog","") == "True":
        catalogDevices = _deviceService.getCatalogDevices()
        return HttpResponse(json.dumps({'result':'OK','devices' : convertDeviceToJson(catalogDevices)}), 'text/json')
    else:
        devices = _deviceService.getDevices(request.user.id, request.GET.get("organizationId",""))
        return HttpResponse(json.dumps({'result':'OK','devices' : convertDeviceToJson(devices)}), 'text/json')
@login_required
def addDevice(request):
    _deviceService.addDevice(request.GET.get("description",""),request.GET.get("organizationId",""),request.GET.get("catalogDeviceId",""))
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')

@login_required
def on(request):
    message = "OK"
    isOpenable = _deviceService.isOpenableDevice(request.GET.get("deviceId",""))
    if isOpenable:
        _deviceService.onDevice(request.GET.get("deviceId",""))
    else:
        message = "Selected device has zero time part or no parts. Please first remove zero part or add new part."        

    return HttpResponse(json.dumps({'result':message}), 'text/json')

@login_required
def off(request):
    _deviceService.offDevice(request.GET.get("deviceId",""))
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')


@login_required
def setNotificationTime(request):
    _userService.setNotificationLimit(request.user.id ,request.GET.get("notificationTimeLimit",""))
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')


@login_required
def attach(request):
    _organizationService.attachDetachOrganizationtion(1,request.GET.get("organizationId",""),request.user.id)
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')

@login_required
def detach(request):
    _organizationService.attachDetachOrganizationtion(0,request.GET.get("organizationId",""),request.user.id)
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')

@login_required
def notifications(request):
    onDeviceIds = _deviceService.getOnDeviceIds(request.user.id)
    
    for deviceId in onDeviceIds:
        _deviceService.offDevice(deviceId.DeviceId)
        _deviceService.onDevice(deviceId.DeviceId)

    notifications = _deviceService.getNotifications(request.user.id)
    return render(request, 'app/notifications.html', { 'notifications': notifications })

@login_required
def catalog(request):
    return redirect('/devices?isCatalog=True')

def convertPartToJson(parts):
    jsonParts = [{'Part_ProductNo':part.Part_ProductNo, 'Description':part.Description, 
                  'Type':part.Type, 'TotalLifeTime':part.TotalLifeTime, 
                  'ExpectedLifeTime':part.ExpectedLifeTime, 'Price':part.Price,
                  'Device_ProductNo':part.Device_ProductNo, "Id":part.Id, "DeviceId" : part.DeviceId}
		 for part in parts]
    return jsonParts

def convertDeviceToJson(devices):
    jsonDevices = [{'Id':device.Id , 'ProductNo':device.ProductNo , 'Type':device.Type , 'Description':device.Description , 'IsOn':device.IsOn }
		 for device in devices]
    return jsonDevices 

def convertOrganizationToJson(organizations):
    jsonOrganizations = [{'Id':organization.Id , 'Name':organization.Name , 'IsAttached':organization.IsAttached }
		 for organization in organizations]
    return jsonOrganizations

def convertUserToJson(users):
    jsonUsers = [{'Id':user.Id , 'Username':user.Username }
		 for user in users]
    return jsonUsers

@login_required
def parts(request):
    parts = _partService.getParts(request.GET.get("deviceId",""))

    return HttpResponse(json.dumps({'result':'OK','parts' : convertPartToJson(parts)}), 'text/json')
@login_required
def addPart(request):
    _partService.addPart(request.GET.get("deviceId",""),request.GET.get("productNo",""),request.GET.get("type",""),
                         request.GET.get("description",""),request.GET.get("totalLifeTime",""),request.GET.get("price",""))
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')


@login_required
def addDeviceToCatalog(request):
    _deviceService.addDeviceAndPartsToCatalog(request.GET.get("type",""),request.GET.get("productNo",""),request.GET.get("description",""),[])
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')

@login_required
def removePart(request):
    _partService.removePart(request.GET.get("partId",""))
    return HttpResponse(json.dumps({'result':'OK'}), 'text/json')


