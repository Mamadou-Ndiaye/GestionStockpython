from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from django.db import models



class Categorie(models.Model):
    designation = models.CharField(max_length=30)
    description = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return  f"{self.designation} {self.description}"


class Produit(models.Model):
    designation = models.CharField(max_length=30)
    description = models.CharField(max_length=30,null=True)
    datePerempt = models.DateField()
    prixU = models.IntegerField()
    quantite = models.IntegerField()
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    #auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, null=True, blank=True, on_delete=models.CASCADE)
    #archive = models.BooleanField(default=False)
    def __str__(self):
        return  f"{self.designation} {self.datePerempt} {self.prixU} {self.quantite}"

class Client(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=30)



class Commande(models.Model):
    dateCommande = models.DateField()
    statut = models.BooleanField(max_length=25)
    details = models.ManyToManyField(Produit, through='DetailCommande')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.dateCommande} {self.statut} {self.details}"



    def __str__(self):
        return  f"{self.nom} {self.prenom} {self.email} {self.telephone} {self.adresse}"

class DetailCommande(models.Model):
    quantite = models.IntegerField()
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.quantite} {self.commande} {self.produit}"

class Compte(models.Model):
    login = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    status = models.CharField(max_length=7)

    def __str__(self):
        return  f"{self.login} {self.password} {self.status}"

class Facture(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    montant = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return  f"{self.commande} {self.montant} {self.date}"


