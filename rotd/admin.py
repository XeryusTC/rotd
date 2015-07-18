from django.contrib.admin import AdminSite
from django.contrib.auth.admin import User, UserAdmin, Group, GroupAdmin

class CustomAdminSite(AdminSite):
    site_header = 'ROTD administration'

admin_site = CustomAdminSite(name='admin')
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
