QUERY_USER_LOGIN_CHECK = "Select Id from Users where username = '{0}' and password = '{1}' "
QUERY_USER_LIST = "Select Id as Id, Username as Username from auth_user au "
QUERY_USER_FILTER_USERNAME = "Select Id from Users where username = '{0}' "

QUERY_PART_INSERT = "INSERT INTO Parts (Id, DeviceId, ProductNo, Type, Description, TotalLifeTime, ExpectedLifeTime, Price, Specs) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','') "
QUERY_PART_INSERT_VIA_CATALOG_DEVICE = "INSERT INTO Parts (Id, DeviceId, ProductNo, Type, Description, TotalLifeTime, ExpectedLifeTime, Price, Specs) Select  lower(hex(randomblob(16)))as id,'{0}' as DeviceId, p.ProductNo , p.Type ,p.Description ,p.TotalLifeTime ,p.ExpectedLifeTime ,p.Price ,p.Specs  from Devices d , Parts p where d.Id  = p.DeviceId and d.Id ='{1}' "
QUERY_PART_DELETE = "DELETE FROM Parts where Id = '{0}' "
QUERY_PART_LIST = "Select d.ProductNo as Device_ProductNo, p.ProductNo as Part_ProductNo, p.Id , p.Type ,p.Description  as Description , p.TotalLifeTime as TotalLifeTime ,p.ExpectedLifeTime as ExpectedLifeTime ,p.Price from Parts p,  OrganizationUsers ou, Devices d where p.DeviceId  = d.Id and d.OrganizationId =ou.OrganizationId and ou.UserId ='{0}' and ou.OrganizationId ='{1}' order by D.ProductNo  "
QUERY_PART_GET_ID_FILTER_ID = "SELECT Id FROM Parts where Id = '{0}' "
QUERY_PART_GET_PART_LIST_OF_DEVICES = "Select d.Id as DeviceId ,d.ProductNo as Device_ProductNo, p.ProductNo as  Part_ProductNo, p.Id as Id , p.Type as Type ,p.Description as Description , p.TotalLifeTime as TotalLifeTime,case when p.ExpectedLifeTime < 0 then 0 else p.ExpectedLifeTime end as ExpectedLifeTime ,p.Price as Price from Parts p,  Devices d where p.DeviceId  = d.Id and d.Id = '{0}' "
QUERY_PART_GET_PART_LIST_OF_ALL_DEVICES = "Select d.Id as DeviceId ,d.ProductNo as Device_ProductNo, p.ProductNo as  Part_ProductNo, p.Id as Id , p.Type as Type ,p.Description as Description , p.TotalLifeTime as TotalLifeTime,case when p.ExpectedLifeTime < 0 then 0 else p.ExpectedLifeTime end as ExpectedLifeTime ,p.Price as Price from Parts p,  Devices d where p.DeviceId  = d.Id  "

QUERY_DEVICE_INSERT = "INSERT INTO Devices (Id, Type, Description, ProductNo, OrganizationId) Select '{0}' as Id ,Type ,Case when '{1}' = '' then Description else '{2}' end as Description, ProductNo ,'{3}' as OrganizationId from Devices  where Id ='{4}' "


QUERY_DEVICE_LIST_FILTER_BY_USER_ID = "Select d.ProductNo as ProductNo , d.Type as Type , d.Description as Description , case when d.IsOn = 1 then 'On' else 'Off' end as IsOn,d.Id as Id from Devices d , OrganizationUsers ou  where d.OrganizationId = ou.OrganizationId and ou.UserId ={0} and ou.OrganizationId = '{1}' "
QUERY_GET_CATALOG_DEVICE_ID_FILTER_BY_PRODUCT_NO = "Select Id from Devices d where d.ProductNo = {0} and  d.OrganizationId is null "

QUERY_ORGANIZATION_INSERT = "INSERT INTO Organizations (Id,Name) VALUES('{0}','{1}')"
QUERY_ORGANIZATIONUSER_INSERT = "INSERT INTO OrganizationUsers (OrganizationId, UserId) VALUES('{0}', {1})"
QUERY_ORGANIZATIONUSER_LIST = "Select o.Name, o.Id, case when IsAttached = 1 then 'True' else 'False' end as IsAttached from OrganizationUsers ou, Organizations o where ou.OrganizationId = o.Id and UserId='{0}' "
QUERY_ORGANIZATIONUSER_FILTER_BY_NAME_AND_USER_ID = "Select o.Id from OrganizationUsers ou, Organizations o where ou.OrganizationId = o.Id and UserId='{0}' and o.Name='{1}' "
QUERY_ORGANIZATIONUSER_USERNAME_FILTER_BY_NAME_AND_USER_ID = "Select o.Id, ou.IsAttached from OrganizationUsers ou, Organizations o where ou.OrganizationId = o.Id and UserId='{0}' and o.Name='{1}' "
QUERY_ORGANIZATIONUSER_DELETE = "DELETE FROM OrganizationUsers WHERE OrganizationId='{0}' AND UserId='{1}' "
QUERY_ORGANIZATIONUSER_ATTACH_DETACH = "Update OrganizationUsers set IsAttached = {0} WHERE OrganizationId='{1}' AND UserId='{2}' "

