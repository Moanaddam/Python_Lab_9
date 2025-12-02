from models import Produit, Client
from sqlite_dao import SqliteDao
# On importe MySQL uniquement si nécessaire ou on gère l'erreur d'import
try:
    from mysql_dao import MysqlDao
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

def afficher_menu():
    print("\n--- GESTION BOUTIQUE ---")
    print("1. Ajouter un produit")
    print("2. Lister les produits")
    print("3. Modifier prix d'un produit")
    print("4. Ajouter un client")
    print("5. Lister les clients")
    print("6. Rechercher un client (email)")
    print("0. Quitter")

def main():
    print("Choisissez votre base de données :")
    print("1. SQLite (Fichier local)")
    print("2. MySQL (Serveur distant)")
    choix_db = input("Choix : ")

    dao = None
    
    if choix_db == "1":
        print("📁 Mode SQLite activé.")
        dao = SqliteDao()
    elif choix_db == "2":
        if not MYSQL_AVAILABLE:
            print("❌ Le module mysql-connector n'est pas installé.")
            return
        # CONFIGURATION A ADAPTER SELON VOTRE SERVEUR MYSQL
        h = input("Hôte (localhost) : ") or "localhost"
        u = input("Utilisateur (root) : ") or "root"
        p = input("Mot de passe : ")
        print("🌍 Mode MySQL activé.")
        dao = MysqlDao(host=h, user=u, password=p)
    else:
        print("Choix invalide.")
        return

    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom du produit : ")
            prix = float(input("Prix du produit : "))
            p = Produit(nom, prix)
            dao.ajouter_produit(p)

        elif choix == "2":
            produits = dao.lister_produits()
            print("\n--- Liste des produits ---")
            for p in produits:
                print(p)

        elif choix == "3":
            id_p = input("ID du produit : ")
            nouveau_prix = float(input("Nouveau prix : "))
            dao.modifier_prix_produit(id_p, nouveau_prix)

        elif choix == "4":
            nom = input("Nom du client : ")
            email = input("Email du client : ")
            c = Client(nom, email)
            dao.ajouter_client(c)

        elif choix == "5":
            clients = dao.lister_clients()
            print("\n--- Liste des clients ---")
            for c in clients:
                print(c)

        elif choix == "6":
            email = input("Email à rechercher : ")
            client = dao.rechercher_client_email(email)
            if client:
                print(f"✅ Trouvé : {client}")
            else:
                print("❌ Aucun client avec cet email.")

        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix inconnu.")

if __name__ == "__main__":
    main()