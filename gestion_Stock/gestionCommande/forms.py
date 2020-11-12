from  django import  forms
from  django.contrib.auth.forms import  UserCreationForm
from  django.contrib.auth.models import  User

from gestionCommande.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('nom','prenom','email', 'telephone', 'adresse')
        # ou bien  fields= '__all__'
        widgets = {
            'nom': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'prenom': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'telephone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'adresse': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }