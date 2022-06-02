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

* L'application permettra essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.
* Une application de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS).
* Les trois applications exploiteront les points de terminaison d'API qui serviront les données.
  
### Models

Chaque **problème** doit avoir un titre, une description, un assigné (l’assigné par défaut étant l'auteur lui-même), une priorité (FAIBLE, MOYENNE ou ÉLEVÉE), une balise (BUG, AMÉLIORATION ou TÂCHE), un statut (À faire, En cours ou Terminé), le project_id auquel il est lié et un created_time (horodatage), ainsi que d'autres attributs mentionnés dans le diagramme de classe.

Les problèmes peuvent faire l'objet de **commentaires** de la part des contributeurs au projet auquel ces problèmes appartiennent. Chaque commentaire doit être assorti d'une description, d'un author_user_id, d'un issue_id, et d'un comment_id.

Remarque: Il est interdit à tout utilisateur autorisé autre que l'auteur d'émettre des requêtes d'actualisation et de suppression d'un problème/projet/commentaire.

Un document répertorie les mesures de sécurité OWASP que le back-end devra respecter.


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



### Conformité PEP8

### Mesures OWASP
### Conformité RGPG
### Crédits et lectures intérestantes

Openclassrooms, bien-sur et surtout le discord DA Python!

Les documentations officielles Django et DRF ; Confucius aurait dit "une image vaut mille mots" ;-)

Vitor Freitas pour les choix d'extension du modèle utilisateur sous la forme d'un questionnaire "fonctionnalités recherchées":
[How to Extend Django User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#proxy)

Špela Giacomelli (aka GirlLovesToCode) pour sa série de billets sur les permissions DRF.
[Permissions in Django REST Framework | TestDriven.io](https://testdriven.io/blog/drf-permissions/)

Gutsytechster pour son introduction aux opérations d'Authentification dans DRF.

[User Auth operations in DRF – Login, Logout, Register, Change Password – Curiosity never ends](https://gutsytechster.wordpress.com/2019/11/12/user-auth-operations-in-drf-login-logout-register-change-password/)

J.V. Zammit @untangled.dev pour son 'explicatif' guide : [A minimal Django testing style guide](https://www.untangled.dev/2021/08/22/django-testing-style-guide/)

Lacey Williams Henschel for her great series about and more precisely [What You Should Know About DRF, Part 1: ModelViewSet attributes and methods — Lacey Williams Henschel](https://www.laceyhenschel.com/blog/2021/2/22/what-you-should-know-about-drf-part-1-modelviewset-attributes-and-methods)


## Documentation de Softdesk API

### Introduction

The SoftDesk API enables your helpdesk team to support your projects thru:

* reporting Issues on a per Project basis,
* allocating these Issues to team members for fixing,
* and collecting related Comments from other project members.

A set of 19 end points are provided to interact with the front end solution of your choice.

### Overview

We could suggest the following workflow to support a project:

1.    The user does log-in.
2.    The user creates a new project
3.    The user adds members to his project
4.    When it occurs, the user creates an open issue & assign it to one of his project members
5.    If needed he or any project member make comments about the issue
6.    When the assignee has fixed the point, the project responsible closes the issue.

The application structure includes basically 3 levels of embedded models : Project, Issues, Comments.

For these, the basic CRUD methods are provided thru the available end-points.

If you need a mock data set for testing purpose, here is what we suggest:

|user/project| 1  |  2 |  3 |  4 | 5 |
|------------|----|----|----|----|---|
| 1.adminoc  |    | A  |    |    |   |
| 2.JohnDoe  | A  |    | A  |  A |   |
| 3.JaneSmith| (M)|    |    |    | A |

(A)uthor ; (M)ember.

We provide two series of test: one of the back-end side and one on the Postman client side.

Fot the latter, remember when checking User permissions that "adminoc" is also the SoftDesk API superuser.
In the Project direction, the tested (C)reate/(U)pdate/(R)etrieve Issue or Comment will be removed thru (D)elete.

Our product is still under active developpement. Feel free to contact us for any questions or proposals of improvement.
Authentication

Only authenticated users can access the SoftDesk backend. In order to do so the user first needs to register by providing an email address. The same email with its associated password will be required to login at the back-end.

We do not use the collected emails for any purpose. Therefore, the provided email could also be a fake one.

SoftDesk API includes the Simple JWT package in order to provide JSON Web Token authentication. The current setting for the Token access and Token refresh life time are :

    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

### Error Codes

Successful status codes:
```
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
```


Error status codes:
```
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_500_INTERNAL_SERVER_ERROR
```

### Rate limit

No limits of request were set in version 1 of the SoftDesk API.


### End Points description

[softdesk_api](https://documenter.getpostman.com/view/19150435/Uz5DrdLm)


## Tests passed

### Postman Test 26/26

![Postman 1/3](img/postman-test-1.png)  

![Postman 2/3](img/postman-test-2.png)  

![Postman 3/3](img/postman-test-3.png)  

### Django ApiTestCase 6/6

```bash
python manage.py test
Found 6 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 3.482s

OK
Destroying test database for alias 'default'...
```