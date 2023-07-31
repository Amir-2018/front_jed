from django.db import models

# Create your models here : 
class TUser(models.Model):
    idemp = models.BigAutoField(primary_key=True)
    userauth = models.CharField(max_length=254, default='')
    passwd = models.CharField(max_length=200)
    categorie = models.SmallIntegerField()
    active = models.SmallIntegerField() 
    adr_ip = models.CharField(max_length=254)
    etat = models.SmallIntegerField(default=0)
    role = models.SmallIntegerField(default=0)
# create model for Files :  


class LoField(models.BinaryField):
    def db_type(self, connection):
        # Set the PostgreSQL type to 'lo' for versions prior to 12
        if 'postgres' in connection.vendor and connection.pg_version < 120000:
            return 'lo'
        # For other database backends or PostgreSQL 12+, use BinaryField
        return super().db_type(connection)
        
class TFichiers(models.Model):
    idemp = models.BigAutoField(primary_key=True)
    file = LoField()  # Custom field for LO storage
    description = models.CharField(max_length=254)






