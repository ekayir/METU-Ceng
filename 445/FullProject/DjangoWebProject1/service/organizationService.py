from databaseQueries import *
import databaseUtility as dbUtility
from service.idGeneratorService import IdGeneratorService

class OrganizationService:


    def attachDetachOrganizationtion(self, isAttached: int ,organization_id:str, user_id: str):
        try:
            return dbUtility.executeStatement(QUERY_ORGANIZATIONUSER_ATTACH_DETACH.format(isAttached,organization_id,user_id))
        except :
            return None
        
    def getOrganizationId(self, user_id: str, organization_name:str):
        try:
            return dbUtility.fetchOne(QUERY_ORGANIZATIONUSER_FILTER_BY_NAME_AND_USER_ID.format(user_id,organization_name))
        except :
            return None

    def getOrganizations(self, user_id: str):
        try:
            return dbUtility.fetchAll(QUERY_ORGANIZATIONUSER_LIST.format(user_id))
        except :
            return None

    def createNewOrganization(self,name: str, user_id: str):
        try:
            _idGeneratorService = IdGeneratorService()
            organization_id = _idGeneratorService.getNewId()
            statements = []
            statements.append(QUERY_ORGANIZATION_INSERT.format(organization_id,name))
            statements.append(QUERY_ORGANIZATIONUSER_INSERT.format(organization_id,user_id))
            return dbUtility.executeStatements(statements)
        except :
            return False

    def addOrganizationDevice(self,organization_id: str, device_id: str):
        try:
            return dbUtility.executeStatement(QUERY_ORGANIZATIONDEVICE_INSERT.format(organization_id , device_id))
        except :
            return False

    def removeOrganizationDevice(self,organization_id: str, device_id: str):
        try:
            return dbUtility.executeStatement(QUERY_ORGANIZATIONDEVICE_DELETE.format(organization_id , device_id))
        except :
            return False

    def shareOrganization(self, organization_id:str, user_id: str):
        try:
            return dbUtility.executeStatement(QUERY_ORGANIZATIONUSER_INSERT.format(organization_id , user_id))
        except :
            return False

    def unShareOrganization(self, organization_id:str, user_id: str):
        try:
            return dbUtility.executeStatement(QUERY_ORGANIZATIONUSER_DELETE.format(organization_id , user_id))
        except :
            return False
