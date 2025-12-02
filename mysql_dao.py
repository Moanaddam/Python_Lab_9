import mysql.connector
from models import Produit, Client
from dao_interface import DaoInterface

class MysqlDao(DaoInterface):
    def __init__(self, host="localhost", user="root", password="", database="boutique"):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        # On tente de créer la base si elle n'existe pas (nécessite des droits)
        self._creer_base_si_absente()
        self.initialiser_tables()

    def _creer_base_si_absente(self):
        try:
            # Connexion sans base spécifiée pour créer la DB
            temp_config = self.config.copy()
            del temp_config['database']
            conn = mysql.connector.connect(**temp_config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            conn.close()
        except mysql.connector.Error as e:
            print(f"⚠️ Erreur connexion initiale MySQL : {e}")

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def initialiser_tables(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL,
                    prix DECIMAL(10, 2) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print(f"❌ Erreur création tables MySQL : {e}")

    def ajouter_produit(self, p):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produits (nom, prix) VALUES (%s, %s)", (p.nom, p.prix))
            conn.commit()
            conn.close()
            print("✅ Produit ajouté (MySQL).")
        except mysql.connector.Error as e:
            print(f"❌ Erreur MySQL : {e}")

    def ajouter_client(self, c):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients (nom, email) VALUES (%s, %s)", (c.nom, c.email))
            conn.commit()
            conn.close()
            print("✅ Client ajouté (MySQL).")
        except mysql.connector.Error as e:
            print(f"❌ Erreur MySQL : {e}")

    def lister_produits(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produits")
        rows = cursor.fetchall()
        conn.close()
        return [Produit(id_produit=row[0], nom=row[1], prix=row[2]) for row in rows]

    def lister_clients(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        conn.close()
        return [Client(id_client=row[0], nom=row[1], email=row[2]) for row in rows]

    def rechercher_client_email(self, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE email = %s", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Client(id_client=row[0], nom=row[1], email=row[2])
        return None

    def modifier_prix_produit(self, id_produit, nouveau_prix):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE produits SET prix = %s WHERE id = %s", (nouveau_prix, id_produit))
            conn.commit()
            if cursor.rowcount > 0:
                print("✅ Prix mis à jour.")
            else:
                print("⚠️ Produit non trouvé.")
            conn.close()
        except mysql.connector.Error as e:
            print(f"❌ Erreur : {e}")