# Spécifiez l'image de base à partir de laquelle l'image sera construite
FROM ubuntu:20.04

# Ajoutez un utilisateur et un groupe
ADD useradd.sh /usr/local/bin/
RUN /usr/local/bin/useradd.sh

# Copiez des fichiers dans l'image
COPY file1 /path/to/destination/
COPY file2 file3 /path/to/destination/
COPY dir /path/to/destination/

# Créez un répertoire dans l'image
RUN mkdir /path/to/directory

# Utilisez des variables d'environnement dans le Dockerfile
ENV VAR_NAME value
ENV VAR_NAME2 value2

# Spécifiez l'utilisateur et le groupe qui exécuteront l'application
USER user
WORKDIR /path/to/working/directory

# Exécutez des commandes et installez des paquets dans l'image
RUN apt-get update && apt-get install -y nginx

# Exposez des ports pour permettre l'accès à l'application
EXPOSE 80

# Spécifiez le script ou le programme qui sera exécuté pour démarrer l'application
CMD ["nginx", "-g", "daemon off;"]

# Définissez des arguments par défaut pour la commande CMD
ARG arg1=default_value
