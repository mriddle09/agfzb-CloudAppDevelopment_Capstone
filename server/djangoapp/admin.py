from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'dealer_id', 'car_model', 'car_year']
    list_filter = ['car_model', 'car_make', 'dealer_id', 'car_year',]
    search_fields = ['car_make', 'name']

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)