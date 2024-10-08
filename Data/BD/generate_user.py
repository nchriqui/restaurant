from faker import Faker
import random
import mysql.connector
import bcrypt

from Data.BD.config import config

N = 300

fake = Faker()

# Générer N prénoms aléatoires
firstnames = [fake.first_name() for i in range(N)]

# Générer N noms de famille aléatoires
lastnames = [fake.last_name() for i in range(N)]

# Générer N mots de passe aléatoires
passwords = [bcrypt.hashpw(fake.password(length=random.randrange(20, 41)).encode("utf-8"), bcrypt.gensalt()) for i in range(N)]

# Définir une liste de domaines
domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

# Générer N adresses email aléatoires
mails = []
for i in range(N):
    firstname = firstnames[i]
    lastname = lastnames[i]
    domain = random.choice(domains)
    mails.append("{}{}@{}".format(firstname.lower(), lastname.lower(), domain))

# Créer une connexion à la base de données MySQL
cnx = mysql.connector.connect(**config)

# Créer un curseur pour exécuter les requêtes SQL
cursor = cnx.cursor()

# Insérer les données dans la table users
for i in range(N):
    # Générer un nombre aléatoire
    random_number = random.randint(1, 1000)

    # Vérifier si l'adresse e-mail existe déjà dans la base de données
    query = "SELECT COUNT(*) FROM users WHERE mail = %s"
    data = (mails[i], )
    cursor.execute(query, data)
    result = cursor.fetchone()

    if result[0] > 0:
        # Ajouter un nombre à la fin de l'adresse e-mail
        mails[i] = "{}{}{}@{}".format(firstnames[i].lower(), lastnames[i].lower(), random_number, domain)

    query = "INSERT INTO users (lastname, firstname, password, mail) VALUES (%s, %s, %s, %s)"
    data = (lastnames[i], firstnames[i], passwords[i], mails[i])
    cursor.execute(query, data)

# Valider les modifications dans la base de données
cnx.commit()

# Fermer la connexion et le curseur
cursor.close()
cnx.close()

