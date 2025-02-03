from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Task

# Register your models here.


#Unregister Groups

admin.site.unregister(Group)

class ProfileInLine(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User;
    fields = ["username"]
    inlines = [ProfileInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Task)

