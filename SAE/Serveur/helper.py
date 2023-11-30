import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

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
        rq = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(rq, (user,))
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

def check_ip_exist(ip, connexion):
    """
    Check si l'ip existe dans la table user
    :param ip: Ip à tester
    :param connexion: La connexion à la Base de Données
    :return: True si existe, sinon False
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT * FROM Users WHERE ip = %s"
        cursor.execute(rq, (ip,))
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
        rq = "INSERT INTO Users (username, password, ip) VALUES (%s, %s, %s)"
        cursor.execute(rq, (user, password, ip))
        connexion.commit()
    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de l'ajout de l'utilisateur : {err}")


def get_channel_id(channel_name, connexion):
    """
    Permet de récuperer le channelID du channel
    :param channel_name: Nom du channel
    :param connexion: La connexion à la Base de Données
    :return: ChannelID si existe sinon None
    """
    cursor = connexion.cursor()

    try:
        rq = "SELECT channelID FROM Channels WHERE channel_name = %s"
        cursor.execute(rq, (channel_name,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération de l'ID du canal : {err}")
        return None

    finally:
        cursor.close()


def get_user_id(user, connexion):
    """
    Permet de récuperer l'userID de l'user
    :param user: Username de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: UserID si existe sinon None
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT userID FROM Users WHERE username = %s"
        cursor.execute(rq, (user,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération de l'userID : {err}")
        return None

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
        rq = "SELECT * FROM Users WHERE username = %s AND status = 'ban'"
        cursor.execute(rq, (user,))
        result_user = cursor.fetchone()
        if result_user:
            return True

        rq = "SELECT * FROM Users WHERE ip = %s AND status = 'ban'"
        cursor.execute(rq, (ip,))
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
        rq = "SELECT timestamp FROM Users WHERE username = %s AND status = 'kick'"
        cursor.execute(rq, (user,))
        result_user = cursor.fetchone()

        if result_user:
            return True, result_user[0]

        rq = "SELECT timestamp FROM Users WHERE ip = %s AND status = 'kick'"
        cursor.execute(rq, (ip,))
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
    "liste , avec dedans une liste a chaque fois comprennant requests_id,channel ,username"

def set_status_channel_rq(connexion, accept=False, refuse=False, request_id=None):
    if accept:
        ...
    if refuse:
        ...

def get_all_user_name(connexion):
    """
    Récupère la liste de tous les users de la base de données
    :param connexion: Connexion avec la base de données
    :return: La liste des users si tout est bon, sinon None
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT username FROM Users"
        cursor.execute(rq)
        results = cursor.fetchall()
        usernames = [result[0] for result in results]
        return usernames

    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des usernames : {err}")
        return None

    finally:
        cursor.close()

def ban_user(user=None, ip=None, connexion=None):
    """
    Permet de ban un username / une ip

    :param user: Username de l'utilisateur
    :param ip: L'ip a ban
    :param connexion: La connexion à la Base de Données
    :return: True si c'est bon, sinon False
    """
    cursor = connexion.cursor()

    try:
        if user:
            user_exist = check_user_exist(user, connexion)
            if not user_exist:
                return False
        if ip:
            ip_exist = check_ip_exist(ip, connexion)
            if not ip_exist:
                return False

        if ip:
            rq_ban_ip = "UPDATE Users SET status = 'ban' WHERE ip = %s"
            cursor.execute(rq_ban_ip, (ip,))

        if user:
            rq_ban_user = "UPDATE Users SET status = 'ban' WHERE username = %s"
            cursor.execute(rq_ban_user, (user,))

        connexion.commit()
        return True

    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors du bannissement : {err}")
        return False

    finally:
        cursor.close()


def kick_user(user=None, ip=None, duree: int = None, connexion= None):
    """
    Permet de kick un username / une ip pendant un nombre d'heure défini

    :param user: Username de l'utilisateur
    :param ip: L'ip a kick
    :param duree: Nombre d'heure de kick
    :param connexion: La connexion à la Base de Données
    :return: True, Date si c'est bon, sinon False
    """
    cursor = connexion.cursor()
    next_login = (datetime.now() + timedelta(hours=duree)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        if user:
            user_exist = check_user_exist(user, connexion)
            if not user_exist:
                return False
        if ip:
            ip_exist = check_ip_exist(ip, connexion)
            if not ip_exist:
                return False

        if user:
            rq_kick_target = "UPDATE Users SET status = 'kick', timestamp = %s WHERE username = %s"
            cursor.execute(rq_kick_target, (next_login, user))
        elif ip:
            rq_kick_target = "UPDATE Users SET status = 'kick', timestamp = %s WHERE ip = %s"
            cursor.execute(rq_kick_target, (next_login, ip))

        connexion.commit()
        return True, next_login

    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors du kick de l'adresse IP ou de l'utilisateur : {err}")
        return False

    finally:
        cursor.close()


def save_channel_message(username, channel_name, message, connexion):
    """
    Permet de sauvegarder un message envoyé dans un channel par un membre
    :param username: Username de l'émetteur du message
    :param channel_name: Nom du channel où le message a été envoyé
    :param message: Message envoyé
    :param connexion: Connexion avec la base de donnée
    :return: True si c'est bon sinon False
    """
    cursor = connexion.cursor()
    try:
        channel_id = get_channel_id(channel_name, connexion)
        user_id = get_user_id(username, connexion)

        if not channel_id or not user_id:
            return False

        rq = "INSERT INTO Messages (senderID, channelID, content, timestamp) VALUES (%s, %s, %s, %s)"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(rq, (user_id, channel_id, message, timestamp))

        connexion.commit()
        return True

    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de la sauvegarde du message : {err}")
        return False

    finally:
        cursor.close()

def save_private_message(username, other_user, message, connexion):
    """
    Permet de sauvegarder un message privé entre le membre 1 et le membre 2 dans la base de donnée
    :param username: Username de l'émetteur du message
    :param other_user: Username du recepteur du message
    :param message: Message envoyé
    :param connexion: Connexion avec la base de donnée
    :return: True si c'est bon sinon False
    """
    cursor = connexion.cursor()
    try:
        user_id = get_user_id(username, connexion)
        other_id = get_user_id(other_user, connexion)

        if not user_id or not other_id:
            return False

        rq = "INSERT INTO Messages (senderID, receiverID, content, timestamp) VALUES (%s, %s, %s, %s)"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(rq, (user_id, other_id, message, timestamp))

        connexion.commit()
        return True

    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de la sauvegarde du message privé : {err}")
        return False

    finally:
        cursor.close()

def get_user_pwd(user, connexion):
    """
    Récupere l'username et le mot de passe d'un user

    :param user: Username de l'utilisateur
    :param connexion: La connexion à la Base de Données
    :return: Username:Password si trouvé sinon None
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT password FROM Users WHERE username = %s"
        cursor.execute(rq, (user,))
        result = cursor.fetchone()
        if result:
            password = result[0]
            return f"user:{password}"
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération du mot de passe : {err}")
        return None

    finally:
        cursor.close()

def get_channel_acceptation(channel_name, connexion):
    """
    Permet de récupérer si le channel a besoin de faire une requête pour être rejoins
    :param channel_name: Le nom du channel
    :param connexion: La connexion a la bdd
    :return: renvoie le resultat si c'est bon sinon None
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT need_accept FROM Channels WHERE channel_name = %s"
        cursor.execute(rq, (channel_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération du champ 'need_accept' : {err}")
        return None

    finally:
        cursor.close()
