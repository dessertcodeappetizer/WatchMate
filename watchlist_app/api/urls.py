from django.contrib import admin
from django.urls import path, include
from watchlist_app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', views.streamplatformsVS, basename='streamplatforms')

urlpatterns = [
    path('list/', views.watchlistAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='movie-detail'),
    path('list2/', views.WatchlistGV.as_view(), name='watch-list'),
    path('', include(router.urls)),
    # path('stream/', views.streamplatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', views.StreamPlatformdetail.as_view(), name='movie-detail'),
    # path('review/', views.Reviewlist.as_view(), name='review-list'),
    # path('review/<int:pk>', views.Reviewdetails.as_view(), name='review-detail'),
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', views.Reviewlist.as_view(), name='review-list'),
    path('review/<int:pk>/', views.Reviewdetails.as_view(), name='review-detail'),
    # path('review/<str:username>/', views.UserReview.as_view(), name='user-review-detail'),
    path('review/', views.UserReview.as_view(), name='user-review-detail'),         #filtering against the query
]