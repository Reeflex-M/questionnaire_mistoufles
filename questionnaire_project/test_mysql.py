import mysql.connector

try:
    # Tentative de connexion
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    
    # Créer la base de données si elle n'existe pas
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS questionnaire_db")
    
    print("Connexion réussie !")
    print("Base de données questionnaire_db créée ou déjà existante")
    
except mysql.connector.Error as err:
    print(f"Erreur: {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion fermée")
