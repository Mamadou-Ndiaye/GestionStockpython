from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from  gestionCommande.models import  Produit

# Create your views here.

@login_required(login_url="/login")
def cart_add(request, id):
    user = request.user;
    cart = Cart(request)
    produit = Produit.objects.get(id=id)
    print("Id du produit =",produit.id)
    cart.add(product=produit.id,quantity=produit.quantite)
    return redirect("/")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    produit = Produit.objects.get(id=id)
    cart.remove(produit)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    produit = Produit.objects.get(id=id)
    cart.add(produit=produit)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    produit = Produit.objects.get(id=id)
    cart.decrement(Produit=produit)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')