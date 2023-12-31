# Client - Projet SAE3.02

Bienvenue dans le dossier du client du projet SAE3.02. Ce client graphique est conçu pour interagir avec le serveur du projet, offrant diverses fonctionnalités. Voici une explication des fichiers et des fonctionnalités du client.

## Fonctionnalités du Client

- [x] Login / Register Systeme

- [x] Possibilité d'envoyer des messages privés et des messages dans les channels

- [x] Demande pour rejoindre des Channels

- [x] Mise en Cache des Messages

- [x] Notifications Kill du Serveur

- [x] Notifications Ban / Kick

- [x] Affichage de l'username en haut de la fenêtre

- [x] Gestion des erreurs

- [x] Affichage des status de tous les users en direct

- [ ] Chiffrage des données pendant la communication avec le serveur

- [ ] Bouton logout (La logique est faite, il manque le bouton)

- [ ] Possibilité de faire des commandes depuis le client (La logique est aussi faite, il manque juste un peu de code)

## Structure des Fichiers

### 1. **main.py**
   - Ce fichier permet de lancer le client.
   - Gère les options de ligne de commande :
      - `-i` : spécifie l'adresse IP pour connecter le socket vers le serveur.
      - `-p` : spécifie le port où le client se connecte.
      - `-h` : affiche l'aide.
   - Exemple de commande :
      ```bash
      python3 main.py -i 192.168.1.19 -p 6530
      ```

### 2. **client.py**
   - Ce fichier contient la classe principale du client.
   - Gère les sockets, les interfaces graphiques, etc.
   - Est instancié et lancé dans le fichier `main.py`.

### 3. **requirements.txt**
   - Contient les dépendances nécessaires pour exécuter le client.
   - Utilisez la commande suivante pour installer les dépendances :
      ```bash
      pip install -r requirements.txt
      ```

