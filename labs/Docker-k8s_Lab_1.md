# Docker-k8s Lab 1

January 23, 2023

# Objectifs:

- Installer docker en local et avoir un environnement fonctionnel pour le reste des exercices
- Apprendre à manipuler les images et conteneurs Docker principalement via son interface de commande.

# 1 - Installation

## 1.1 - Windows

Pré-requis:

- Windows 10 11, processeur 64-bit
- Au moins 4GB de RAM
- Virtualisation activée dans le BIOS (généralement le cas)
- Powershell installé (généralement le cas)

Etapes:

- Installez de WSL2 (Windows Subsytem for Linux) si ce n’est pas déjà activé

[Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

*Remarque: L’installation de WSL 2 peut exiger un redémarrage de votre machine* 

- Téléchargez Docker Desktop: 
Dans le lien ci-dessous vous allez trouvez un lien de téléchargement du fichier `.exe` du téléchargement ainsi

[Install on Windows](https://docs.docker.com/desktop/install/windows-install/)

- Une fois le fichier téléchargé, démarrez l’installation et suivez les étapes
- Vérifiez l’installation de Docker en ouvrant l’icône de docker desktop et en vérifiant que ça tourne correctement.

## 1.2 - MacOS

Pré-requis:

- macOS 11 ou plus récent
- Au moins 4GB de RAM
- VirtualBox < 4.3.0 non installé (incompatible avec Docker Desktop)

Etapes:

- Téléchargez Docker Desktop: 
Dans le lien ci-dessous vous allez trouvez un lien de téléchargement du fichier `.dmg` du téléchargement ainsi

[Install on Mac](https://docs.docker.com/desktop/install/mac-install/)

*Remarque: Il y a deux version du fichier d’installation de docker pour Mac, un qui est pour les processeurs Intel et l’autre pour les processeur Apple Silicon (M1, M2)*

- Une fois le fichier téléchargé, démarrez l’installation et suivez les étapes
- Vérifiez l’installation de Docker en ouvrant l’icône de docker desktop et en vérifiant que ça tourne correctement.

## 1.3 - Linux

Sur Linux on peut installer seulement Docker Engine (le service Docker) ou installer docker desktop, qui n’est pas forcément disponible pour toutes les distributions de linux.

Pour vous assurer de la compatibilité de votre système avec Docker Engine regardez le tableau suivant donnée par Docker:

[Docker Engine installation overview](https://docs.docker.com/engine/install/)

### Docker Engine

Pré-requis:

ça peut varier selon la distribution mais en général:

- Une version la plus récente de l’OS (kernel linux `> 3.10` ) 
Pour verifier la version de votre machine linux Utilisez la commande `uname -r`
- Au moins 4GB de RAM

Etapes (Ubuntu):

- Désinstallez les anciennes versions

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

- Mettez à jour `apt` et installer quelques package pour autoriser l’accès au repository `apt`

```bash
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

- Ajoutez la clé GPG de Docker et faire le setup de repository: pour avoir l’accès nécessaire au téléchargement

```bash
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- Refaites un update

```bash
sudo apt-get update
```

Si vous rencontrez une erreur GPG au cours de l’update essayez les commandes suivantes:

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
```

- Lancez l’installation

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

- Créez un groupe de users `docker` avec les droits administrateur 
(pour éviter d’écrire sudo à chaque fois)

```bash
sudo groupadd docker
```

```bash
sudo usermod -aG docker $USER
```

```bash
newgrp docker
```

*Remarque: Il est possible d’un redémarrage de la session ou la VM (linux soit nécessaire), généralement il suffit d’ouvrir une nouvelle terminal/session*

- Testez votre installation

```bash
docker run hello-world
```

Documentation d’installation plus poussé en cas de soucis: 

- [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
- [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)

### Docker Desktop

Vous pouvez choisir d’installer docker desktop sur Linux et il n’est pas nécessaire de faire les deux installations (docker desktop et docker engine).

Docker Desktop tourne dans une VM dans votre système et n’a donc pas accès à vos resources docker déjà existantes si c’est le cas.

Les étapes d’installation sont détaillés dans le lien suivant:

[Install on Linux](https://docs.docker.com/desktop/install/linux-install/)

# 2 - Manipulation de Docker

## 2.1 - Docker Hub

Un repository (dépôt) public d’images de Docker géré par Docker Inc

Représente de plus grand dépôt d’images docker publiques au monde

Lien: 

[Docker Hub Container Image Library | App Containerization](https://hub.docker.com/)

1. Naviguez le lien ci-dessous et créez un compte dans le site
et trouvez une images Docker d’une techno de votre choix.
    
    Remarque: l’image peut être une image OS, un langage de programmation, une base de données etc …
    
2. Quels sont les 3 tags de trusted content ? Quel tag correspond à l’image vous avez choisi ?
3. Vérifiez si l’architecture de votre système est compatible avec les image
    
    Remarque: Pour windows vous pouvez trouver cette information dans le panel “System Information” et sur Mac dans “About this Mac”
    
4. En ligne de commande, connectez vous à docker hub avec la commande
    
    ```bash
    docker login -u <username> -p <password>
    ```
    
5. Déconnectez vous avec `docker logout`
6. Cherchez sur DockerHub la commande qui vous permettent de télécharger l’image que vous avez choisi et choisissez un tag de ceux disponibles dans la page de l’image.
7. Télécharger l’image choisi avec le tag choisi avec la commande docker trouvée la page de l’image
8. Une autre façon de chercher les images disponibles est d’utiliser la commande `docker search` pour lister les images sur Docker Hub
    
    ```bash
    docker search <image_name>
    ```
    

*Bonus: Pour des recherches plus avancées via le terminal, on peut utiliser l’API de docker, pas nécessaire dans le cadre de notre formation:*

[https://registry.hub.docker.com/v2/repositories/library/centos/tags?page_size=1024](https://registry.hub.docker.com/v2/repositories/library/centos/tags?page_size=1024)

Example Python:

```bash
GET https://registry.hub.docker.com/v2/repositories/library/python/tags?page_size=1024
```

## 2.2 Monitoring des images et Conteneurs

### Exercice 1

On commence dans cette partie par faire le pull de ces trois images:

```bash
docker pull ubuntu:20.04
docker pull python:3.9
docker pull mysql:8.0.31
```

Pour Lister les images:

```bash
docker image ls
ou
docker images
```

Pour lister les conteneurs

```bash
docker container ls -a 
ou
docker container ls
ou 
docker ps
ou 
docker ps -a
# -a permet de lister tous les conteneurs y compris ceux arrêtés
```

1. Lancez les commandes ci-dessus, Pourquoi il est préférable d’ajouter les versions dans les pull ?
2. Une fois fini vérifiez que les 3 images sont bien présentes en listant toutes les images sur votre machine, utilisez la ligne de commande.
3. Lancez les deux images `ubuntu` et `python` avec les commandes suivantes
    
    ```bash
    docker run ubuntu:20.04
    docker run python:3.9
    ```
    
    Lister les conteneurs existants, que remarquez vous par rapport au conteneurs que vous venez de lancez ? 
    
4. Lancez maintenant le conteneurs ubuntu en mode interactif
    
    ```bash
    docker run -it --name my-ubuntu ubuntu:20.04
    ```
    
    Ce mode vous permet dans ce cas de lancer un terminal bash à l’intérieur du conteneur (vous êtes maintenant à l’intérieur du conteneur ubuntu que vous venez de lancez)
    
5. Ouvrez une session de terminal à part, sans fermer la premiere et dans la deuxième lister les conteneurs en cours d’exécution et identifiez votre conteneur ubuntu
6. Revenez dans le conteneur ubuntu et lancez installez le package vim à l’intérieur:

    
    ```bash
    apt update
    apt install apt-utils
    apt install vim
    ```
    
    Vérifiez l’installation en faisant `vim —help`
    
7. Quittez le conteneur avec la commande `exit` ou bien en fermant tout simplement le terminal
8. Redémarrez ce même conteneur en mode interactif avec la commande `docker start`:
    
    ```bash
    docker start -i my-ubuntu
    ```
    
9. Vérifiez si vim est encore installé
10. Regardez les conteneurs en cours d’exécution maintenant, vous allez remarquer que votre conteneur n’est plus actif, et repérez l’id de ce conteneur arrêté (La colonne `CONTAINER_ID` dans `docker container ls -a`)
11. Supprimez ce conteneur définitivement
    
    ```bash
    docker container rm <l'id trouvé>
    ```
    
    **Important:** *Si vous avez en conteneur, même en état d’arrêt, qui un certain nom disant “scooby-doo”, vous ne pouvez pas utiliser le même nom pour lancez un autre conteneur avant de supprimer l’ancien*
    
    Remarque: On peut aussi utiliser le nom du conteneur pour le supprimer le conteneur ou bien utiliser l’id pour relancer un conteneur arrêté 
    
12. Relancez un conteneur en mode interactive exactement comme dans l’instruction 4 (avec `docker run`) et vérifiez si vim est encore installé