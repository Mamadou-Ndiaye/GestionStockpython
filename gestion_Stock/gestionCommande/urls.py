from django.urls import path

from .views import *




urlpatterns = [
    # ici on declare le view  qui sera definit dans view et le nom pour acceder a sa page template
    path("",home,name='acceuil'),
    path("about/",about,name='about'),
    path("produit/",list_produits,name='produit'),
    path("produit/<int:id>",detail_produits,name='details'),
    path("produit/new", new_product, name='nouveau_produit'),
    path("produit/search/", search, name='search_produit'),
    path("produit/edit_produit/<int:id>",edit_produit,name='edit_produit'),
    path("produit/delete_produit/<int:id>",delete_produit,name='delete_produit'),
    path("categories/",categories,name='categories'),
    path("categorie/<int:id>",parcategorie,name='typecategories'),
    path("client/new", new_client, name='client'),
    path("client/",client,name='list_client'),
    path("client/<int:id>",detail_clients,name='details_client'),


]