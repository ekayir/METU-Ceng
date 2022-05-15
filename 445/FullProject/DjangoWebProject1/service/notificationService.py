from databaseQueries import *
import databaseUtility as dbUtility

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from service.deviceService import DeviceService
from service.partService import PartService

_deviceService = DeviceService()
_partService = PartService()

class NotificationService:

    def getNotificationJson(self):
        self.adjustNotification()

        _deviceService.setOffDevice()

        data = self.getNotificationsV2()

        convertedData = self.convertNotificationDataToJson(data)

        parts = _partService.getAllParts()
        convertedPartData = self.convertPartToJson(parts)

        

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('test', {'type':'chat_message','message':{'notifications':convertedData,'partsData':convertedPartData}})
        #async_to_sync(channel_layer.group_send)('test', {'type':'chat_message','partsData':convertedPartData})

    

    def convertPartToJson(self,parts):
        jsonParts = [{'Part_ProductNo':part.Part_ProductNo, 'Description':part.Description, 
                      'Type':part.Type, 'TotalLifeTime':part.TotalLifeTime, 
                      'ExpectedLifeTime':part.ExpectedLifeTime, 'Price':part.Price,
                      'Device_ProductNo':part.Device_ProductNo, "Id":part.Id, "DeviceId" : part.DeviceId}
		     for part in parts]
        return jsonParts

    def convertNotificationDataToJson(self,data):
        jsonData = [{'UserId':d.UserId , 'OrganizationName':d.OrganizationName , 'DeviceProductNo':d.DeviceProductNo, 'PartProductNo':d.PartProductNo, 'ExpectedLifeTime':d.ExpectedLifeTime}
		     for d in data]
        return jsonData

    def adjustNotification(self):
        onDeviceIds = self.getOnDeviceIds()
    
        for deviceId in onDeviceIds:
            _deviceService.offDevice(deviceId.DeviceId)
            _deviceService.onDevice(deviceId.DeviceId)

    def getOnDeviceIds(self):
        try:
            return dbUtility.fetchAll(QUERY_GET_ALL_ON_DEVICE_IDS)
        except :
            return None

    def getNotificationsV2(self):
        try:
            return dbUtility.fetchAll(QUERY_GET_NOTIFICATIONS_V2)
        except :
            return None