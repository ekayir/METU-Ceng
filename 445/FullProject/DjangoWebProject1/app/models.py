# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Devices(models.Model):
    id = models.TextField(db_column='Id', primary_key = True)  # Field name made lowercase.
    type = models.TextField(db_column='Type')  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    productno = models.TextField(db_column='ProductNo')  # Field name made lowercase.
    organizationid = models.TextField(db_column='OrganizationId', blank=True, null=True)  # Field name made lowercase.
    ison = models.IntegerField(db_column='IsOn')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Devices'


class Organizationusers(models.Model):
    organizationid = models.ForeignKey('Organizations', models.DO_NOTHING, db_column='OrganizationId')  # Field name made lowercase.
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    isattached = models.IntegerField(db_column='IsAttached')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrganizationUsers'


class Organizations(models.Model):
    id = models.TextField(db_column='Id', primary_key = True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', unique=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Organizations'


class Parts(models.Model):
    id = models.TextField(db_column='Id', primary_key = True)  # Field name made lowercase.
    deviceid = models.TextField(db_column='DeviceId')  # Field name made lowercase.
    productno = models.TextField(db_column='ProductNo')  # Field name made lowercase.
    type = models.TextField(db_column='Type')  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    totallifetime = models.IntegerField(db_column='TotalLifeTime')  # Field name made lowercase.
    expectedlifetime = models.IntegerField(db_column='ExpectedLifeTime')  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    specs = models.TextField(db_column='Specs')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Parts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
