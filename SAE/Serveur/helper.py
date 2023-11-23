import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta, date

"""
La plupart des fonctions d'acces a la base de donnée
"""

def check_bdd(host):
    """
    Permet de check si la base de données est accessible, se connecte et renvoi le curseur

    :param host: Ip de la base de donnée
    :return: Connexion si c'est bon sinon False
    """
    try:
        connexion = mysql.connector.connect(
            host=host,
            user="Server",
            password="4dm1n",
            database="SAE"
        )

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur d'authentification : Vérifiez votre nom d'utilisateur et votre mot de passe.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Base de données non existante : Vérifiez le nom de la base de données.")
        else:
            print(f"Erreur MySQL non gérée : {err}")
        return False
    else:
        return connexion


def check_user_exist(user, connexion):
    """
    Check si l'user existe dans la table user
    :param user: Username de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: True si existe, sinon False
    """
    cursor = connexion.cursor()
    try:
        query = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Erreur lors de la vérification de l'existence de l'username : {err}")
        return False
    finally:
        cursor.close()

def register_user(user, password, ip, connexion):
    """
    Créer un user dans la table user, ajoute son mot de passe et son ip

    :param user: Username de l'utilisateur
    :param password: Le mot de passe de l'utilisateur
    :param ip: L'ip de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return:
    """
    cursor = connexion.cursor()
    try:
        query = "INSERT INTO Users (username, password, ip) VALUES (%s, %s, %s)"
        cursor.execute(query, (user, password, ip))
        connexion.commit()
    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de l'ajout de l'utilisateur : {err}")


def get_channel_id(channel_name, connexion):
    cursor = connexion.cursor()


def get_user_id(user, connexion):
    """
    Permet de récuperer l'userID de l'user
    :param user: Username de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: UserID si existe sinon None
    """
    cursor = connexion.cursor()
    try:
        query = "SELECT userID FROM Users WHERE username = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération de l'userID : {err}")
    finally:
        cursor.close()

def check_ban(user, ip, connexion):
    """
    Permet de check si une ip ou un utilisateur est banni

    :param user: Username de l'utilisateur
    :param ip: Ip de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: True si l'user ou l'ip est ban, False sinon
    """
    cursor = connexion.cursor()
    try:
        query_user = "SELECT * FROM Users WHERE username = %s AND status = 'ban'"
        cursor.execute(query_user, (user,))
        result_user = cursor.fetchone()
        if result_user:
            return True

        query_ip = "SELECT * FROM Users WHERE ip = %s AND status = 'ban'"
        cursor.execute(query_ip, (ip,))
        result_ip = cursor.fetchone()

        if result_ip:
            return True

        return False

    except mysql.connector.Error as err:
        print(f"Erreur lors de la vérification du bannissement : {err}")
        return False

    finally:
        cursor.close()

def check_kick(user, ip, connexion):
    """
    Permet de check si une ip ou un utilisateur est kick

    :param user: Username de l'utilisateur
    :param ip: Ip de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: True, Date si l'user ou l'ip est kick , avec la date a laquelle il pourra se relogin, False, None sinon
    """

    cursor = connexion.cursor()
    try:
        query_user = "SELECT timestamp FROM Users WHERE username = %s AND status = 'kick'"
        cursor.execute(query_user, (user,))
        result_user = cursor.fetchone()

        if result_user:
            return True, result_user[0]

        query_ip = "SELECT timestamp FROM Users WHERE ip = %s AND status = 'kick'"
        cursor.execute(query_ip, (ip,))
        result_ip = cursor.fetchone()

        if result_ip:
            return True, result_ip[0]

        return False, None

    except mysql.connector.Error as err:
        print(f"Erreur lors de la vérification du kick : {err}")
        return False, None

    finally:
        cursor.close()

def get_channel_rq(connexion):
    cursor = connexion.cursor()

def get_all_user_name(connexion):
    cursor = connexion.cursor()

def ban_user(user=None, ip=None, connexion=None):
    cursor = connexion.cursor()

    try:
        if ip:
            query_ip_exist = "SELECT * FROM Users WHERE ip = %s"
            cursor.execute(query_ip_exist, (ip,))
            result_ip_exist = cursor.fetchone()
            if not result_ip_exist:
                return False

        if user:
            query_user_exist = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query_user_exist, (user,))
            result_user_exist = cursor.fetchone()
            if not result_user_exist:
                return False

        if ip:
            query_ban_ip = "UPDATE Users SET status = 'ban' WHERE ip = %s"
            cursor.execute(query_ban_ip, (ip,))

        if user:
            query_ban_user = "UPDATE Users SET status = 'ban' WHERE username = %s"
            cursor.execute(query_ban_user, (user,))

        connexion.commit()
        return True

    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors du bannissement : {err}")
        return False

    finally:
        cursor.close()


def kick_user(user, duree: int, connexion):
    cursor = connexion.cursor()
    next_login = (datetime.now() + timedelta(hours=duree)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        query_user_exist = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(query_user_exist, (user,))
        result_user_exist = cursor.fetchone()

        if not result_user_exist:
            return False

        query_kick_user = "UPDATE Users SET status = 'kick', timestamp = %s WHERE username = %s"
        cursor.execute(query_kick_user, (next_login, user))

        connexion.commit()
        return True, next_login

    except mysql.connector.Error as err:
        print(f"Erreur lors du kick de l'utilisateur : {err}")
        connexion.rollback()
        return False

    finally:
        cursor.close()

def save_channel_message(username, channel_name, message, connexion):
    cursor = connexion.cursor()

def save_private_message(username, other_user, message, connexion):
    cursor = connexion.cursor()

def get_user_pwd(user, connexion):
    """
    Récupere l'username et le mot de passe d'un user

    :param user: Username de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: Username:Password si trouvé sinon None
    """
    cursor = connexion.cursor()
    try:
        query = "SELECT password FROM Users WHERE username = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        if result:
            password = result[0]
            return f"user:{password}"
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération du mot de passe : {err}")
    finally:
        cursor.close()
