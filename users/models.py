from django.db import models

# Create your models here.
class TUser(models.Model):
    idemp = models.BigAutoField(primary_key=True)
    userauth = models.CharField(max_length=254, default='')
    passwd = models.CharField(max_length=200)
    categorie = models.SmallIntegerField()
    active = models.SmallIntegerField() 
    adr_ip = models.CharField(max_length=254)
    etat = models.SmallIntegerField(default=0)
    role = models.SmallIntegerField(default=0)


