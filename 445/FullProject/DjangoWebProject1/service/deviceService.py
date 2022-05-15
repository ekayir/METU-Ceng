from databaseQueries import *
import databaseUtility as dbUtility
from service.idGeneratorService import IdGeneratorService
class DeviceService:

    def addDevice(self, description: str, organization_id: str, catalogue_device_id: str):
        try:
            _idGeneratorService = IdGeneratorService()
            device_id = _idGeneratorService.getNewId()
            commands = []
            commands.append(QUERY_DEVICE_INSERT.format(device_id,description, description, organization_id,catalogue_device_id))
            commands.append(QUERY_PART_INSERT_VIA_CATALOG_DEVICE.format(device_id,catalogue_device_id))
            return dbUtility.executeStatements(commands)
        except :
            return False

    def getDevices(self, user_id: int, organization_id: str):
        try:
            return dbUtility.fetchAll(QUERY_DEVICE_LIST_FILTER_BY_USER_ID.format(user_id, organization_id))
        except :
            return []

    def getCatalogDeviceId(self, product_no: str):
        try:
            return dbUtility.fetchOne(QUERY_GET_CATALOG_DEVICE_ID_FILTER_BY_PRODUCT_NO.format(product_no))
        except :
            return None

    def getCatalogDevices(self):
        try:
            return dbUtility.fetchAll(QUERY_GET_CATALOG_DEVICES)
        except :
            return None

    def getDeviceId(self, device_id: str):
        try:
            return dbUtility.fetchOne(QUERY_DEVICES_FILTER_BY_ID.format(device_id))
        except :
            return None

    def onDevice(self, device_id: str):
        try:
            return dbUtility.executeStatement(QUERY_DEVICES_SET_ON.format(device_id))
        except :
            return False

    def isOpenableDevice(self, device_id: str):
        try:
            count = dbUtility.fetchOne(QUERY_IS_OPENABLE_DEVICE.format(device_id))
            parts = dbUtility.fetchAll(QUERY_PART_GET_PART_LIST_OF_DEVICES.format(device_id))
            return (count[0] == 0 and parts != [])
        except :
            return False

    def offDevice(self, device_id: str):
        try:
            commands = []
            commands.append(OUERY_DEVICES_SET_OFF_UPDATE_TIME.format(device_id,device_id))
            commands.append(QUERY_DEVICES_SET_OFF.format(device_id))
            return dbUtility.executeStatements(commands)
        except :
            return False

    def addDeviceAndPartsToCatalog(self, type: str, product_no: str, description:str, parts):
        try:
            _idGeneratorService = IdGeneratorService()
            device_id = _idGeneratorService.getNewId()
            commands = []
            commands.append(QUERY_ADD_DEVICE_TO_CATALOG.format(device_id,type,description, product_no))
            for part in parts:
                commands.append(OUERY_ADD_PART_TO_CATALOG_DEVICE.format(_idGeneratorService.getNewId(),device_id,part[0],part[1],part[2],part[3],part[3],part[4]))
            return dbUtility.executeStatements(commands)
        except :
            return False

    def getNotifications(self, user_id: str):
        try:
            return dbUtility.fetchAll(QUERY_GET_NOTIFICATIONS.format(user_id))
        except :
            return None

    def getNotificationsV2(self):
        try:
            return dbUtility.fetchAll(QUERY_GET_NOTIFICATIONS_V2)
        except :
            return None

    def getOnDeviceIds(self, user_id: str):
        try:
            return dbUtility.fetchAll(QUERY_GET_ON_DEVICE_IDS.format(user_id))
        except :
            return None

    def setOffDevice(self):
        try:
            return dbUtility.executeStatement(QUERY_SET_OFF_DEVICE_HAS_ZERO_TIME)
        except :
            return None