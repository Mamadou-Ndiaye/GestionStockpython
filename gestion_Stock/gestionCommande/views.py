from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from gestionCommande.models import Produit


@login_required(login_url="/login/")
def home(request):
    produits = Produit.objects.all()
    context = {"produits": produits}
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
    print(context)
    return render(request, "produits/produit.html",context)

@login_required(login_url="/login/")
def detail_produits(request,id):
    produit= get_object_or_404(Produit,id=id)
    context = {"produit": produit}
    print(context)
    return render(request, "produits/produit_detail.html",context)

@login_required(login_url="/login/")
def  new_product(request):
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
        #request.FILES['image']
        photo = request.FILES['photo']

        produit= Produit.objects.create(
            designation =designation,
            description =description,
            datePerempt =datePerempt,
            prixU =prixU,
            quantite = quantite,
            auteur = auteur,
            photo = photo
        )

        produit.save()

        return  redirect("/produit/")

    return render(request, "produits/nouveau_produit.html")

@login_required(login_url="/login/")
def  edit_produit(request,id):
    produit = get_object_or_404(Produit,id=id)
    if request.method == "POST" :


        designation = request.POST['designation']
        description = request.POST['description']
        datePerempt = request.POST['datePerempt']
        prixU = request.POST['prixU']
        quantite = request.POST['quantite']
        photo = request.POST['photo']
        produit_to_update= Produit.objects.filter(pk=produit.id)
        produit_to_update.update(
            designation =designation,
            description =description,
            datePerempt =datePerempt,
            prixU =prixU,
            quantite = quantite,
            photo = photo
        )
        return  redirect("/produit")


    return render(request, "produits/edit_produit.html",{"produit" : produit})



@login_required(login_url="/login/")
def  delete_produit(request,id):
    produit = get_object_or_404(Produit,id=id)
    if request.method == "POST" :
        produit.delete()
        return  redirect("/produit")


    return render(request, "produits/delete_produit.html",{"produit" : produit})

