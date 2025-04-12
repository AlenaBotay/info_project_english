from django.contrib import admin
from django.urls import path
from flashcards import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('add-category/', views.add_category, name='add_category'),
    path('categories/', views.list_categories, name='list_categories'),
    path('add-card/', views.add_card, name='add_card'),
    path('cards/', views.list_cards, name='list_cards'),
    path('test-card/', views.test_card, name='test_card'),
]
