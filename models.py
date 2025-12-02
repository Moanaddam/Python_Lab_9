class Produit:
    def __init__(self, nom, prix, id_produit=None):
        self.id = id_produit
        self.nom = nom
        self.prix = prix

    def __str__(self):
        return f"[Produit #{self.id}] {self.nom} - {self.prix} €"

class Client:
    def __init__(self, nom, email, id_client=None):
        self.id = id_client
        self.nom = nom
        self.email = email

    def __str__(self):
        return f"[Client #{self.id}] {self.nom} ({self.email})"