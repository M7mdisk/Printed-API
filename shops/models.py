from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django_extensions.db.fields import ShortUUIDField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from .validators import validate_file_extension
import os
import PyPDF2
# Helper Functions

def file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "media/%s/%s_%s.%s" % (instance.shop.name,instance.shop.name,instance.uuid, ext)
    return os.path.join('uploads', filename)

class Profile(models.Model):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE,related_name='profile')
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,limit_choices_to={'is_owner': True})
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return self.name


SIZE_CHOICES = (("A4","A4"),("A3","A3"),('A2','A2'))
STATUS_CHOICES = (("On Queue","On Queue"),("Proccessing","Proccessing"),('Finished','Finished'),('Recieved','Recieved'))

class Order(models.Model):
    uuid = ShortUUIDField(primary_key=True)
    buyer = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='buyer')
    date = models.DateTimeField(auto_now_add=True)
    docfile = models.FileField(upload_to=file_name,validators=[validate_file_extension])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1)
    type = models.ForeignKey(Type,on_delete=models.CASCADE, related_name='printtype',default=0)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='shop')
    @property
    def total(self):
        ext = os.path.splitext(self.docfile.url)[1]
        if ext == '.pdf':
            pdf = PyPDF2.PdfFileReader(self.docfile)
            npages = pdf.getNumPages()
            return self.quantity * npages * Type.objects.filter(name=self.type).first().price
        else:
            return self.quantity * Type.objects.filter(name=self.type).first().price        
    
    @property
    def pages(self):
        pdf = PyPDF2.PdfFileReader(self.docfile)
        return pdf.getNumPages()  
           
    notes = models.TextField(blank=True,max_length=300, default='')
    size = models.CharField(max_length=9,
                  choices=SIZE_CHOICES,
                  default="A4")  
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,
                  default="On Queue")
    @property
    def extension(self):
        name, extension = os.path.splitext(self.docfile.name)
        return extension

    def __str__(self):
        return str(self.uuid)

    class Meta:
        ordering = ['date']

