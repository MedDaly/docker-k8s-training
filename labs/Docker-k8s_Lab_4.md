# Docker-k8s Lab 4

January 26, 2023 

**Remarque:** Tout au long des exercices vous pouvez lancez le minikube dashboard dans un terminal à part ou en background pour observer les différents changements à votre cluster

# 1. Pods

### Partie I

On va commencer par un exercice simple ou on va lancer un pod de l’image `nginx` 

1. Démarrez votre cluster Minikube en utilisant la commande `minikube start`.
2. Utilisez la commande `kubectl get nodes` pour vérifier que le noeud Minikube est en cours d'exécution.
3. Démarrez un Pod `kubectl run nginx --image=nginx` pour créer un pod exécutant une image Nginx.
4. Listez les pods `kubectl get pods` pour vérifier que le pod est en cours d'exécution.
5. Exposez votre Pod avec un service `kubectl expose pod nginx --port=80 --type=NodePort` pour exposer le pod en utilisant un port de nœud.
6. Utilisez la commande `minikube service nginx` pour obtenir l'URL d'accès au service.
7. Utilisez un navigateur pour accéder à l'URL du service pour vérifier que Nginx est en cours d'exécution.
8. Utilisez les commandes suivantes pour supprimer le Pod et le service
    
    ```bash
    kubectl delete pod nginx
    # ou
    kubeclt delete pod/nginx
    
    kubectl delete service nginx
    # ou
    kubectl delete service/nginx
    ```
    

Il y a deux façons de créer les ressources sur Kubernetes:

- La méthode **Imperative** directement dans la ligne de commande, Partie I
- La méthode **Declarative** qui se fait via les fichiers de manifest YAML qui décrivent les ressources, Partie II

### Partie II

Récupérez le repository de formation, si c’est pas encore le cas:

