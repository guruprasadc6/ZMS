from django.db import models

from django.contrib.auth.models import User

class staff_test(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    cardid = models.CharField(db_column='cardID', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'staff_test'


class Animal(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    commonname = models.CharField(db_column='commonName', max_length=45)  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=45)  # Field name made lowercase.
    dob = models.DateField()
    class_field = models.CharField(db_column='class', max_length=45)  # Field renamed because it was a Python reserved word.
    dod = models.DateField(blank=True, null=True)
    edscore = models.FloatField(db_column='edScore', blank=True, null=True)  # Field name made lowercase.
    height = models.FloatField()
    weight = models.FloatField()
    healthstatus = models.CharField(db_column='healthStatus', max_length=45)  # Field name made lowercase.
    image = models.ImageField()

    def get_name(self):
        return self.commonname
    def __str__(self):
        return self.commonname
    class Meta:
        managed = False
        db_table = 'animal'


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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

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


class Department(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=45)
    image = models.ImageField()

    def get_name(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'department'


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


class Exhibit(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=45)
    doo = models.DateField()
    noofvisitors = models.IntegerField(db_column='noOfVisitors')  # Field name made lowercase.
    image = models.ImageField()

    def get_name(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'exhibit'


class LivesIn(models.Model):
    animal = models.ForeignKey(Animal, models.DO_NOTHING,unique=True)
    exhibit = models.ForeignKey(Exhibit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lives_in'
        unique_together = (('animal', 'exhibit'),)


class LooksAfter(models.Model):
    animal = models.ForeignKey(Animal, models.DO_NOTHING)
    staff = models.ForeignKey('Staff', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'looks_after'
        unique_together = (('staff', 'animal'),)


class Manages(models.Model):
    staff = models.ForeignKey('Staff', models.DO_NOTHING)
    exhibit = models.ForeignKey(Exhibit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'manages'
        unique_together = (('staff', 'exhibit'),)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=4)
    firstname = models.CharField(db_column='firstName', max_length=45)  # Field name made lowercase.
    middlename = models.CharField(db_column='middleName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    dob = models.DateField()
    doorno = models.CharField(db_column='doorNo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    housename = models.CharField(db_column='houseName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    streetname = models.CharField(db_column='streetName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1)
    contactno = models.CharField(db_column='contactNo', max_length=10)  # Field name made lowercase.
    image = models.ImageField(null=True,blank=True)

    def get_name(self):
        return self.firstname +' '+ self.lastname

    class Meta:
        managed = False
        db_table = 'staff'


class TicketBookings(models.Model):
    id = models.IntegerField(primary_key=True)
    f_name = models.CharField(max_length=45)
    l_name = models.CharField(max_length=45)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    contact = models.CharField(max_length=10)
    email = models.CharField(max_length=45)
    date_of_visit = models.DateField()
    city = models.CharField(max_length=45)
    no_of_adult_tickets = models.IntegerField()
    no_of_child_tickets = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket_bookings'


class WorksIn(models.Model):
    staff = models.ForeignKey(Staff, models.DO_NOTHING, unique=True)
    dept = models.ForeignKey(Department, models.DO_NOTHING)
    doj = models.DateField()
    dol = models.DateField(blank=True, null=True)
    salary = models.FloatField()

    class Meta:
        managed = False
        db_table = 'works_in'
        unique_together = (('staff', 'dept'),)