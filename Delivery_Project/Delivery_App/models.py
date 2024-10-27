from django.db import models
import uuid

# Create your models here.

'''class DeliveryPersons(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_id = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30)
    phone = models.BigIntegerField(null=True,blank=True)
    invertrID = models.CharField(max_length=30, null=True, blank=True)
    inviteCode = models.JSONField(null=True,blank=True)
    tags = models.CharField(max_length=20,null=True,blank=True)
    first_name = models.CharField(max_length=30, null=True,blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    dateofbirth = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male','Male'),('female','Female'),('others','Others')])
    last_login = models.DateTimeField(blank=True, null=True)
    twofactor_authentication = models.JSONField(null=True, blank=True)
    Account_verification = models.JSONField(null=True, blank=True)
    activity_status = models.CharField(max_length=30, null=True, blank=True, choices=[('offline','Offline'),('online','Online')])
    account_status = models.CharField(max_length=30, null=True, blank=True)
    ratings = models.IntegerField(null=True,blank=True)
    avgrating = models.FloatField(null=True, blank=True)
    clatitude = models.FloatField(blank=True)
    clongitude = models.FloatField(blank=True)
    Geopoint = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username
'''