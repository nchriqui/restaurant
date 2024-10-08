import mysql.connector
import bcrypt

from Data.BD.config import config

def new_user(lastname, firstname, password, mail):
    if lastname == "" or firstname == "" or password == "" or mail == "":
        return -1
    
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Vérifier si l'adresse e-mail existe déjà dans la base de données
    query = "SELECT COUNT(*) FROM users WHERE mail = %s"
    data = (mail, )
    cursor.execute(query, data)
    result = cursor.fetchone()[0]

    if result > 0:
        return -2

    # Génération du hachage sécurisé
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # hashed_password = hashed_password.decode('utf-8')

    query = "INSERT INTO users (lastname, firstname, password, mail) VALUES (%s, %s, %s, %s)"

    data = (lastname, firstname, hashed_password, mail)
    cursor.execute(query, data)

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    return 0

def get_user(password, mail):
    if password == "" or mail == "":
        return -1
    
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Récupérer les données de l'utilisateur
    query = """
    SELECT *
    FROM users u
    WHERE u.mail = %s;
    """

    data = (mail, )
    cursor.execute(query, data)

    # Récupérer les résultats de la requête
    result = cursor.fetchone()

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    if result is None:
        return -1
    
    user_id = result[0]
    lastname = result[1]
    firstname = result[2]
    stored_hashed_password = result[3]
    mail = result[4]
    balance = result[5]    

    # Vérification du mot de passe
    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        print("Mot de passe correct")
        return user_id
    else:
        print("Mot de passe incorrect")
        return -1

def update_password(password, mail):
    if password == "" or mail == "":
        return -1
    
    # Créer une connexion à la base de données MySQL
    cnx = mysql.connector.connect(**config)

    # Créer un curseur pour exécuter les requêtes SQL
    cursor = cnx.cursor()

    # Vérifier si l'adresse e-mail existe dans la base de données
    query = "SELECT COUNT(*) FROM users WHERE mail = %s"
    data = (mail, )
    cursor.execute(query, data)
    result = cursor.fetchone()[0]

    # Existe pas
    if result == 0:
        return -2

    # Génération du hachage sécurisé
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # hashed_password = hashed_password.decode('utf-8')

    query = "UPDATE users SET password = %s WHERE mail = %s"

    data = (hashed_password, mail)
    cursor.execute(query, data)

    # Valider les modifications dans la base de données
    cnx.commit()

    # Fermer la connexion et le curseur
    cursor.close()
    cnx.close()

    return 0