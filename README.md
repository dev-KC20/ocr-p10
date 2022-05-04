# ocr-p10 Créez une API sécurisée RESTful en utilisant Django REST

Disclaimer

---

This code is part of the openclassrooms learning adventure split in 13 business alike projects.  
  
  
This one is to code a chess management app following the rules of Swiss tournament.  
Some materials or links may have rights to be granted by https://openclassrooms.com. 
The additionnal code follows "CC BY-SA ".
  
** Not to be used for production **  


---
## Objet.  
  
Développer le back-end d'une application de suivi des problèmes, basée sur la mise à disposition d'une API RESTful.

* Une application de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS).
* L'application permettra essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.
* Les trois applications exploiteront les points de terminaison d'API qui serviront les données.
  
### Models

Chaque **problème** doit avoir un titre, une description, un assigné (l’assigné par défaut étant l'auteur lui-même), une priorité (FAIBLE, MOYENNE ou ÉLEVÉE), une balise (BUG, AMÉLIORATION ou TÂCHE), un statut (À faire, En cours ou Terminé), le project_id auquel il est lié et un created_time (horodatage), ainsi que d'autres attributs mentionnés dans le diagramme de classe.

Les problèmes peuvent faire l'objet de **commentaires** de la part des contributeurs au projet auquel ces problèmes appartiennent. Chaque commentaire doit être assorti d'une description, d'un author_user_id, d'un issue_id, et d'un comment_id.

Remarque: Il est interdit à tout utilisateur autorisé autre que l'auteur d'émettre des requêtes d'actualisation et de suppression d'un problème/projet/commentaire.

Un document répertorie les mesures de sécurité OWASP que le back-end devra respecter.

## Fonctionnement du logiciel

### Connexion à la plate-forme.

### Création d'un projet.

### Affectation d'utilisateur à un projet.

### Fonctions CRUD de problème dans un projet.

### Fonctions CRUD de commentaire à un problème.

### Mesures de sécurité mises en place.

### Documentation de l'API.








---



## Installation

Pour utiliser les scripts,
il est conseillé sous le prompt bash python (ici cmd Anaconda3 sous Windows 10):

1.  de cloner l'ensemble du répertoire github dans un répertoire local dédié.
    git clone https://github.com/dev-KC20/ocr-p10.git

2.  se déplacer dans le sous répertoire de travail ocr-p9-main
    cd ocr-p10

3. créer un environnement virtuel python, ENV
    python -m venv ENV

4.  d'activer un environnement virtuel python, ENV
    ENV\scripts\activate.bat

5.  d'installer les paquets requis pour mémoire,
    pip install -r requirements-dev.txt

6.  de créer un fichier .env sous le répertoire courant afin de contenir les "secrets" (cf. plus bas) :
    
        # SECURITY WARNING: keep the secret key used in production secret!
        SECRET_KEY = blabla
        DEBUG = True

7.  d'exécuter la migration des modèles 
    python manage.py migrate

8.  d'exécuter le script serveur 
    python manage.py runserver

9.  d'accéder à l'application servie par Django en cliquant sur :
    http://127.0.0.1:8000/




### Gestion des secrets

Django utilise un "secret" pour générer ses certificats et recommande de garder cette clé secrète. 
Nous utilisons le paquet python-decouple pour remplacer les clés de secret par leur valeur dans le fichier settings.py :
Le fait de stocker les secrets dans un fichier .env évite de le "committer" par accident sur un dépôt centralisé grâce au paramétrage de notre .gitignore.

S'agissant d'un exercice pédagogique, nous voulons permettre d'utiliser notre code source et éventuelles données tout en respectant les bonnes pratiques. C'est pourquoi nous affichons en clair ce secret dans les instructions d'installation de ce readme.

```py
from decouple import config
...
SECRET_KEY = config("SECRET_KEY")

```

Références: 

cf. [Réglages | Documentation de Django | Django](https://docs.djangoproject.com/fr/4.0/ref/settings/#password-hashers)

**Gardez cette valeur secrète.**
Le fonctionnement de Django avec une clé [`SECRET_KEY`](https://docs.djangoproject.com/fr/4.0/ref/settings/#std:setting-SECRET_KEY) connue réduit à néant de nombreuses protections de sécurité de Django et peut amener à une élévation de privilèges et à des vulnérabilités d’exécution de code à distance.

cf. [GitHub - henriquebastos/python-decouple: Strict separation of config from code.](https://github.com/henriquebastos/python-decouple/)

## [Python Decouple: Strict separation of settings from code](https://github.com/henriquebastos/python-decouple/#id1)
_Decouple_ helps you to organize your settings so that you can change parameters without having to redeploy your app.

If `SECRET_KEY` is not present in the `.env`, _decouple_ will raise an `UndefinedValueError`.
This _fail fast_ policy helps you avoid chasing misbehaviours when you eventually forget a parameter.


### Conformité PEP8


