# BDD - Base de Données

Bienvenue dans le dossier BDD du projet SAE3.02. Cette section fournit des instructions pour configurer et utiliser la base de données associée au serveur. Suivez ces étapes pour mettre en place la base de données.

## Schéma Relationnel

Le fichier `schema bdd.PNG` dans ce dossier représente le schéma relationnel de la base de données. Vous pouvez le consulter pour comprendre la structure des tables et les relations entre elles.

## 1/ Configuration du Serveur MySQL

1. **Installer MySQL Server** :
   Assurez-vous que MySQL Server est installé sur votre machine. Si ce n'est pas le cas, vous pouvez le télécharger et l'installer depuis le site officiel de MySQL.

2. **Créer un Serveur MySQL** :
   - Utilisateur : `Server`
   - Mot de passe : `4dm1n`

## 2/ Charger la Base de Données

### Option 1 : Utiliser le Script 'script mysql.txt'

   - Copiez le contenu du fichier `script mysql.txt`.
   - Ouvrez un terminal MySQL.
   - Collez le contenu et exécutez-le pour créer la base de données.

### Option 2 : Utiliser le Dump SQL

   - Utilisez la commande suivante pour créer la base de données `sae` et charger le dump SQL :
     ```bash
     mysql -u Server -p4dm1n -e "CREATE DATABASE IF NOT EXISTS sae;" && mysql -u Server -p4dm1n sae < dump.sql
     ```


