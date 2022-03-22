from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_item, name="create"),
    path("submit", views.submit, name="submit"),
    path("listing/<int:id>", views.view_listing, name="listing"),
    path("addwatchlist/<int:id>", views.add_watchlist, name="addWlist"),
    path("remwatchlist/<int:id>", views.rem_watchlist, name="remWlist"),
    path("viewWatchlist", views.view_watchlist, name="viewWatchlist"),
    path("placebid/<int:id>", views.make_bid, name="make_bid"),
    path("closebid/<int:id>", views.close_bid, name="close_bid"),
    path("categorylist", views.categories, name="view_cat"),
    path("categoryView/<str:catname>", views.catview, name="category"),
    path("postcomment/<str:id>", views.make_comment, name="make_comment")
]
