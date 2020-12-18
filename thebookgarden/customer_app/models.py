from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

UserModel=get_user_model()
# Create your models here.
class AddressBook(models.Model):
    user=models.ForeignKey(UserModel,verbose_name=_("Address Belongs to?"), on_delete=models.CASCADE,null=False)
    first_name=models.CharField(max_length=100,blank=False)
    last_name=models.CharField(max_length=100,blank=False)
    address=models.CharField(verbose_name=_("Kindly Provide Complete Address"),max_length=264,blank=False)
    city=models.CharField(max_length=100,blank=False)
    country=models.CharField(max_length=100,blank=False)
    zip_code=models.CharField(max_length=50,blank=True)
    phone_number=models.CharField(max_length=20,blank=False)
    is_default=models.BooleanField(verbose_name='By Checking this the address will come on top',default=True)

    def __str__(self):
        complete_address=self.address+','+self.city+','
        if self.zip_code == '':
            complete_address=complete_address+self.country
        else:
            complete_address=complete_address+self.zip_code+','+self.country
        return complete_address
    
        
        
