from django.contrib import admin

# Register your models here.
from home.models import *

admin.site.register(MyUser)
admin.site.register(SoThich)
admin.site.register(SoThich_User)
admin.site.register(Conversation)
admin.site.register(Message)