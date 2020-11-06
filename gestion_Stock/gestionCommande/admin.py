from django.contrib import admin
from .models import  *

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Compte)
admin.site.register(Commande)
admin.site.register(Client)
admin.site.register(DetailCommande)
admin.site.register(Facture)


# Register your models here.
