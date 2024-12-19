# Docker-k8s Lab 5

January 26, 2023 

# 1. Services

## Partie I

On va commencer par créer un service cluster IP pour exposer les Pods de notre Deployment

Récupérez le repository de formation, si c’est pas encore le cas:

[https://github.com/MedDaly/docker-k8s-training](https://github.com/MedDaly/docker-k8s-training)

1. Naviguez dans le dossier `day5/services` et démarrez le deployment `notes-deployment.yaml` 
2. Créez un fichier de configuration YAML de service
`notes-service-cluster-ip.yaml`
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: notes-service-cluster-ip
    spec:
      selector:
        app: notes-app
      ports:
      - port: 5000
        targetPort: 80
      type: ClusterIP
    ```
    
3. Lancez le service: `kubectl apply -f notes-service-cluster-ip.yaml` 
4. Vérifiez l’état de service `kubectl get services` 
5. Pour connecter au service à l’intérieur du cluster on commence par trouver l’adresse IP du service 
    
    ```bash
    kubectl get services notes-service-cluster-ip
    ```
    
    Une alternative est de regarder le dashboard de minikube
    
6. Run a busybox pod to ran for 1 hour
    
    ```bash
    kubectl run ubuntu --image=ubuntu --command -- sleep 3600
    ```
    
7. Ouvrez une session de terminal dans le pod
    
    ```bash
    kubectl exec -it ubuntu -- bash
    ```
    
8. Depuis le Pod ubuntu installez `curl` 
    
    ```bash
    apt update
    apt install curl
    ```
    
9. ce qu’on va faire maintenant c’est de requeter le service à partir du container ubuntu et on a trois façons de faire ça
    
    ```bash
    curl <IP du service>:5000 
    # ou
    curl <nom du service>:5000
    # ou
    curl <mon du service>.<namespace>.<svc>.<cluster>.<local>:5000
    ```
    

Vous allez recevoir le code HTML de la page home

## Partie II

Ce type de service permet la communication interne entre Pods mais pas pour accéder de l’extérieur à l’application qui tourne sur les pods

Le cluster IP est idéal pour des services qui tournent en backend c’est pourquoi on va l’utiliser pour implementer notre base de données mysql

1. Commençons par supprimer les deployment et pods qui tournent sur notre cluster (namespace default)
    
    ```bash
    kubectl delete all --all
    ```
    
2. Créez deux fichiers YAML:
    - `db-deployment.yaml`
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: db-deployment
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: notes
          type: db
      template:
        metadata:
          labels:
            app: notes
            type: db
        spec:
          containers:
          - name: db
            image: eddeli/notes-db
      strategy:
        type: RollingUpdate
    ```
    
    - `db-service.yaml`
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: db-service
    spec:
      selector:
        app: notes
        type: db
      ports:
      - port: 3306
        targetPort: 3306
      type: ClusterIP
    ```
    
3. Lancez le deployment et le service de la base de données
4. Reprenez les fichiers YAML de Deployment `notes-deployment.yaml`de l’application web et faites les changements suivants:
    1. Changez les labels du deployment et dans les selectors de service à:
        
        ```yaml
        labels:
          app: notes
          type: web
        ```
        
    2. Changez l’image docker à celle publié dans le lien suivant:
        
        [Docker](https://hub.docker.com/r/eddeli/notes-app-db/tags)
        
5. Create a new service configuration YAML `notes-service.yaml` de type NodePort
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: notes-service
    spec:
      selector:
        app: notes
        type: web
      ports:
      - NodePort: 30080
        port: 80
        targetPort: 80
      type: NodePort
    ```
    
6. Lancez le deployment et le service 
7. Le NodePort permet d’exposer à l’extérieur du cluster, pour accéder à ce service sur votre [localhost](http://localhost) activez la commande `minikube service notes-service` 
Et manipulez l’application
8. Minikube offre également la possibilité d’exposer votre service avec un service `Loadbalancer` Pour faire ça modifier le YAML de service:
    
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: notes-service
    spec:
      selector:
        app: notes
        type: web
      ports:  
        port: 80
        targetPort: 80
      type: LoadBalancer
    ```
    
    Notez que la configuration de type LoadBalancer n’est pas disponible par défaut sur tout cluster k8s et peut varier d’un cloud provider à un autre. 
    
    Minikube offre cette possibilité avec un Load Balancer dans sa configuration
    

**Some Extra Sources:**

[Kubernetes NodePort vs LoadBalancer vs Ingress? When should I use what?](https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0)

# 2. Gestion des données et Volumes

On va commencer par le même setup de dernier exercice 

1. Commencez par créer un nouveau dossier de travail `day5/volumes` et copiez les YAMLs utilisés précédemment dans ce dossier
2. Assurez vous que les deux services tournent correctement
3. On sait que chaque Pod enregistre des logs dans le fichier `logs/log.txt` de son container nous allons créer un volume de type `EmptyDir`  en modifiant le `spec`  du template dans le deployment
    
    ```yaml
    spec:
    	containers:
      - name: notes
        image: eddeli/notes-app-db
        env:
        - name: DB_HOST
          value: db-service
        volumeMounts:
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: logs-volume
        emptyDir:
          sizeLimit: 1Gi
    ```
    
    Then update the deployment
    
4. Using the app Add 2 notes “Notes 1” and “Note2” and get the name of the Pod used from the UI
5. On peut vérifier les logs en se connectant au Pod
    
    ```yaml
    kubectl exec -it <pod-name> -- bash
    # inside the Pod
    root@<pod-name>: cat logs/flask.log
    ```
    
6. (Optionnel): Ce type de volume n’est pas supprimé si le conteneur à l’intérieur de Pod est supprimé mais disparait sir le Pod est supprimé.
On peut essayer dans trouver le conteneur qui tourne à l’intérieur de ce Pod et le supprimer
    
    ```bash
    # Se connecter au noeud qui héberge le pod
    minikube ssh <le noeud du pod>
    # Lister les conteneurs
    docker container ls
    # Trouver le conteneur associé au Pod, le nom du pod devrait être inclus dans le nom du conteneur
    docker stop <conteneur>
    dokcer rm <conteneur>
    ```
    
7. (Optionnel) Redémarrez le deployment, de nouveau pods vont être crées
Avant de réutiliser l’application, vous pouvez vous connecter à tous les trois pods et verifier que les fichiers logs sont vides.
8. On va essayer maintenant de changer le volume vers le type HosPath
    
    ```yaml
    ...
    volumes:
    - name: logs-volume
      hostPath:
        path: /opt/notes-log/
        type: Directory
    ...
    ```
    
    Utilisez l’application pour ajouter des notes 
    
9. Connectez aux nodes et regardez si les logs on été stockés dans le fichier log
`/opt/notes-log/` 

1. Jusqu’à ce stade nous avons utilisé un seul Pod pour la base de données mais si on utilise plusieurs replicas, modifiez le nombre de replicas à 2 du deployment `db-deployment.yaml`  et relancez le.
Que remarquez vous par rapport à la fiabilité de la page liste de notes ? Pourquoi on n’a pas toujours la même liste ?
2. Dans le besoin d’avoir des volumes persistants nous allons créer 1 pour stocker les données de services base de données
Créez les fichiers de configuration du volume et du volume claim
`persistant-volume.yaml` 
    
    ```yaml
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: data-pv
    spec:
      capacity:
        storage: 5Gi
      volumeMode: Filesystem
      storageClassName: standard
      accessModes:
      - ReadWriteMany
      hostPath:
        path: /opt/data
        type: DirectoryOrCreate
    ```
    
    `persistant-volume-claim.yaml` 
    
    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: data-pvc
    spec:
      volumeName: data-pv
      accessModes:
      - ReadWriteOnce
      storageClassName: standard
      resources:
        requests:
          storage: 2Gi
    ```
    
3. Créez le volume et et le volume claim
    
    ```bash
    kubectl apply -f persistant-volume.yaml
    kubectl apply -f persistant-volume-claim.yaml
    ```
    
4. Modifie le spec de conteneur du deployment pour monter le volume
    
    ```yaml
    ...
    	spec:
        containers:
        - name: db
          image: eddeli/notes-db
          volumeMounts:
          - name: data-volume
            mountPath: /var/lib/mysql
        volumes:
        - name: data-volume
          persistentVolumeClaim:
            claimName: data-pvc
    ...
    ```
    
    And restart the database services
    
    Remarque: Le type HostPath de persistant volume ne marche que pour un cluster mono-node.