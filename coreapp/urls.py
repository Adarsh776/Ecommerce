from django.urls import path
from . import views

urlpatterns = [
    path('eachcategory/<int:id>',views.EachCategory.as_view(),name='eachcategory'),
    path('paroductdetail/<str:slug>',views.ProductDetailView.as_view(),name='productdetail'),
    path('subcategoryproducts/<int:id>/',views.SubCategoryProducts.as_view(),name='subcategoryproducts'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    ]