#return authorized user filter by user id and organization id without itself
QUERY_ORGANIZATIONUSER_USERNAME_FILTER_BY_USERID_ORG_ID = "Select u.Id as Id , u.Username as Username from OrganizationUsers ou, Organizations o, auth_user u ,OrganizationUsers ou1 where ou.OrganizationId = o.Id and u.Id  = ou.UserId  and o.Id  = ou.OrganizationId  and o.Id = ou1.OrganizationId AND ou.UserId <> ou1.UserId and ou1.UserId ='{0}' and o.Id ='{1}' "
QUERY_ALL_USER_EXCEPT_AUTH_ORGANIZATION = "select au.Id as Id , au.Username as Username from auth_user au WHERE au.Id not in ( Select u.Id   from OrganizationUsers ou, Organizations o, auth_user u ,OrganizationUsers ou1 where ou.OrganizationId = o.Id and u.Id  = ou.UserId  and o.Id  = ou.OrganizationId  and o.Id = ou1.OrganizationId  and ou1.UserId ='{0}' and o.Id ='{1}')"

QUERY_ORGANIZATIONDEVICE_INSERT = "INSERT INTO OrganizationDevices (OrganizationId, DeviceId) VALUES('{0}','{1}')"
QUERY_ORGANIZATIONDEVICE_DELETE = "DELETE OrganizationDevices Where OrganizationId = '{0}' and DeviceId = '{1}'"

QUERY_GET_CATALOG_DEVICES = "select ProductNo as ProductNo ,Type as Type , Description as Description, Id as Id, 'Off' as IsOn  from Devices d where d.OrganizationId is null "
QUERY_DEVICES_FILTER_BY_ID = "select d.Id from Devices d where d.Id='{0}' "
QUERY_DEVICES_SET_ON = "Update Devices set isOn = 1, OnDateTime = DATETIME('now') where Id = '{0}' "
QUERY_DEVICES_SET_OFF = "Update Devices set isOn = 0, OnDateTime = NULL where Id = '{0}' "
OUERY_DEVICES_SET_OFF_UPDATE_TIME = "Update Parts set ExpectedLifeTime = ExpectedLifeTime - (select ROUND((JULIANDAY( DATEtime('now')) - JULIANDAY(OnDateTime )) * 86400) from Devices d where d.Id ='{0}') where DeviceId ='{1}' "

QUERY_ADD_DEVICE_TO_CATALOG = "INSERT INTO Devices (Id, Type, Description, ProductNo) VALUES('{0}', '{1}', '{2}', '{3}' )"
OUERY_ADD_PART_TO_CATALOG_DEVICE = "INSERT INTO Parts (Id, DeviceId, ProductNo, Type, Description, TotalLifeTime, ExpectedLifeTime, Price, Specs) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6}, {7}, '')"
QUERY_GET_CATALOG_PARTS = "Select d.ProductNo as Device_ProductNo, p.Id , p.Type ,p.Description , p.TotalLifeTime ,p.ExpectedLifeTime ,p.Price from Parts p , Devices d where p.DeviceId = d.Id  and d.OrganizationId is null order by d.ProductNo "

QUERY_GET_NOTIFICATIONS = "select o.Name as OrganizationName, d.ProductNo as DeviceProductNo, p.ProductNo  as PartProductNo, case when p.ExpectedLifeTime < 0 then 0 else p.ExpectedLifeTime end as ExpectedLifeTime, case when d.IsOn = 1 then 'On' else 'Off' end as IsOn from Parts p , OrganizationUsers ou , Devices d , Organizations o where p.DeviceId = d.Id and ou.OrganizationId = d.OrganizationId and o.Id = ou.OrganizationId  and ou.IsAttached = 1 and p.ExpectedLifeTime < 10 and ou.UserId = {0} order by o.Name ,d.Id  "
QUERY_GET_ON_DEVICE_IDS = "Select Id as DeviceId from Devices d, OrganizationUsers ou where d.OrganizationId = ou.OrganizationId and d.IsOn = 1 and ou.UserId = {0}"
QUERY_GET_ALL_ON_DEVICE_IDS = "Select Id as DeviceId from Devices d where d.IsOn = 1 and Id not in (Select Id from Parts p where p.ExpectedLifeTime <= 0) "

QUERY_GET_NOTIFICATIONS_V2 = "select p.Id as PartId,ou.UserId as UserId ,o.Name as OrganizationName, d.ProductNo as DeviceProductNo, p.ProductNo  as PartProductNo, case when p.ExpectedLifeTime < 0 then 0 else p.ExpectedLifeTime end as ExpectedLifeTime, case when d.IsOn = 1 then 'On' else 'Off' end as IsOn from Parts p , OrganizationUsers ou , Devices d , Organizations o, auth_user au where p.DeviceId = d.Id and ou.OrganizationId = d.OrganizationId and o.Id = ou.OrganizationId and au.id =ou.UserId and ou.IsAttached = 1 and p.ExpectedLifeTime < au.notificationLimit  order by o.Name ,d.Id "

QUERY_IS_OPENABLE_DEVICE = "Select COUNT(1) from Parts p where DeviceId ='{0}' and ExpectedLifeTime <= 0 "

QUERY_SET_OFF_DEVICE_HAS_ZERO_TIME = "Update Devices set IsOn = 0 where IsOn = 1 and Id in (select DeviceId from Parts where ExpectedLifeTime <=0)"


QUERY_SET_USER_NOTIFICATION_TIME = "update auth_user set notificationLimit ={0} where id ={1} "