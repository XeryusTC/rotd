from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'ROTD administration'

admin_site = CustomAdminSite(name='admin')
