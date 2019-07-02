from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shophome'),
    path('about/', views.about, name='AboutUs'),
    path('track-item/', views.track, name='TrackItem'),
    path('products/<int:id>/', views.productview, name="ProductView"),
]
