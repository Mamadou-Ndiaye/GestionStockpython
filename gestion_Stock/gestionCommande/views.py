import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils._os import safe_join

from gestionCommande.forms import ClientForm
from gestionCommande.models import Produit, Categorie ,Client
from django.conf import settings


@login_required(login_url="/login/")
def home(request):
    categories = Categorie.objects.all()
    context = {"categories": categories}
    print(context)
    produits = Produit.objects.all()
    context = {"produits": produits,"categories": categories}
    print(context)
    return  render(request ,"pages/index.html",context)

def about(request):
    message="Voici un variable de la vue qu'on affiche dans notre templates"
    context={"message":message}
    return  render(request ,"pages/about.html",context)

# on force l'utilisateur a se connecter d'abord pour acceder a cette page
@login_required(login_url="/login/")
def list_produits(request):
    user= request.user;
    print(user)
        #Pour les filtres ici seul l'utilisateur ne voit que ces donnees
           #produits = Produit.objects.filter(auteur=user)
        # Pour les filtres ici seul l'utilisateur ne voit que ces donnees dons si on voudrait l'appliquer on
        #  remplace all par filter et on passe l'objet auteur com auteur=user
    produits=Produit.objects.all()
    context = {"produits": produits}
    #print(context)
    return render(request, "produits/produit.html",context)


@login_required(login_url="/login/")
def categories(request):
    # user = request.user;
    # print(user)
    # Pour les filtres ici seul l'utilisateur ne voit que ces donnees
    # produits = Produit.objects.filter(auteur=user)
    # Pour les filtres ici seul l'utilisateur ne voit que ces donnees dons si on voudrait l'appliquer on
    #  remplace all par filter et on passe l'objet auteur com auteur=user
    categories = Categorie.objects.all()
    context = {"categories":  categories}
    print(context)
    return render(request, "pages/index.html", {"categories":  categories})

@login_required(login_url="/login/")
def  parcategorie(request,id):
     categorie= get_object_or_404(Categorie,id=id)
     categorie = Categorie.objects.get(id=id)
     designation=categorie.designation
     print('voici la designation de',designation)

     produits = Produit.objects.filter(categorie_id=categorie.id)
     categories = Categorie.objects.all()
     context = {"produits": produits, "categories": categories}
     print(context)

     return render(request, "categories/categories.html",context)



@login_required(login_url="/login/")
def detail_produits(request,id):
    produit= get_object_or_404(Produit,id=id)
    context = {"produit": produit}
    print(context)
    return render(request, "produits/produit_detail.html",context)

@login_required(login_url="/login/")
def search(request):
    categories = Categorie.objects.all()
    query = request.GET.get('query')
    print(query)
    if not query:
        produits = Produit.objects.all()
    else :
        produits = Produit.objects.filter(designation__icontains=query)
        context = {"produits": produits}
        #print(context)
    return render(request, "produits/search.html", {"produits" : produits ,"categories": categories})

@login_required(login_url="/login/")
def  new_product(request):
    categories= Categorie.objects.all()
    if request.method == "POST" :
        form = Produit(request.POST, request.FILES)
        print("FILES", request.FILES)
        auteur = request.user
        print("auteur ",auteur)
        designation = request.POST['designation']
        description = request.POST['description']
        datePerempt = request.POST['datePerempt']
        prixU = request.POST['prixU']
        quantite = request.POST['quantite']
        photo = request.FILES['photo']
        nom_categorie= request.POST['categorie']
        categorie=Categorie.objects.get(designation=nom_categorie)
        produit= Produit.objects.create(
            designation =designation,
            description =description,
            datePerempt =datePerempt,
            prixU =prixU,
            quantite = quantite,
            photo = photo,
            categorie=  categorie
        )
        context={'categorie':categorie}
        produit.save()

    return render(request, "produits/nouveau_produit.html",{'categories':categories})




@login_required(login_url="/login/")
def  edit_produit(request,id):
    produit = get_object_or_404(Produit,id=id)
    if request.method == "POST" :
        request.POST, request.FILES

        designation = request.POST['designation']
        description = request.POST['description']
        datePerempt = request.POST['datePerempt']
        prixU = request.POST['prixU']
        print("Voici le prix Unitaire =",  prixU)
        quantite = request.POST['quantite']
        print("Voici la quantitee est =", quantite)
        photo = request.FILES['photo']
        #new_path = settings.MEDIA_ROOT + photo
        print("poiuytrewwertyuioiuytrewu",type(photo))
        #path1 = safe_join(os.path.abspath(settings.MEDIA_ROOT) + '\images', photo)
        #print(path1)
        print("Voici la photo",photo)

        print("type  poiuytre",type(produit.photo.url))
        #print("Deuxieme voici ureal de la page", photo.url)
        produit_to_update= Produit.objects.filter(pk=produit.id)
        produit_to_update.update(
            designation =designation,
            description =description,
            datePerempt =datePerempt,
            prixU =prixU,
            quantite = quantite,
            photo = photo
        )
        print("photo",photo)
        print("Derniere affichage url de la page", produit.photo.url)
        return  redirect("/produit")


    return render(request, "produits/edit_produit.html",{"produit" : produit})



@login_required(login_url="/login/")
def  delete_produit(request,id):
    produit = get_object_or_404(Produit,id=id)
    if request.method == "POST" :
        produit.delete()
        return  redirect("/")


    return render(request, "produits/delete_produit.html",{"produit" : produit})


def new_client(request):
        if request.method == "POST":
            clientform = ClientForm(request.POST)
            if clientform.is_valid():
                clientform.save()
                return redirect("/client")
        else:
            clientform = ClientForm()
        return render(request, "clients/new_client.html", {"form":  clientform})


def client(request):
    clients = Client.objects.all()
    context = {"clients":  clients}
    # print(context)
    return render(request, "clients/clients.html",{"clients":  clients} )

def detail_clients(request,id):
    client= get_object_or_404(Client,id=id)
    context = {"client":  client}
    print(context)
    print('voici le nom du client',client.nom)
    return render(request, "clients/client_detail.html",context)
