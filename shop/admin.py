from django.contrib import admin
from shop.models import City, Street, Shop


admin.site.register([City, Street, Shop])
