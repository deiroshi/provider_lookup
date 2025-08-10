from django.db import models

# Create your models here.
class Provider(models.Model): # Create a new db table called Provider 
    id = models.AutoField(primary_key=True)  # unique ID that increases automatically
    npi = models.CharField(max_length=20, unique=True)  # national provider ID
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True) # ok if no middle name
    credential = models.CharField(max_length=50, blank=True, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2) 
    zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Taxonomy(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    grouping = models.CharField(max_length=100)
    classification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.display_name

class ProviderTaxonomy(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.provider} - {self.taxonomy}"