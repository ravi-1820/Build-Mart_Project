from django.db import models    
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=10)
    uprofile = models.ImageField(default="", upload_to="uprofile/")
    usertype = models.CharField(max_length=20, default="buyer")

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = (
        ("Cement", "Cement"),
        ("Bricks", "Bricks"),
        ("Rebars", "Rebars"),
        ("Concrete Bricks", "Concrete Bricks"),
        ("Concrete Block", "Concrete Block"),
        ("Soil", "Soil"),
        ("Patthar", "Patthar")
    
    )
    company = (
        ("UltraTech", "UltraTech"),
        ("Jindal", "Jindal"),
        ("Trishul", "Trishul"),
        ("Village Soil", "Village Soil"),
        ("Arbuda", "Arbuda")

    )
    pcategory = models.CharField(max_length = 50)
    pcompany = models.CharField(max_length = 50)
    pname = models.CharField(max_length = 50)
    pprice = models.IntegerField()
    pdesc = models.TextField()
    pimage = models.ImageField(default = "", upload_to = "product/")

    def __str__(self):
        return f"{self.pname}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    ttime = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    ttime = models.DateTimeField(default = timezone.now)
    total = models.PositiveBigIntegerField()
    qty = models.PositiveBigIntegerField(default=1)
    payment = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product}"