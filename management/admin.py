from django.contrib import admin
from management.models import Management, Cart

class AdminBook(admin.ModelAdmin):
    list_display = ('BookRating', 'cover_image', 'BookAuthor', 'Booktitle')
class Cartsetting(admin.ModelAdmin):
    list_display = ('user', 'book_title', 'quantity', 'total_price_display')

    def book_title(self, obj):
        return obj.book.Booktitle
    book_title.short_description = "Book"

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Total Price"

admin.site.register(Management, AdminBook)
admin.site.register(Cart,Cartsetting)  
