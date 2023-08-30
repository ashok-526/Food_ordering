from django.contrib import admin
from .models import *
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
	pass



admin.site.register(Categories, MemberAdmin)
admin.site.register(Pizza, MemberAdmin) 
admin.site.register(Cart, MemberAdmin) 
admin.site.register(CartItem, MemberAdmin) 


