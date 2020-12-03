
class Item(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default="S", help_text='sizes and quantity' ,verbose_name='1-category', editable=False, null=True, blank=True)
    product_category = models.CharField(max_length=2, choices=types, default='V', help_text='Products Dropdown in Egypt Fabrics Navbar', verbose_name='2-Product Category', null=True, blank=True,editable=False)
    title = models.CharField(max_length=250, unique=False)
    Company = models.CharField(max_length=260, unique=False, null=True, blank=True)
    price = models.FloatField(unique=False)
    
    discount_price = models.FloatField(blank=True, null=True, editable=False)
    description = models.TextField()   
    slug = models.SlugField(max_length=300, unique=False,help_text='random input')
    start_date = models.DateField(null=True, blank=True, editable=False)
    end_date = models.DateField(null=True, blank=True, editable=False)
    image = models.ImageField(upload_to='Egypt_fabrics', blank=False, null=False, verbose_name="1- image")
    image2 = models.ImageField(upload_to='Egypt_fabrics', blank=True, null=True,help_text="this field is optional",  verbose_name="2- image" )
    image3 = models.ImageField(upload_to='Egypt_fabrics', blank=True, null=True,help_text="this field is optional",   verbose_name="3- image" )

    class Meta:
        ordering = ['-id']


    def __str__(self):
        return self.title
    def save(self, *args, **kwargs, ):

        self.slug = slugify(self.title + self.slug + str(self.price) + '/' )+ mar
        super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Main:product", kwargs={
        'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("Main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("Main:remove-from-cart", kwargs={
            'slug': self.slug
        })

var_category = (
    ('size','size'),
   
)

class ObjectVariation(models.Manager):
    def sizes(self):
        return self.all().filter(category='size')
  
        
class Variation(models.Model):
    itemy = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item", help_text="select the item that you want to add variation to.")
    Title = models.CharField(max_length=200, verbose_name="Size", help_text="the size of the item")
    category = models.CharField(max_length=200, choices=var_category, default='size', editable=False)
    pricy = models.FloatField(verbose_name="Price")
    
    class Meta:
        ordering = ['Title']

    def __str__(self):
        return f"{self.itemy.title} - {self.Title}"
    
   
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation)
  
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['id']


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        int_hold = int()
        for i in self.variation.all():
            qypr = self.quantity * i.pricy
            int_hold += qypr
          
            return qypr
        return int_hold    

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    
