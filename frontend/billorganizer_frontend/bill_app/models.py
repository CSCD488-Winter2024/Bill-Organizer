# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bills(models.Model):
    biennium = models.CharField(primary_key=True, max_length=255)  # The composite primary key (biennium, bill_id) found, that is not supported. The first column is selected.
    bill_id = models.CharField(max_length=255,unique=True)
    bill_number = models.PositiveSmallIntegerField(blank=True, null=True)
    substitute_version = models.PositiveIntegerField(blank=True, null=True)
    engrossed_version = models.PositiveIntegerField(blank=True, null=True)
    original_agency = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    fiscal_notes = models.CharField(max_length=11, blank=True, null=True)
    appropriations = models.IntegerField(blank=True, null=True)
    requested_by = models.CharField(max_length=41, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    request = models.CharField(max_length=255, blank=True, null=True)
    introduced_date = models.DateTimeField(blank=True, null=True)
    sponsor_id = models.PositiveIntegerField(blank=True, null=True)
    long_description = models.CharField(max_length=255, blank=True, null=True)
    legal_title = models.CharField(max_length=255, blank=True, null=True)
    companion_bill = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bills'
        unique_together = (('biennium', 'bill_id'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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
    id = models.BigAutoField(primary_key=True)
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


class Lists(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    color = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey(User, models.DO_NOTHING, db_column='author')
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'lists'


class Marks(models.Model):
    list = models.ForeignKey(Lists, models.DO_NOTHING, db_column='list')
    biennium = models.ForeignKey(Bills, models.DO_NOTHING, db_column='biennium')
    bill = models.ForeignKey(Bills, models.DO_NOTHING, to_field='bill_id', related_name='marks_bill_set')

    class Meta:
        managed = False
        db_table = 'marks'


class Notes(models.Model):
    id = models.CharField(primary_key=True,max_length=256)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='author')
    creation_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    biennium = models.ForeignKey(Bills, models.DO_NOTHING, db_column='biennium')
    bill = models.ForeignKey(Bills, models.DO_NOTHING, to_field='bill_id', related_name='notes_bill_set')

    class Meta:
        managed = False
        db_table = 'notes'


class Sponsors(models.Model):
    biennium = models.CharField(primary_key=True, max_length=255)  # The composite primary key (biennium, id) found, that is not supported. The first column is selected.
    id = models.PositiveIntegerField()
    long_name = models.CharField(max_length=255, blank=True, null=True)
    agency = models.CharField(max_length=255, blank=True, null=True)
    acronym = models.CharField(max_length=255, blank=True, null=True)
    party = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sponsors'
        unique_together = (('biennium', 'id'),)


class Status(models.Model):
    biennium = models.OneToOneField(Bills, models.DO_NOTHING, db_column='biennium', primary_key=True)  # The composite primary key (biennium, bill_id, action_date) found, that is not supported. The first column is selected.
    bill = models.ForeignKey(Bills, models.DO_NOTHING, to_field='bill_id', related_name='status_bill_set')
    history_line = models.CharField(max_length=255, blank=True, null=True)
    action_date = models.DateTimeField()
    amended_by_opposite_body = models.IntegerField(blank=True, null=True)
    vetoed = models.CharField(max_length=18, blank=True, null=True)
    amendments_exist = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'status'
        unique_together = (('biennium', 'bill', 'action_date'),)
