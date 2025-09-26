from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ================================
# Modèle utilisateur personnalisé
# Utilise AbstractUser pour ajouter bio et avatar
# ================================
#User
class User(AbstractUser):
    bio = models.TextField(max_length=500, null=True, blank=True, verbose_name="Biographie")
    avatar = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Avatar")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return settings.MEDIA_URL + 'images/default-avatar.png'

# ================================
# Modèle de catégorie
# Permet de classer les activités
# ================================
#Category
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie", unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

# ================================
# Modèle d’activité
# Contient toutes les informations liées à une activité
# ================================
#Activity
class Activity(models.Model):
    title = models.CharField(verbose_name="Titre", validators=[MinLengthValidator(5, "Le titre doit contenir au moins 5 caractères.")], max_length=200)
    description = models.TextField(verbose_name="Description", validators=[MinLengthValidator(10, "La description doit contenir au moins 10 caractères.")])
    location_city = models.CharField(verbose_name="Ville", validators=[MinLengthValidator(2, "La ville doit contenir au moins 2 caractères.")], max_length=100)
    start_time = models.DateTimeField(verbose_name="Date et Heure de début")
    end_time = models.DateTimeField(verbose_name="Date et Heure de fin")
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposed_activities', verbose_name="Organisateur")
    attendees = models.ManyToManyField(User, related_name='attended_activities', verbose_name="Participants", blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='activities', verbose_name="Catégorie", null=True, blank=True,)

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['start_time']

    def __str__(self):
        return self.title

    def clean(self):
        """Validation personnalisée du modèle."""
        super().clean()

        now = timezone.now()
        if self.start_time and self.end_time:
            if self.start_time <= now:
                raise ValidationError("La date de début doit être dans le futur.")
            if self.end_time <= self.start_time:
                raise ValidationError("La date de fin doit être après la date de début.")

    def save(self, *args, **kwargs):
        """Override save pour appeler clean() automatiquement."""
        self.full_clean()
        super().save(*args, **kwargs)