from django.db import models
from shop import models as md
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def get_all_categories():
        return Category.objects.all
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default =0)
    description = models.CharField(max_length=50,default = ' ')
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(md.Category,on_delete=models.CASCADE)
    def get_all_products():
        return Product.objects.all

    def get_by_prodId(ids):
        return Product.objects.filter(id__in = ids)

    def get_all_prod_byId(id):
        if id:
            return Product.objects.filter(category=id)
        else:
            Product.get_all_products()


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=1000000000000000000000000000000000000000000)

    def register(self):
        self.save()
    def get_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False


class Order(models.Model):
    product = models.ForeignKey(Product,on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def get_by_custoId(c_id):
        return Order.objects.filter(customer=c_id)

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField(max_length=254)
    problem = models.CharField(max_length=100000)