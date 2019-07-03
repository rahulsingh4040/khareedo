from django.db import models


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default='NA')
    product_desc = models.CharField(max_length=1500, default='NA')
    product_seller = models.CharField(max_length=100, default='NA')
    product_stock = models.IntegerField(default=0)
    product_pubdate = models.DateField(default='2019-07-01')
    product_price = models.IntegerField(default=0)
    product_cat = models.CharField(max_length=50, default='NA')
    product_subcat = models.CharField(max_length=50, default='NA')
    product_img = models.ImageField(upload_to="shop/images", default="")
    product_discount = models.IntegerField(default=0)
    product_amt = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=30)
    state  = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=6)
    phone = models.CharField(max_length=10,default="")

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key = True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
