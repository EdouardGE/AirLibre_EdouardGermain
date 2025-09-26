from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Activity

User = get_user_model()

class RegisterForm(UserCreationForm):
    """Formulaire d'inscription utilisateur avec champs personnalisés."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")
        labels = {
            "username": "Nom d’utilisateur",
            "first_name": "Prénom",
            "last_name": "Nom",
            "password1": "Mot de passe",
            "password2": "Confirmer le mot de passe",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        placeholders = {
            "username": "Nom d’utilisateur",
            "first_name": "Votre prénom",
            "last_name": "Votre nom",
            "password1": "Mot de passe",
            "password2": "Confirmer le mot de passe",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder

class AjouterActivityForm(forms.ModelForm):
    """Formulaire pour créer une activité."""
    class Meta:
        model = Activity
        fields = ['title', 'description', 'location_city', 'category', 'start_time', 'end_time']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'location_city': 'Ville',
            'category': 'Catégorie',
            'start_time': 'Date de début',
            'end_time': 'Date de fin',
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['category'].required = False
        self.fields['category'].empty_label = "Choisissez une catégorie (optionnel)"

        placeholders = {
            'title': "Titre de l'activité",
            'description': 'Description',
            'location_city': 'Ville',
            'start_time': "Date de début de l'activité",
            'end_time': "Date de fin de l'activité",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder


class ModifierUserForm(forms.ModelForm):
    """Formulaire pour modifier le profil utilisateur."""
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'email', 'bio']
        labels = {
            'avatar': "Avatar",
            'first_name': "Prénom",
            'last_name': "Nom",
            'email': "Adresse courriel",
            'bio': "Biographie",
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['bio'].widget = forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})

        placeholders = {
            'first_name': self.instance.first_name if self.instance and self.instance.first_name else "Votre prénom",
            'last_name': self.instance.last_name if self.instance and self.instance.last_name else "Votre nom",
            'email': self.instance.email if self.instance and self.instance.email else "Votre adresse courriel",
            'bio': self.instance.bio if self.instance and self.instance.bio else "Parlez-nous un peu de vous...",

        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder



