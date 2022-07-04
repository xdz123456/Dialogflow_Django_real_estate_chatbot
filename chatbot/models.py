from django.db import models


# Create your models here.
class House(models.Model):
    house_address = models.CharField(max_length=128, null=False)
    house_area = models.FloatField()
    house_date = models.DateTimeField()

    def __str__(self):
        return self.house_address


class User(models.Model):
    user_name = models.CharField(max_length=128, null=False)
    user_email = models.EmailField()
    user_telephone = models.CharField(max_length=128)
    user_house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name


class InputText(models.Model):
    input_text = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.input_text