[https://github.com/MedDaly/docker-k8s-training](https://github.com/MedDaly/docker-k8s-training)

1. Naviguez dans le dossier `/day4/k8s` et créez un fichier YAML appelé `nginx-pod.yaml` 
    
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
    ```
    
2. Utilisez la commande `kubectl apply -f nginx-pod.yaml` pour créer le pod à partir du fichier YAML.
3. Utilisez la commande `kubectl get pods` pour vérifier que le pod est en cours d'exécution.
4. Utilisez la commande `kubectl port-forward nginx 3000:80` pour accéder au port 80 du pod sur localhost.
5. Utilisez un navigateur pour accéder à l'adresse [http://localhost:3000/](http://localhost:3000/) pour vérifier que Nginx est en cours d'exécution.
6. Vous pouvez supprimer le Pod de la même manière que dans l’exercice précédent

# 2. ReplicaSet

1. Créez un fichier appelé `nginx-rs.yaml`  et ajoutez-y le contenu suivant
    
    ```yaml
    apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      name: nginx-rs
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx
    ```
    
2. Utilisez la commande `kubectl apply -f nginx-rs.yaml` pour créer le ReplicaSet.
3. Listez les replicasets `kubectl get replicaset` 
4. Regardez combien de pods sont en train de tourner
5. Choisissez l’un des pods qui tourne supprimez le la command `kubectl delete` et regardez la réaction de k8s en surveillant le nombre de pods
6. Augmentez le nombre de réplicas  à 5 dans le ReplicaSet en mettant à jour le champ `replicas=5` dans le fichier YAML, 
puis utilisez la commande `kubectl apply -f nginx-rs.yaml` pour appliquer les modifications.
7. Regardez si les modifications ont bien été prise en compte par le replicaset déployé
avec la commande `kubectl get rs nginx-rs -o yaml` 
Ceci va vous donner un output en format yaml dans le terminal, vérifiez le nouveau nombre de replicas
8. Utilisez la commande `kubectl get replicaset` et `kubectl get pods` pour voir le nombre de réplicas mis à jour.
9. Redémarrez maintenant le pod de l’exercice précédent `kubectl apply -f nginx-pod.yaml` 
Constatez l’état de ce pod
10. Créez un nouveau fichier de config d’un deuxième Pod similaire au premier. 
Ajoutez les mêmes labels que le replicaset et changez le nom à `nginx-2` 
`nginx-pod-2.yaml` 
    
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: nginx-2
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
    ```
    
11. Démarrez le nouveau conteneur et constatez l’état des pods, que remarquez vous? Pourquoi k8s supprime ce pod ne continue pas de tourner

# 3.Deployments

1. Créez un fichier appelé `nginx-deployment.yaml`et ajoutez-y le contenu suivant:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
```

1. Utilisez la commande `kubectl apply -f nginx-deployment.yaml` pour créer le Deployment.
2. Utilisez la commande `kubectl get deployment` pour voir le Deployment et le nombre de réplicas en cours d'exécution.
3. Utilisez la commande `kubectl get all` pour voir toutes les ressource. Remarquez qu’un replicaset pour ce Deployment a été crée.
4. Mettez à jour le Deployment en changeant la version de l'image dans le fichier yaml à `nginx:1.23` et utilisez la commande `kubectl apply -f nginx-deployment.yaml`.
5. Utilisez la commande `kubectl rollout status deployment/nginx-deployment` pour vérifier le statut du déploiement et `kubectl rollout history deployment/nginx-deployment` pour voir l'historique des déploiements.
6. (Optionnel) On peut annoter les versions pour garder une trace du changement qui a été fait dans l’historique
`kubectl annotate deployment nginx-deployment [kubernetes.io/change-cause=](http://kubernetes.io/change-cause=)"version update" --overwrite=true` 
7. Mettez à jour le déploiement en changeant la version de l'image dans le fichier yaml à un nom d'image non existant comme `imaginary-frog` et l'appliquer
8. Vérifiez l’état du rollout `kubectl rollout status deployment/nginx-deployment`
vous verrez que le déploiement échouera, Est ce que l’ensemble de replicas a échoué ?
9. Utilisez la commande `kubectl rollout undo deployment/nginx-deployment` pour faire un retour en arrière sur le dernier déploiement et vérifiez le statut des pods et des replicasets.
10. Corrigez le nom de l’image et changez la strategy de rollout de `RollingUpdate` à `Recreate` 
    
    ```yaml
    strategy:
      type: Recreate
    ```
    
11. Supprimez le deployment puis récréez un nouveau
    
    ```yaml
    kubectl delete -f nginx-deployment.yaml
    kubectl apply -f nginx-deployment.yaml 
    ```
    
12. Refaites la même modification avec le mauvais nom d’image inexistant et regarder l’état de vos pods. Quelle est la différence de comportement par rapport à la strategy d’avant ?
Quelle est l’avantage de la strategy `RollingUpdate` ?

# Notes-app (Bonus)

Faisons les mêmes manipulations avec notre application python de notes: la version sans base de données: Pod, replicaset et deployment

Pour que k8s sur minikube puisse accéder à notre image nous avons deux options:

- Référencer une image directement sur DockerHub, et k8s fera le pull
    
    [Docker](https://hub.docker.com/r/eddeli/notes-app)
    
- Faire le build localement et puis loader l’image locale dans minikube dans minikube
Le code source est dans `day2/flask-app`
    
    ```bash
    minikube image load <local_image_name>
    ```
    
    Pour voir l’ensemble des images téléchargé sur votre cluster minikube
    
    ```bash
    minikube image ls --format=table
    ```
    
- Choisis l’un des pods qui tournent et fait un transfert de port pour accéder à l’application qui tourne à l’intérieur
    
    ```bash
    kubectl port-forward pod/<nom_du_pod> 3000:80
    ```
    

Nous avons réussi à scaler notre application sur plusieurs pods qui tournent, qu’est ce qui manque pour bénéficier de cette nouvelle architecture ? Comment persister de la donnée ?  Comment éviter de se connecter à un pod à la fois pour y accéder ? Ce sont les aspects qu’on va traiter dans le prochain lab