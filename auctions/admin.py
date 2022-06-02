from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid, Watchlist

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'slug')
  prepopulated_fields = {'slug': ('name',)}

class ListingAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "startingBid", "category", "author", "active")



admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
