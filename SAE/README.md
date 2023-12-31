# Caractéristiques - Serveur

### Fonctionnalités Actuelles

- **Gestion des Erreurs:** 
  Mise en place d'une gestion d'erreurs optimales permettant la stabilité du serveur, empêchant les crashs.
- **Contrôle du Serveur:** 
  Intégration de fonctionnalités permettant le contrôle du serveur, notamment la possibilité de l'arrêter (Kill) pour des raisons de maintenance.
- **Authentification Admin:** 
  Mise en œuvre d'un mécanisme d'authentification directe depuis le serveur, permettant un accès administratif sécurisé.
- **Commandes Serveur:** 
  Ajout de la capacité d'effectuer diverses commandes directement sur le serveur, améliorant la flexibilité et la gestion.
- **Gestion des Utilisateurs:** 
  Possibilité d'accepter / refuser des demandes pour rejoindre des channels en temps réel, et de bannir / kicker des utilisateurs directement avec des commandes.
- **Gestion en direct du nombre d'utilisateurs:** 
  Libération de places à la déconnexion des utilisateurs lorsque le serveur atteint le nombre maximal d'utilisateurs en simultané.
- **Flexibilité du Code:** 
  Le code a été conçu de manière à faciliter l'ajout de nouvelles fonctionnalités. Il est simple d'améliorer le code et d'ajouter des features pour répondre aux besoins spécifiques.

# Caractéristiques - Client

### Fonctionnalités Actuelles

- **Login / Register Systeme:** 
  Permet aux utilisateurs de créer un compte et de se connecter de manière sécurisée.
- **Envoi de Messages:** 
  Possibilité d'envoyer des messages privés et des messages dans les channels.
- **Demandes pour Rejoindre des Channels:**
  Fonctionnalité pour solliciter l'accès à des channels spécifiques.
- **Mise en Cache des Messages:** 
  Conservation des messages en cache pour une expérience utilisateur fluide.
- **Notifications Kill du Serveur:** 
  Alertes lorsque le serveur est arrêté pour maintenance.
- **Notifications Ban / Kick:** 
  Informations sur les actions de bannissement ou d'expulsion.
- **Affichage de l'Username:** 
  Présentation de l'username en haut de la fenêtre.
- **Gestion des Erreurs:** 
  Prise en charge efficace des erreurs pour une expérience stable.


# Limites / Points d'Amélioration

- **Sécurité des Mots de Passe:**
  Les mots de passe ne sont pas actuellement hashés dans la base de données, ce qui expose les utilisateurs à des risques potentiels en cas de violation de la sécurité.

- **Interface Graphique (Serveur):**
  L'interface graphique n'est actuellement disponible que sur le client, ce qui pourrait limiter l'expérience utilisateur.

- **Fonction Appel et Médias:**
  Possibilité d'ajouter des fonctionnalités telles que les appels, l'envoi d'images, de gifs, de vidéos, d'emojis, ainsi que la personnalisation avec une image de profil.

- **Historique des Messages:**
  Amélioration potentielle en ajoutant la fonctionnalité d'affichage des anciens messages lors de la connexion, offrant un historique complet des échanges.

- **Bouton Logout (client):** 
  Ajout d'un bouton de déconnexion pour une meilleure navigation.

- **Commandes depuis le Client:** 
  Possibilité d'effectuer des commandes directement depuis l'interface client.

# Documentation Développeur

Une documentation complète développeur a été élaborée tant pour le client que pour le serveur, facilitant l'amélioration continue du code. Cette ressource détaillée permet à tout développeur de comprendre rapidement l'architecture, d'ajouter de nouvelles fonctionnalités et de contribuer au développement du projet.
