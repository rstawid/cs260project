from django.contrib import admin
from lists.models import List, Item

#to displaye fields in admin page of Item
class ItemAdmin(admin.ModelAdmin):
	list_display = ('text', 'created_date', 'done', 'list')

class ListAdmin(admin.ModelAdmin):
	list_display = ('id')

# Register your models here.
admin.site.register(List)
admin.site.register(Item, ItemAdmin)