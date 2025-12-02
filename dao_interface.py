from abc import ABC, abstractmethod

class DaoInterface(ABC):
    
    @abstractmethod
    def initialiser_tables(self):
        pass

    @abstractmethod
    def ajouter_produit(self, produit):
        pass

    @abstractmethod
    def ajouter_client(self, client):
        pass

    @abstractmethod
    def lister_produits(self):
        pass

    @abstractmethod
    def lister_clients(self):
        pass

    @abstractmethod
    def rechercher_client_email(self, email):
        pass

    @abstractmethod
    def modifier_prix_produit(self, id_produit, nouveau_prix):
        pass