# Serveur - Projet SAE3.02

Bienvenue dans le dossier du serveur du projet SAE3.02. Le serveur gère les connexions avec la base de données, les utilisateurs, les channels, etc. Voici une explication des fichiers et des fonctionnalités du serveur.

## Fonctionnalités du Serveur

- [x] Gestion des erreurs
- [x] Kill du serveur
- [x] Authentification directe depuis le serveur pour le compte admin
- [x] Possibilité d'effectuer des commandes sur le serveur
- [x] Possibilité d'accepter / refuser des demandes pour rejoindre des channels des utilisateurs en temps réel
- [x] Possibilité de ban / kick des utilisateurs directement avec des commandes
- [x] Libérer de l'espace à la déconnexion des utilisateurs si le serveur a atteint le nombre max d'utilisateurs en simultané
- [ ] Hashage des mots de passe dans la base de données
- [ ] Interface graphique
- [ ] Déconnexion du compte admin


## Structure des Fichiers

### 1. **main.py**
   - Ce fichier permet de lancer le serveur.
   - Gère les options de ligne de commande :
      - `-i` : spécifie l'adresse IP du serveur.
      - `-p` : spécifie le port du serveur.
      - `-u` : spécifie le nombre maximal d'utilisateurs simultanés sur le serveur.
      - `-b` : spécifie l'adresse IP de la base de données.
   - Exemple de commande :
      ```bash
      python3 main.py -i 192.168.1.19 -p 6530 -u 3 -b 127.0.0.1
      ```

### 2. **server.py**
   - Ce fichier contient la classe principale du serveur.
   - Gère le serveur socket qui interagit avec les clients.
   - Lancé par le fichier `main.py`.

### 3. **helper.py**
   - Ce fichier gère la connexion avec la base de données et toutes les fonctions avec des requêtes SQL.

### 4. **requirements.txt**
   - Contient les dépendances nécessaires pour exécuter le serveur.
   - Utilisez la commande suivante pour installer les dépendances :
      ```bash
      pip install -r requirements.txt
      ```


