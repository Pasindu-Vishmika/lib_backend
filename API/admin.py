from django.contrib import admin
from API.models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Librarian)
admin.site.register(IssuedBook)


