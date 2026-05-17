from django.db import models


class User(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=64, default="")
    last_name = models.CharField(verbose_name="Фамилия", max_length=64, default="")
    age = models.IntegerField(verbose_name="Возраст", default=0)
    email = models.CharField(verbose_name="Почта", max_length=128, default="")
    password = models.CharField(verbose_name="Пароль", max_length=256, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.created}"


class Places(models.Model):
    id_name = models.CharField(verbose_name="ID", max_length=16, default="")
    category = models.CharField(verbose_name="Категория", max_length=64, default="")
    name = models.CharField(verbose_name="Название", max_length=64, default="")
    description = models.CharField(verbose_name="Описание", max_length=256, default="")
    address = models.CharField(verbose_name="Адрес", max_length=128, default="")
    image_name = models.CharField(verbose_name="Название изображения", max_length=128, default="")
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.category}: {self.name}"
