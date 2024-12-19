# Docker-k8s: Lab 2

January 24, 2023 

# 1. Dockerfile

Le Dockerfile est en quelque sorte la pièce d’identité d’une image docker, ce fichier de configuration permet de docker de construire l’image.

Le configuration de Dockerfile suit un format assez spécifique à docker et contient toujours l’image de base et les instructions à faire pour construire l’image

Dans cet exercice on va progressivement apprendre les bases d’un Dockerfile dans le cadre d’un packaging d’une application simple

Ci-dessous le template du Dockerfile pour vous aiguiller dans l’exercice:

```docker
# Spécifie l'image de base à partir de laquelle construire l'image personalisée
FROM <image-de-base>

# Installe les paquets ou les bibliothèques nécessaires pour l'exécution de main.py
RUN <une_commande>

# Copie des fichiers/dossier dans l'image: dans le dossier app/ de l'image
COPY <file> /app/<file>

# Définit le répertoire de travail de l'image toutes les commandes après WORKDIR
# vont partir de ce répertoire
WORKDIR <Directory>

# Définit main.py comme commande par défaut à exécuter lorsque le conteneur est démarré
ENTRYPOINT ["command", "to", "execute" ]
```

Pour plus d’informations sur le Dockerfile: 

[Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

1. Créez un répertoire pour votre projet et naviguez dedans (par exemple: `labs2-part1`) .
2. Créez un fichier appelé `Dockerfile` dans votre répertoire de projet.
3. Dans le `Dockerfile`, spécifiez une image de base telle que `python:3.9-slim`.
4. Utilisez la commande `RUN` pour installer les paquets ou les bibliothèques nécessaires.
Dans notre cas ce sont les packages: `argrparse` et `time` 
Pour installer ces package on executes ces deux commandes:
    
    ```docker
    pip install argparse
    pip install time
    ```
    
5. Voici le script python [`main.py`](http://main.py) 
    
    ```python
    import argparse
    import time
    
    # parse the command-line argument for n
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=60, help="number of seconds it takes to finish the counter")
    args = parser.parse_args()
    n = args.n
    
    for i in range(1, n+1):
        print(i)
        time.sleep(1)
    ```
    
6. Utilisez la commande `COPY` dans le `Dockerfile` pour copier le script `main.py` dans l'image dans le dossier `/app`  de l’image.
7. Définissez le `WORKDIR` dans le `Dockerfile` sur le répertoire où se trouve `main.py`.
8. Utilisez la commande `ENTRYPOINT` pour spécifier que `main.py` doit être la commande par défaut qui s'exécute lorsqu'un conteneur est démarré à partir de l'image.
Pour exécutez le script python et donc un compteur de 10 secondes on utilise la commande suivante:
    
    ```python
    python main.py --n 10
    ```
    
    Si aucune valeur n’est spécifié, par défaut `n = 60`
    
9. Construisez l'image à l'aide de la commande `docker build`, en lui donnant le nom `py-counter`
10. Exécutez un conteneur à partir de l'image (en background avec paramètre `-d`) et vérifiez qu'il exécute le script `main.py` comme prévu et vérifiez les logs du conteneur exécuté
le nom du conteneur `my-counter` 
Commande docker run:

La commande pour les logs:
    
    ```python
    docker run --name <container-name> -d <image-name>
    ```
    
11. Utilisez la commande `docker logs` pour afficher les journaux d'un conteneur en cours d'exécution.

# 3. Arguments et Variables d’environnement

Dans cette partie nous allons utiliser deux autres instructions courantes de Dockerfile et qui sont:

- `ARG` : permet de spécifier des arguments du build de l’image, ces valeurs disparaissent après le build, c’est comme des simples arguments d’un script quelconque, et dans ce cas là c’est l’exécution du build
- `ENV` : permettent de définir des variables d’environnement pour le runtime de l’image, càd ces variables sont définis pour être disponibles aux process en cours d’exécution dans le conteneur

On va commencer par ajouter un nouveau argument à notre script compteur, sur lequel on a travaillé dans l’exercice d’avant.

Le nouveau template de Dockerfile est le suivant:

```python
# Spécifie l'image de base à partir de laquelle construire l'image personalisée
FROM <image-de-base>

# Installe les paquets ou les bibliothèques nécessaires pour l'exécution de main.py
RUN <une_commande>

# Copie des fichiers/dossier dans l'image: dans le dossier app/ de l'image
COPY <file> /app/<file>

# Définit le répertoire de travail de l'image toutes les commandes après WORKDIR
# vont partir de ce répertoire
WORKDIR <Directory>

# Arguments
ARG <argument_name>=<default_name>

# Environement variables
ENV <env_var>=<default_value>

# Définit main.py comme commande par défaut à exécuter lorsque le conteneur est démarré
CMD ["command", "to", "execute"]
```

Remarque: Vous allez remarquer que qu’on a remplacé `ENTRYPOINT` par `CMD` , à ce stade on considère que les deux instructions font la même chose, on expliquera la différence plus tard dans l’exercice

### **Partie I: ARG**

1. Ajoutez un argument à votre Dockerfile avec le nom `N`  et la valeur par défaut égale à`60`
2. Changez la commande à exécuter dans l’instruction `CMD` pour utiliser la valeur du nouveau argument créé `N` comme input du script python dans le paramètre `--n` 
Pour faire cette commande dans le Dockerfile la commande devient:
    
    ```docker
    python main.py --n $N
    ```
    
3. Refaites le build de l’image `py-counter` sans spécifier d’arguments 
4. Lancez l’image, elle doit compter pendant 60 secondes et s’arrêter, regarder les logs de l’image pour vérifier c’est bien le cas (si vous lancez votre conteneur en mode background / detach `-d` ).
5. On va maintenant rebuilder l’image `py-counter` en spécifiant l’argument `N` à `20` 
On utilise pour ça `build-arg` 
    
    ```bash
    docker build --build-arg N=20 -t py-counter .
    ```
    
6. Relancez l’image, elle doit compter pendant 20 secondes et s’arrêter cette fois.
Ce qu’on a fait donc maintenant c’est de modifier la commande à exécuter pour compter jusqu’à 20
7. relancez maintenant l’image avec la commande suivante:
    
    ```bash
    docker run py-counter python main.py --n 10
    ```
    
    Que remarquez vous ? la commande spécifié dans `CMD` de l’image a été prise en compte ?
    

La différence entre `CMD` et `ENTRYPOINT`

la commande docker run peut spécifier aussi la commande à executer dans le conteneur d’une façon optionnelle. et la commande spécifié dans docker run interagit différemment si on a utilisé `CMD` ou `ENTRYPOINT` dans le Dockerfile

`CMD`spécifie la commande à exécuter lorsque le conteneur est lancé, si on ajoute une commande dans docker run, cette dernière remplace celle du `CMD` qui est ignorée. 

Tandis que `ENTRYPOINT`définit aussi la commande qui sera **toujours** exécutée lorsque le conteneur est lancé, avec la possibilité d'ajouter des arguments lors du lancement du conteneur et donc elle n’est pas ignorée par l’ajout d’une commande dans docker run.

Illustration:

Cas `ENTRYPOINT`

```bash
docker run <image> <arguments-to-be-appended-to-existing-command>
# Example
## Dockerfile
ENTRYPOINT ["python", "main.py"]
## Docker run command
docker run py-counter --n 10
```

Cas `CMD`

```bash
docker run <image> <new-command>
# Example
## Dockerfile
CMD ["python", "main.py"]
## Docker run command
docker run py-counter python main.py --n 10
```

### **Partie II: ENV**

On commence par modifier le script python [`main.py`](http://main.py) 

Le nouveau script:

```bash
import argparse
import time
import os

# parse the command-line argument for n
parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=60, help="number of seconds it takes to finish the counter")
args = parser.parse_args()
n = args.n

for i in range(1, n+1):
    print(i)
    time.sleep(1)

# Look for Env variable LOG_FILE or take by default log.txt
log_file = os.getenv("LOG_FILE", "log.txt")

# Write log in this file
with open(log_file, "w") as f:
    f.write(f"{time.time()} - N = {n}\n")
```

Maintenant le script écrit des logs dans un fichier `log.txt` , le nom de ce fichier peut être spécifié par la variable d’environnement `LOG_FILE`

1. Ajoutez une variable d’environnement au docker file qui s’appelle `LOG_FILE` et qui a comme valeur `default_log.txt`.
2. Faites le build et lancez le container avec le nom `my-counter`, après avoir fini son traitement cherchez le conteneur et redémarrez le avec `docker start` 
    
    ```bash
    docker run --name my-counter py-counter python main.py --n 10
    # On attends qu'il finit de compter et après ..
    docker start -i my-counter /bin/bash
    # maintenant on est à l'interieur du conteneur
     > cd /app
     > ls
    ```
    
    Regarder maintenant le nom du fichier de log, vous pouvez lire le fichier log avec la commande `cat <nom_du_fichier_log>`
    
3. Sortez, supprimez le conteneur `my-counter` et refaites les mêmes étapes, **sans rebuilder l’image cette fois**, avec en plus la spécification d’une variable d’environnement dans le docker run
    
    ```bash
    docker run --name my-counter --env LOG_FILE=new_log.txt py-counter python main.py --n 10
    ```
    
    Que remarquez vous maintenant par rapport au nom du fichier de log ? A t-il changé ?
    

# 2. Les volumes

A partir de cette partie nous allons travailler avec une simple application web (en flask) qui permet de stocker les notes text et les afficher.

Nous commençons par chercher le code dans le repository Github suivant:

[https://github.com/MedDaly/docker-k8s-training](https://github.com/MedDaly/docker-k8s-training)

Dans le repo de code téléchargé nous trouvons le code cible dans le path:

`day2/flask-app` : [https://github.com/MedDaly/docker-k8s-training/tree/main/day2/flask-app](https://github.com/MedDaly/docker-k8s-training/tree/main/day2/flask-app)

1. Une fois le code téléchargé naviguez vers le repertoire de l’application et listez les documents:
    
    ```bash
    > cd <local_path_of_code>/day2/flask-app
    > ls
    # You should have the following files/folders
    static/ templates/ app.py Dockerfile requirements.txt
    ```
    
2. Construisez l’image de l’application avec comme nom d’image `notes-app` 
3. Démarrez le conteneur en faisant le transfert de port entre le conteneur et vôtre machine hôte pour pouvoir accéder à l’application sur votre adresse locale 
    
    ```bash
    docker run -p 5000:80 -d --name my-notes-app notes-app
    ```
    
4. Vous devrez pouvoir accès  à l’application en local sur votre navigateur à l’adresse: 
[http://localhost:5000](http://localhost:5000/)
Vous pouvez manipuler un peux l’application et créer quelques notes
5. Arrêtez le conteneur, et supprimez le et redémarrez un nouveau. Vous allez remarque que vos anciennes notes ont disparues, pourquoi ?
6. Pour éviter de perdre les notes nous allons faire un mount du fichier txt au moment de docker run.
Commençons par créer le fichier `notes.txt` dans le du projet (flask-app) puis démarrer le conteneur en docker run 
    
    ```bash
    > touch.notes.txt
    > docker run -p 5000:80 -d --name my-notes-app -v "$(pwd)"/notes.txt:/app/notes.txt notes-app
    ```
    
7. Ajoutez quelques notes dans l’application et vérifiez si votre fichier notes.txt est en train de changer et vice versa
8. Maintenant, on va créer un volume docker et qui s’appelle `note-volume` avec la commande `docker volume create` 
9. On monte le nouveau volume au fichier txt en démarrant le conteneur
    
    ```bash
    docker run -p 5000:80 -d --name my-notes-app -v note-volume:/app notes-app
    ```
    
10. Ajoutez des notes, supprimez le conteneur et redémarrez un nouveau. Vérifiez cette fois si les données sont notes sont encore là

# 3. Les networks

Dans cette partie on va changer un petit peu notre application et au lieu de stocker les notes dans un fichier texte, on va le faire maintenant dans une base mysql qui tourne sur un deuxième conteneur.

Nous allons commencer par créer l’image de cette base de données et la lancez en conteneur

Ensuite on lance la nouvelle version de l’image de l’application. Et on montrera deux façons de faire la connexion entre les deux

1. Naviguez dans le dossier `day2/db/` et Construisez l’image de la base de données:
    
    ```bash
    docker build -t notes-db .
    ```
    
2. Lancez la base de données
    
    ```bash
    docker run -p 3306:3306 --name my-db -d notes-db
    ```
    
    A ce stade la base de données doit tourner sur le port 3306 du conteneur, et on transfère ce port au port de la machine host pour y accéder sur le [localhost](http://localhost) de la machine hôte
    
3. Naviguez dans le dossier `day2/flask-app-db` et Construisez une autre image de l’application 
    
    ```bash
    docker build -t notes-app-db .
    ```
    
4. Démarrez l’application web avec docker run 
    
    ```bash
    docker run -p 5000:80 -d --name my-notes-app-db notes-app-db
    ```
    
    Vérifiez que tout fonctionne et que l’enregistrement des données dans la base et la lecture via l’application fonctionne
    
    Regarder la partie du code qui configure la connection à la base de données
    
    ```python
    # DB connection parameters
    CONN_PARAMS = {
        "host": "host.docker.internal",
        #"host": "localhost",
        #"host": "my-db",
        "port": 3306,
        "user": "root",
        "password": "admin",
        "database": "notesdb"
    }
    ```
    
    Pourquoi l’adresse du host est `host.docker.internal` et pas [`localhost`](http://localhost) ? 
    
5. Maintenant on va faire la même connexion mais cette fois avec docker network,
Commencez par créer le network
    
    ```python
    docker network create notes-network
    ```
    
6. Arrêtez et supprimez les deux conteneurs: base de données et application
7. Redémarrez la base de données 
    
    ```python
    docker run --network notes-network --name my-db -d notes-db
    ```
    
8. Changez le Code de l’application en modifiant le paramètre host qui va prendre la valeur `my-db` 
    
    ```python
    # DB connection parameters
    CONN_PARAMS = {
        #"host": "host.docker.internal",
        #"host": "localhost",
        "host": "my-db",
        "port": 3306,
        "user": "root",
        "password": "admin",
        "database": "notesdb"
    }
    ```
    
9. Reconstruisez l’image de l’application
10. Redémarrez l’application
    
    ```python
    docker run -p 5000:80 --network notes-network --name my-notes-app-db -d notes-app-db
    ```