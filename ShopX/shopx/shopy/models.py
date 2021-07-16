from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models.deletion import CASCADE

# Create your models here.
CONTIGUOUS_STATES = (
    ('AL', 'Alabama'),
    ('AZ', 'Arizona'), 
    ('AR', 'Arkansas'), 
    ('CA', 'California'), 
    ('CO', 'Colorado'), 
    ('CT', 'Connecticut'), 
    ('DE', 'Delaware'), 
    ('DC', 'District of Columbia'), 
    ('FL', 'Florida'), 
    ('GA', 'Georgia'), 
    ('ID', 'Idaho'), 
    ('IL', 'Illinois'), 
    ('IN', 'Indiana'), 
    ('IA', 'Iowa'), 
    ('KS', 'Kansas'), 
    ('KY', 'Kentucky'), 
    ('LA', 'Louisiana'), 
    ('ME', 'Maine'), 
    ('MD', 'Maryland'), 
    ('MA', 'Massachusetts'), 
    ('MI', 'Michigan'), 
    ('MN', 'Minnesota'), 
    ('MS', 'Mississippi'), 
    ('MO', 'Missouri'), 
    ('MT', 'Montana'), 
    ('NE', 'Nebraska'), 
    ('NV', 'Nevada'), 
    ('NH', 'New Hampshire'), 
    ('NJ', 'New Jersey'), 
    ('NM', 'New Mexico'), 
    ('NY', 'New York'), 
    ('NC', 'North Carolina'), 
    ('ND', 'North Dakota'), 
    ('OH', 'Ohio'), 
    ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), 
    ('PA', 'Pennsylvania'), 
    ('RI', 'Rhode Island'), 
    ('SC', 'South Carolina'), 
    ('SD', 'South Dakota'), 
    ('TN', 'Tennessee'), 
    ('TX', 'Texas'), 
    ('UT', 'Utah'), 
    ('VT', 'Vermont'), 
    ('VA', 'Virginia'), 
    ('WA', 'Washington'), 
    ('WV', 'West Virginia'), 
    ('WI', 'Wisconsin'), 
    ('WY', 'Wyoming')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=CONTIGUOUS_STATES ,max_length=100)

    def __str__(self):
        return str(self.id)

CATEGORY = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear')
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY, max_length=5)
    product_image = models.ImageField(upload_to='productIMG')# name folder upload Img auto create   

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property

    def total_cost(self):
        return self.quantity * self.product.discounted_price 

STATUS = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS,default='Pending')


