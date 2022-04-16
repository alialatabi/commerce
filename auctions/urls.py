from django.urls import path

from . import views

urlpatterns = [
    path("Listing/Closed/<int:l_id>", views.close, name="close"),
    path("Listing/Comment/<int:l_id>", views.comment, name="comment"),
    path("Listing/<int:l_id>", views.show, name="show"),
    path("Listings/<int:cat_id>", views.cat_listings, name="cat_listings"),
    path("category", views.category, name="category"),
    # path("watch/<int:w_id>", views.del_watch, name="del_watch"),
    path("watch/<int:l_id>", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
