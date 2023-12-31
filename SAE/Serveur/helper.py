import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

"""
La plupart des fonctions d'accès à la base de données
"""

"""
//////////////////////////////////

FONCTIONS CHECK (PERMETTANT DE VÉRIFIER UNE INFORMATION DANS LA BASE DE DONNÉES)

//////////////////////////////////
"""


def check_bdd(host):
    """
    Vérifie si la base de données est accessible, se connecte et renvoie le curseur

    :param host: Adresse IP de la base de données
    :return: Connexion si réussie, sinon False
    """
    try:
        connexion = mysql.connector.connect(
            host=host,
            user="Server",
            password="4dm1n",
            database="SAE",
            connect_timeout=2
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Accès refusé. Vérifiez votre nom d'utilisateur ou votre mot de passe.") # Ne doit pas apparaitre sauf si mal config coté server
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de données spécifiée n'existe pas.")
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            print("Impossible de se connecter au serveur mysql (mauvaise ip ?).")
        elif err.errno == errorcode.CR_CONNECTION_ERROR:
            print("Erreur de connexion à la base de données.")
        elif err.errno == errorcode.CR_SERVER_LOST:
            print("La connexion au serveur MySQL a été perdue.")
        else:
            print(f"Erreur MySQL: {err}")
        return False
    else:
        return connexion


def check_user_exist(user, connexion):
    """
    Vérifie si l'utilisateur existe dans la table 'Users'

    :param user: Nom d'utilisateur
    :param connexion: Connexion à la base de données
    :return: True si l'utilisateur existe, sinon False
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
    Vérifie si l'adresse IP existe dans la table 'Users'

    :param ip: Adresse IP à tester
    :param connexion: Connexion à la base de données
    :return: True si l'adresse IP existe, sinon False
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT * FROM Users WHERE ip = %s"
        cursor.execute(rq, (ip,))
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Erreur lors de la vérification de l'existence de l'username : {err}")
        return False
    finally:
        cursor.close()


def check_ban(user, ip, connexion):
    """
    Vérifie si un utilisateur ou une adresse IP est banni

    :param user: Nom d'utilisateur
    :param ip: Adresse IP de l'utilisateur
    :param connexion: Connexion à la base de données
    :return: True si l'utilisateur ou l'adresse IP est banni, False sinon
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT * FROM Users WHERE username = %s AND status = 'ban'"
        cursor.execute(rq, (user,))
        result_user = cursor.fetchone()
        if result_user:
            return True

        ip_exist = check_ip_exist(ip, connexion)
        if not ip_exist:
            return False

        rq = "SELECT * FROM Users WHERE ip = %s AND status != 'ban'"
        cursor.execute(rq, (ip,))
        result_ip = cursor.fetchall()

        if not result_ip:
            return True

        return False

    except mysql.connector.Error as err:
        print(f"Erreur lors de la vérification du bannissement : {err}")
        return False

    finally:
        cursor.close()


def check_kick(user, ip, connexion):
    """
    Vérifie si un utilisateur ou une adresse IP est kick

    :param user: Nom d'utilisateur
    :param ip: Adresse IP de l'utilisateur
    :param connexion: Connexion à la base de données
    :return: True, Date si l'utilisateur ou l'adresse IP est kick, False, None sinon
    """

    cursor = connexion.cursor()
    try:
        rq = "SELECT timestamp FROM Users WHERE username = %s AND status = 'kick'"
        cursor.execute(rq, (user,))
        result_user = cursor.fetchone()

        if result_user:
            return True, result_user[0].strftime('%Y-%m-%d %H:%M:%S')

        ip_exist = check_ip_exist(ip, connexion)
        if not ip_exist:
            return False, None

        rq = "SELECT * FROM Users WHERE ip = %s AND status != 'kick'"
        cursor.execute(rq, (ip,))
        result_ip = cursor.fetchall()
        if not result_ip:
            rq = "SELECT timestamp FROM Users WHERE ip = %s AND status = 'kick'"
            cursor.execute(rq, (ip,))
            result_ip = cursor.fetchall()
            return True, result_ip[0][0].strftime('%Y-%m-%d %H:%M:%S')

        return False, None


    except mysql.connector.Error as err:
        print(f"Erreur lors de la vérification du kick : {err}")
        return False, None

    finally:
        cursor.close()


"""
//////////////////////////////////

FONCTIONS SET (PERMETTANT DE MODIFIER LA BASE DE DONNÉES)

//////////////////////////////////
"""

def set_new_channel_rq(connexion, username, channel_name, status="pending"):
    """
    Ajoute une nouvelle requête pour rejoindre un channel

    :param connexion: Connexion à la base de données
    :param username: Nom de l'utilisateur faisant la demande
    :param channel_name: Nom du channel pour lequel la demande est faite
    """

    user_id = get_user_id(username, connexion)
    channel_id = get_channel_id(channel_name, connexion)

    cursor = connexion.cursor()

    try:
        rq = "INSERT INTO ChannelRequests (channelID, userID, status) VALUES (%s, %s, %s)"
        cursor.execute(rq, (channel_id, user_id, status))

        connexion.commit()
    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de l'ajout de la nouvelle requête vers le channel : {err}")
        return
    finally:
        cursor.close()


def set_status_channel_rq(connexion, accept=False, refuse=False, request_id=None):
    """
    Définit le statut d'une requête pour rejoindre un channel

    :param connexion: Connexion à la base de données
    :param accept: True si la demande doit être acceptée
    :param refuse: True si la demande doit être refusée
    :param request_id: ID de la requête à modifier
    """
    if not (accept or refuse) or (accept and refuse):
        return

    status = 'pending'
    if accept:
        status = 'accept'
    elif refuse:
        status = 'refuse'

    cursor = connexion.cursor()

    try:
        rq = "UPDATE ChannelRequests SET status = %s WHERE requestID = %s"
        cursor.execute(rq, (status, request_id))
        connexion.commit()

    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de la mise a jour de la requete vers le channel: {err}")
        return
    finally:
        cursor.close()


def ban_user(user=None, ip=None, connexion=None):
    """
    Bannit un utilisateur ou une adresse IP

    :param user: Nom d'utilisateur
    :param ip: Adresse IP à bannir
    :param connexion: Connexion à la base de données
    :return: True si réussi, False sinon
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


def kick_user(user=None, ip=None, duree: int = None, connexion=None):
    """
    Kick un utilisateur ou une adresse IP pendant une durée définie

    :param user: Nom d'utilisateur
    :param ip: Adresse IP à kicker
    :param duree: Nombre d'heures du kick
    :param connexion: Connexion à la base de données
    :return: True, Date si réussi, False sinon
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
            rq = "UPDATE Users SET status = 'kick', timestamp = %s WHERE username = %s"
            cursor.execute(rq, (next_login, user))
        elif ip:
            rq = "UPDATE Users SET status = 'kick', timestamp = %s WHERE ip = %s"
            cursor.execute(rq, (next_login, ip))

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
    Sauvegarde un message envoyé dans un channel par un membre

    :param username: Nom de l'émetteur du message
    :param channel_name: Nom du channel où le message a été envoyé
    :param message: Message envoyé
    :param connexion: Connexion à la base de données
    :return: True si réussi, False sinon
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
    Sauvegarde un message privé entre deux membres dans la base de données

    :param username: Nom de l'émetteur du message
    :param other_user: Nom du destinataire du message
    :param message: Message envoyé
    :param connexion: Connexion à la base de données
    :return: True si réussi, False sinon
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


def register_user(user, password, ip, connexion):
    """
    Crée un utilisateur dans la table 'Users', ajoute son mot de passe et son adresse IP

    :param user: Nom d'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param ip: Adresse IP de l'utilisateur
    :param connexion: Connexion à la base de données
    """
    cursor = connexion.cursor()
    try:
        rq = "INSERT INTO Users (username, password, ip) VALUES (%s, %s, %s)"
        cursor.execute(rq, (user, password, ip))
        connexion.commit()
    except mysql.connector.Error as err:
        connexion.rollback()
        print(f"Erreur lors de l'ajout de l'utilisateur : {err}")


"""
//////////////////////////////////

FONCTIONS GET (PERMETTANT DE RÉCUPÉRER DES INFORMATIONS DE LA BASE DE DONNÉES)

//////////////////////////////////
"""


def get_user_pwd(user, connexion):
    """
    Récupère le mot de passe d'un utilisateur

    :param user: Nom d'utilisateur
    :param connexion: Connexion à la base de données
    :return: Nom d'utilisateur, Mot de passe, sinon None
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT password FROM Users WHERE username = %s"
        cursor.execute(rq, (user,))
        result = cursor.fetchone()
        if result:
            password = result[0]
            return user, password
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération du mot de passe : {err}")
        return None

    finally:
        cursor.close()


def get_channel_acceptation(channel_name, connexion):
    """
    Récupère si le channel nécessite une demande d'acceptation pour rejoindre.
    :param channel_name: Le nom du channel
    :param connexion: Connexion à la base de données
    :return: Renvoie le résultat si réussi, sinon None
    """
    cursor = connexion.cursor()
    try:
        rq = "SELECT need_accept FROM Channels WHERE channel_name = %s"
        cursor.execute(rq, (channel_name,))
        result = cursor.fetchone()
        if result:
            return result[0] if result[0] != 'None' else None
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération du champ 'need_accept' : {err}")
        return None

    finally:
        cursor.close()


def get_all_user_name(connexion):
    """
    Récupère la liste de tous les utilisateurs de la base de données.
    :param connexion: Connexion à la base de données
    :return: La liste des noms d'utilisateur si réussi, sinon None
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


def get_channel_rq(connexion):
    """
    Cette fonction est utilisée par le serveur pour récupérer toutes les demandes pour rejoindre des canaux.
    :param connexion: Connexion à la base de données
    :return: Une liste de listes contenant ['request_id', 'channel_name', 'username']
    """
    result = []

    cursor = connexion.cursor()

    try:
        rq = "SELECT * FROM ChannelRequests"
        cursor.execute(rq)

        for row in cursor.fetchall():
            request_id, channel_id, user_id, status = row

            if status == 'pending':
                rq = "SELECT channel_name FROM Channels WHERE channelID = %s"
                cursor.execute(rq, (channel_id,))
                channel_name = cursor.fetchone()[0]

                rq = "SELECT username FROM Users WHERE userID = %s"
                cursor.execute(rq, (user_id,))
                username = cursor.fetchone()[0]

                result.append([request_id, channel_name, username])

    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération : {err}")
        return None

    finally:
        cursor.close()

    return result


def get_channel_id(channel_name, connexion):
    """
    Récupère le channelID du channel.
    :param channel_name: Nom du channel
    :param connexion: Connexion à la base de données
    :return: ChannelID s'il existe, sinon None
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
        print(f"Erreur lors de la récupération de l'ID du channel : {err}")
        return None

    finally:
        cursor.close()

def get_joined_channel_rq(connexion, username):
    """
    Récupère les informations des demandes de channel pour un utilisateur donné
    :param connexion: Connexion à la base de données
    :param username: Nom de l'utilisateur
    :return: Dictionnaire avec le nom du channel en clé et le statut en valeur
    """
    cursor = connexion.cursor(dictionary=True)

    try:
        user_id = get_user_id(username, connexion)

        rq = "SELECT Channels.channel_name, ChannelRequests.status " \
             "FROM ChannelRequests " \
             "JOIN Channels ON ChannelRequests.channelID = Channels.channelID " \
             "WHERE ChannelRequests.userID = %s"
        cursor.execute(rq, (user_id,))
        result = cursor.fetchall()

        joined_channels = {row['channel_name']: row['status'] for row in result}

        return joined_channels

    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des demandes de channel pour l'utilisateur : {err}")
        return None
    finally:
        cursor.close()

def get_user_id(user, connexion):
    """
    Permet de récuperer l'userID de l'user
    :param user: Nom d'utilisateur
    :param connexion: Connexion à la base de données
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

if __name__ == "__main__":
    co = check_bdd("192.168.1.11")
    print(co)
    # print(check_user_exist("toto", co))
    # print(register_user("toto2", "toto", "192.168.1.19", co))
    # x = get_channel_acceptation(channel_name="Blabla", connexion=co)
    # if x:
    #     print(x)
    # print(check_ban(user="toto2", ip="192.168.1.1",connexion=co))
    # print(ban_user(user="toto2", connexion=co))
    # print(ban_user(ip="192.168.1.19", connexion=co))
    # print(check_ban(user="toto10", ip="192.168.1.19",connexion=co))
    # print(get_user_id("toto10", connexion=co))
    # print(get_joined_channel_rq(connexion=co, username="toto"))
    # print(get_channel_rq(connexion=co))
    # print(check_ban("toto", "192.168.1.19",connexion=co))
    # print(check_kick(user="toto", ip="192.168.1.19",connexion=co))
    # print(kick_user(ip="192.168.1.19", connexion=co, duree=24))
    # print(check_kick(user="toto", ip="192.168.1.19", connexion=co))
    # print(ban_user(ip="10.0.0.1", connexion=co))
    # print(check_kick("toto","192.168.1.19",connexion=co))