from django.db import models

from core.models import User


class New(models.Model):
    img = models.ImageField(upload_to='news')
    title = models.CharField(max_length=512)
    desc = models.TextField()
    view = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def response(self):
        return {
            "img": "" if not self.img else self.img.url,
            "title": self.title,
            "desc": self.desc,
            "view": self.view,
            "date": self.date
        }


class Category(models.Model):
    name = models.CharField(max_length=224)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    img = models.ImageField(upload_to="shop")
    cost = models.IntegerField(default=0)
    discount_price = models.IntegerField(null=True, blank=True)
    discount_percent = models.IntegerField(editable=False, default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.discount_price:
            self.discount_price = self.cost
        self.discount_percent = int(((self.cost-self.discount_price)/self.cost)*100)
        return super(Product, self).save(*args, **kwargs)


class Algorithm(models.Model):
    reward = models.IntegerField(default=0)
    description = models.TextField()
    bonus = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Done(models.Model):
    status = models.CharField(max_length=20, choices=[
        ("Bajarilmoqda", "Bajarilmoqda"),
        ("Tekshirilmoqda", "Tekshirilmoqda"),
        ("Muaffaqiyatli", "Muaffaqiyatli"),
        ("Xato", "Xato"),
    ], default="Bajarilmoqda")
    algorithm = models.ForeignKey(Algorithm, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"ut": 3})







