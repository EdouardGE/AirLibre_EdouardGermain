from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Activity, User, Category
from .utils import get_air_quality

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm, AjouterActivityForm, ModifierUserForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# ================================
# Vue d'accueil : liste des activités
# Permet de filtrer par catégorie, par activités proposées ou par inscriptions
# Pagination : 3 activités par page
# ================================
#index
def index(request):
    activities = Activity.objects.all().order_by("start_time")

    category_name = request.GET.get("category")
    if category_name:
        activities = activities.filter(category__name=category_name)

    filter_option = request.GET.get("filter", "all")
    if filter_option == "mine" and request.user.is_authenticated:
        activities = activities.filter(proposer=request.user)
    elif filter_option == "inscriptions" and request.user.is_authenticated:
        activities = activities.filter(attendees=request.user)

    paginator = Paginator(activities, 3)
    page_number = request.GET.get("page")
    activities = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(
        request,
        "activities/index.html",
        {"activities": activities, "categories": categories},
    )

# ================================
# Vue détail d’une activité
# Ajoute aussi la qualité de l’air en fonction de la ville via l’API
# ================================
#detail_activite
def detail_activite(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    activity.air_quality = get_air_quality(activity.location_city)

    return render(request, 'activities/detail_activite.html', {'activity': activity})

# ================================
# Vue pour se désinscrire d’une activité
# Supprime l’utilisateur de la liste des participants
# ================================
#desinscription_activite
@login_required()
def desinscription_activite(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
            activity.attendees.remove(request.user)
            messages.success(request, "Vous vous êtes désinscrit de l'activité.")
    return redirect("detail_activite", pk=pk)

# ================================
# Vue pour s’inscrire à une activité
# Ajoute l’utilisateur à la liste des participants
# ================================
#inscription_activite
@login_required()
def inscription_activite(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
            activity.attendees.add(request.user)
            messages.success(request, "Vous vous êtes inscrit à l'activité.")
    return redirect("detail_activite", pk=pk)

# ================================
# Page de connexion (Django auth.)
# ================================
#login
def login(request):
    return render(request, 'registration/login.html')

# ================================
# Inscription d’un nouvel utilisateur
# Utilise RegisterForm pour valider et enregistrer un compte
# ================================
#signup
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect("login")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = RegisterForm()

    return render(request, "registration/signup.html", {"form": form})

# ================================
# Vue profil utilisateur
# Affiche les activités créées par l’utilisateur et celles auxquelles il participe
# ================================
#profile
def profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    activities = Activity.objects.filter(proposer=profile_user)
    mes_inscriptions = Activity.objects.filter(attendees=profile_user).order_by("start_time")

    return render(
        request,
        "activities/profile.html", { "profile_user": profile_user, "activities": activities, "mes_inscriptions": mes_inscriptions, },
    )

# ================================
# Création d’une nouvelle activité
# Seul un utilisateur connecté peut proposer une activité
# ================================
#new_activity
@login_required()
def new_activity(request):
    if request.method == "POST":
        form = AjouterActivityForm(request.POST)
        if form.is_valid():
            new_activity = form.save(commit=False)
            new_activity.proposer = request.user
            new_activity.save()
            messages.success(request, "Activité ajoutée avec succès !")
            return redirect("index")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AjouterActivityForm()

    return render(request, "activities/ajouter_activite.html", {"form": form})

# ================================
# Mise à jour du profil utilisateur
# Permet de modifier ses informations personnelles et son avatar
# ================================
#update_profile
@login_required()
def update_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = ModifierUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profile a été mis à jour !")
            return redirect("profile", user_id=request.user.id)
    else:
        form = ModifierUserForm(instance=request.user)

    return render(request, "activities/modifier_profile.html", {"form": form, "user": user})



