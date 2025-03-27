from django.urls import path
from . import views


urlpatterns=[
    path('addtocart/<str:slug>/',views.AddToCartView.as_view(),name='addtocart')
]