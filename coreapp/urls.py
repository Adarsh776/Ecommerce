from django.urls import path
from . import views

urlpatterns = [
    path('eachcategory/<int:id>',views.EachCategory.as_view(),name='eachcategory'),
    path('paroductdetail/<str:slug>',views.ProductDetailView.as_view(),name='productdetail')
    ]