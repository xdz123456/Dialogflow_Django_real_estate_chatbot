from django.contrib.auth.models import User
from django.db import models


# Create your Property here.
class Property(models.Model):
    property_address = models.CharField(max_length=128, null=False)
    property_city = models.CharField(max_length=128, null=False)
    property_postcode = models.CharField(max_length=128)
    property_type = models.CharField(max_length=128)
    property_num_bedroom = models.IntegerField()
    property_price = models.FloatField()
    property_date = models.DateTimeField()
    property_belong = models.ManyToManyField(User, related_name='user_belong')
    property_interested = models.ManyToManyField(User, related_name='user_interested')

    def __str__(self):
        return self.property_address


class InputText(models.Model):
    input_text = models.CharField(max_length=512, null=False)

    def __str__(self):
        return self.input_text
