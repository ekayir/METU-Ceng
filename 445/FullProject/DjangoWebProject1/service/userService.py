from databaseQueries import *
import databaseUtility as dbUtility

class UserService():
    def getUserId(self,username: str, password: str):
        try:
            return dbUtility.fetchOne(QUERY_USER_LOGIN_CHECK.format(username, password))
        except :
            return None

    def getUserIdByUsername(self, username: str):
        try:
            return dbUtility.fetchOne(QUERY_USER_FILTER_USERNAME.format(username))
        except :
            return None

    def getAllUsers(self):
        try:
            return dbUtility.fetchAll(QUERY_USER_LIST)
        except :
            return None

    def getAllAuthUsers(self, user_id: str, organization_id: str):
        try:
            return dbUtility.fetchAll(QUERY_ORGANIZATIONUSER_USERNAME_FILTER_BY_USERID_ORG_ID.format(user_id, organization_id))
        except :
            return None

    def getAllNotAuthUsers(self, user_id: str, organization_id: str):
        try:
            return dbUtility.fetchAll(QUERY_ALL_USER_EXCEPT_AUTH_ORGANIZATION.format(user_id, organization_id))
        except :
            return None


    def setNotificationLimit(self, user_id: str, time: int):
        try:
            return dbUtility.executeStatement(QUERY_SET_USER_NOTIFICATION_TIME.format(time,user_id))
        except :
            return None
