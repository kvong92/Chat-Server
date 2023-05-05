
# PROJET Chat

# I- Sujet

Le but de ce tp, est de créer une application de discussion, permettant de communiquer avec la personne que l'on souhaite et peu importe l'endroit où on se trouve. En fait: un Chat.
Vous devez réaliser cette application dans le langaguage que vous souhaitez parmis les suivants: java, C#, python.
Le serveur et le client devront être écris dans des langages différents.

## Le client

Voici une liste d'exigences pour le client :
- L'utilisateur doit définir un pseudo avant de pouvoir se connecter et le pseudo ne doit dépasser 20 caractères.
- L'utilisateur ne peut pas prendre un pseudo déjà utilisé
- L'utilisateur doit envoyer le message au serveur et le message sera diffusé à tous les autres utilisateurs.
- Utilisez la notion de classe avec des structures
- Prévenir les autres utilisateurs qu'un utilisateur s'est connecté/déconnecté
- Le client et le serveur communiquent via le protocole TCP
- Utiliser les SCOKET et le MULTI-THREAD 
- Le client peut être en interface graphique ou en console

## Le serveur

Le serveur est une application différente de l'application client.
Voici une liste d'exigences pour le serveur :
- Le serveur accepte plusieurs utilisateurs
- Le serveur possède un fichier de logs avec les connexions entrantes et sortantes.
- Utilisez la notion de classe avec des structures pour le code
- Doit stocker en mémoire la liste des clients
- Le client et le serveur communiquent via le protocole TCP
- Utiliser les SCOKET et le MULTI-THREAD 
- Le serveur doit être en console
