from django.contrib import admin
from .models import BookCategory,Book,BookImage,Author
# Register your models here.
admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(BookImage)
admin.site.register(Author)
