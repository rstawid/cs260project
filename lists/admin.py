from django.contrib import admin
from lists.models import List, Item

#to display fields in admin page of Item
class ItemAdmin(admin.ModelAdmin):
	list_display = ('text', 'list', 'created_date', 'done', 'done_date' )

class ListAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

# Register your models here.
admin.site.register(List,ListAdmin)
admin.site.register(Item, ItemAdmin)