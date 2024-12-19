# Docker-k8s: Lab 3

January 25, 2023 

# 1. Docker Compose

Dans cette partie on va reprendre la même application web et sa base de données de notes pour explorer le fonctionnement de Docker Compose.

Commencez par se positionner dans le dossier du projet `day3/compose/` du repository Github:

[https://github.com/MedDaly/docker-k8s-training](https://github.com/MedDaly/docker-k8s-training)

1. Une fois le code téléchargé naviguez vers le repertoire du projet et explorez le
    
    ```bash
    cd <local_path_of_code>/day3/compose
    ```
    
2. Vous allez trouver le fichier de configuration `docker-compose.yaml` 
    
    ```yaml
    version: '3'
    services:
      my-notes-app:
        image: notes-app:v3
        build: .
        command: python app.py
        ports:
          - "5000:80"
      my-db:
        image: notes-db
    ```
    
3. Exécutez le build de l’image de l’app avec la commande:
    
    ```bash
    docker-compose build
    ```
    
    Listez les images et remarquez l’ajout de la nouvelle image `notes-app:v3` 
    
4. démarrez docker-compose avec la commande:
    
    ```bash
    docker-compose up
    ```
    
    L’ensemble de conteneurs vont être démarré, une fois `Ctrl-C` les conteneurs sont arrêtés et supprimés.
    
    Pour lancer docker compose en background vous pouvez, comme avec docker run essayer le mode `--detach` 
    
    ```bash
    docker-compose up --detach
    # ou
    docker-compose up -d
    ```
    
    Pour arrêter le stack démarré par docker compose on peut utiliser la commande down
    
    ```bash
    docker-compose down
    ```
    
5. On va commencer maintenant à modifier le fichier yaml de docker compose, la première étape et de setup un network pour les deux conteneurs.
Ce setup n’est pas obligatoire car car docker compose fait par défaut un network commun pour tous les conteneurs dans sa configuration, mais on peut par contre faire une configuration spécifique et créez un volume dans la configuration.
La première étape serait d’ajouter le network en question dans le fichier yaml
    
    ```yaml
    version: '3'
    services:
      ...
    networks:
      notes-network:
        driver: bridge
    ```
    
    Puis ajouter ce network à la configuration de chacun des deux composants de la façon suivante:
    
    ```yaml
    version: '3'
    services:
      my-notes-app:
        ...
        networks:
          - notes-network
      my-db:
        ...
        networks:
          - mynetwork
    ...
    ```
    
6. Démarrez le docker compose, testez l’application et regarder la liste de network disponibles
    
    ```bash
    docker network ls
    ```
    
7. Une fois le compose arrêté, vous allez remarquer que le network devrait aussi être supprimé
8. Docker Compose permet également de faire des dependences entre les conteneurs, ceci permet par exemple de ne pas lancer l’application avant que la db est prête.
Dans des use case ou la dépendance est critique à l’utilisation normale de l’application et le démarrage de certaines image pourrait prendre du temps, ce paramètre est très utile.
Dans notre cas on va rendre l’app web dépendante de la db, ceci se fait dans la config de l’app de la façon suivante:
    
    ```yaml
    version: '3'
    services:
      my-notes-app:
        ...
        depends_on:
          - my-db
      my-db:
        ...
    ...
    ```
    
9. On remarque également que deux types de données sont en train de disparaitre à chaque fois qu’on redémarre le système:
    - Les données de la base de données
    - Le fichier de log
    
    Pour garder ces deux types de données on définie deux volumes:
    
    ```yaml
    version: '3'
    services:
      ...
    volumes:
      db-data:
      log-volume:
        driver: local
    networks:
      ...
    ```
    
    Et puis monter ces volumes au conteneur
    
    ```yaml
    version: '3'
    services:
      my-notes-app:
        ...
        volumes:
          - log-volume:/app/logs
    		...
      my-db:
        ...
        volumes:
          - db-data:/var/lib/mysql
        ...
    volumes:
      ...
    networks:
      ...
    ```
    
10. Faites tourner  tourner les services docker compose up et down et tester l’application pour voir si les notes persistent, vous pouvez également vérifier que les volumes restent présent et ne disparaissent pas après l’arrêt des services docker compose

# 2. Kubernetes

## 2.1 - Installation de Minikube

[minikube start](https://minikube.sigs.k8s.io/docs/start/)

### Pré-requis:

- 2 CPUs ou plus
- Au moins 2GB de RAM
- 20 GB de disque disponible
- Container or virtual machine manager, comme: 
(dans notre cas on devrait avoir docker déjà installé)
- [Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/)
- [Hyper-V](https://minikube.sigs.k8s.io/docs/drivers/hyperv/)
- [KVM](https://minikube.sigs.k8s.io/docs/drivers/kvm2/)
- [VirtualBox](https://minikube.sigs.k8s.io/docs/drivers/virtualbox/)

## 2.1.1 - Windows

Téléchargez le fichier d’installation de la dernière version:

[](https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe)

Puis ajoutez ce fichier au PATH de windows

[Procédure : ajouter des emplacements d'outils à la variable d'environnement PATH](https://learn.microsoft.com/fr-fr/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))

Dan le lien ci-dessous de minikube on explique également comment faire ça en ligne de commande

Il possible également d’utiliser le package manager de windows chocolatey, si vous l’avez sur 

```powershell
choco install minikube
```

## 1.2 - MacOS

Le plus simple est d’utiliser `homebrew`

```bash
brew install minikube
```

## 1.3 - Linux

Pour une architecture `x86-64`

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Vérifiez l’installation en executant la commande:

```bash
minikube version
```

## 2.2 - Manipulation de Minikube

1. Après l’installation vous pouvez lancer votre cluster minikube en local:
    
    ```bash
    minikube start
    ```
    
2. L’installation de minikube comprend également la commande le CLI `kubectl` qui permet de gérer votre cluster.
Dans kubernetes `kubectl` est l’équivalent de la commande `docker` 
On peut commencer par lister tous les pods qui tournent sur votre cluster:
    
    ```bash
    kubectl get pods -A
    ```
    
    Ceci va vous listez l’ensemble des pods système qui constituent Kubernetes et le permettent d’assurer son rôle.
    
    - `kube-apiserver`: Ce pod exécute le serveur d'API Kubernetes, qui est responsable de gérer les demandes d'API et de coordonner l'état du cluster.
    - `kube-controller-manager`: Ce pod exécute le gestionnaire de contrôleur Kubernetes, qui est responsable de gérer l'état du cluster et de s'assurer que l'état souhaité est atteint.
    - `kube-scheduler`: Ce pod exécute le planificateur Kubernetes, qui est responsable de prendre des décisions d'ordonnancement pour les pods et de s'assurer que les pods sont répartis de manière équitable sur les nœuds dans le cluster.
    - `etcd`: Ce pod exécute etcd, qui est un magasin de clés-valeurs distribué utilisé par la plaque de commande Kubernetes pour stocker la configuration et l'état du cluster.
    - `kube-proxy`: Ce pod exécute le proxy Kubernetes, qui est responsable de mettre en œuvre le protocole proxy de service Kubernetes, de gérer la découverte de services et de transférer le trafic vers les pods appropriés.
    - `coredns` : Ce pod exécute CoreDNS, un serveur DNS flexible et extensible qui fournit la découverte de service et est un remplacement pour kube-dns.
    - `storage-provisioner` : Responsable de la gestion des stocks de stockage dans votre cluster Kubernetes. Il est utilisé pour provisionner automatiquement des volumes de stockage pour les pods qui en ont besoin.
3. Une fois démarré on peut suivre l’état des général du cluster avec la fonctionnalité dashboard de minikube qui lance un UI capable de monitorer les différents aspects
    
    ```bash
    minikube dashboard
    ```
    
4. On peut aussi arrêter et redémarrer le cluster
    
    ```bash
    minkube stop
    
    minkube start
    ```
    
5. Et pour supprimer toutes les ressources associées (reset)
    
    ```bash
    docker delete --all
    ```
    
6. Dans les versions récentes de minikube, il est possible de démarrer des clusters multi-noeuds
On peut démarrer un cluster avec deux noeuds:
    
    ```bash
    mininkube start --nodes 2
    ```
    
7. On peut aussi lister les différent noeuds avec kubectl
    
    ```bash
    kubeclt get nodes
    ```
    

***Bonus:***

Pour plus de manipulation du mode multi-node de minikube vous pouvez consulter ce tutoriel:

[Using Multi-Node Clusters](https://minikube.sigs.k8s.io/docs/tutorials/multi_node/)