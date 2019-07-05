from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shophome'),
    path('about/', views.about, name='AboutUs'),
    path('track-item/', views.track, name='TrackItem'),
    path('products/<int:id>/', views.productview, name="ProductView"),
    path('checkout/', views.checkout, name="CheckOut"),
    path('handlerequest/',views.handlerequest,name="HandleRequest"),
    path('search/', views.search, name="Search"),
]
