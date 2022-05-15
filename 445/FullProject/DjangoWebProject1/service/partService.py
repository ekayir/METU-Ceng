from databaseQueries import *
import databaseUtility as dbUtility
from service.idGeneratorService import IdGeneratorService

class PartService():

    def addPart(self,device_id: str ,product_no: str, part_type: str, description: str,total_life_time:int , price: float):
        try:
            _idGeneratorService = IdGeneratorService()
            return dbUtility.executeStatement(QUERY_PART_INSERT.format(_idGeneratorService.getNewId(),device_id,product_no,part_type,description,total_life_time,total_life_time,price))
        except :
            return False

    def removePart(self,part_id: str):
        try:
            return dbUtility.executeStatement(QUERY_PART_DELETE.format(part_id))
        except :
            return False

    def getPartsV2(self,user_id: str, organization_id : str):
        try:
            return dbUtility.fetchAll(QUERY_PART_LIST.format(user_id, organization_id))
        except :
            return []
        #QUERY_PART_GET_PART_LIST_OF_DEVICES
    def getParts(self,device_id: str):

        try:
            return dbUtility.fetchAll(QUERY_PART_GET_PART_LIST_OF_DEVICES.format(device_id))
        except :
            return []

    def getAllParts(self):

        try:
            return dbUtility.fetchAll(QUERY_PART_GET_PART_LIST_OF_ALL_DEVICES)
        except :
            return []

    def getCatalogParts(self):
        try:
            return dbUtility.fetchAll(QUERY_GET_CATALOG_PARTS)
        except :
            return []

    def getPartId(self, part_id: str):
        try:
            return dbUtility.fetchOne(QUERY_PART_GET_ID_FILTER_ID.format(part_id))
        except :
            return None
    
