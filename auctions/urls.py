from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("categories", views.get_categories, name="categories"),
    path("category/<slug:category_slug>", views.display_category, name="category"),
    path("listing/<int:listing_id>", views.get_listing, name="listing"),
    path("closed-auctions", views.closed_auctions, name="closed-auctions"),
]

