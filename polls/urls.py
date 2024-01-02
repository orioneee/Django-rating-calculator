from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("fillSubjects/", views.fillSubjects, name="fillRating"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("fill_rating/", views.ratingForm, name="fill_rating"),
    path("table/", views.ratingTable, name="ratingTable"),
]