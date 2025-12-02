import sqlite3
from models import Produit, Client
from dao_interface import DaoInterface

class SqliteDao(DaoInterface):
    def __init__(self, db_name="boutique.db"):
        self.db_name = db_name
        self.initialiser_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def initialiser_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prix REAL NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()

    def ajouter_produit(self, p):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO produits (nom, prix) VALUES (?, ?)", (p.nom, p.prix))
                conn.commit()
                print("✅ Produit ajouté (SQLite).")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")

    def ajouter_client(self, c):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clients (nom, email) VALUES (?, ?)", (c.nom, c.email))
                conn.commit()
                print("✅ Client ajouté (SQLite).")
        except sqlite3.IntegrityError:
            print("❌ Erreur : Cet email existe déjà.")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")

    def lister_produits(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produits")
            rows = cursor.fetchall()
            return [Produit(id_produit=row[0], nom=row[1], prix=row[2]) for row in rows]

    def lister_clients(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients")
            rows = cursor.fetchall()
            return [Client(id_client=row[0], nom=row[1], email=row[2]) for row in rows]

    def rechercher_client_email(self, email):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return Client(id_client=row[0], nom=row[1], email=row[2])
            return None

    def modifier_prix_produit(self, id_produit, nouveau_prix):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE produits SET prix = ? WHERE id = ?", (nouveau_prix, id_produit))
                if cursor.rowcount > 0:
                    print("✅ Prix mis à jour.")
                else:
                    print("⚠️ Produit non trouvé.")
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Erreur : {e}")