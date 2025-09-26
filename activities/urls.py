from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('activities/', views.index, name='activity_list'),
    path('activity/<int:pk>/', views.detail_activite, name='detail_activite'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path("activity/new/", views.new_activity, name="ajouter_activite"),
    path("profile/<int:user_id>/edit/", views.update_profile, name="modifier_profile"),
    path("activity/<int:pk>/inscription/", views.inscription_activite, name="inscription_activite"),
    path("activity/<int:pk>/desinscription/", views.desinscription_activite, name="desinscription_activite"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
