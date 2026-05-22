Pipeline ETL & Business Intelligence - Analyse du Marché Immobilier Darkom.ma
Ce projet met en place un pipeline de données complet (ETL) pour extraire, nettoyer, enrichir et modéliser les données d'annonces immobilières du site Darkom.ma. L'objectif final est de structurer ces données dans un Data Warehouse (DWH) selon un schéma en étoile afin de faciliter l'analyse décisionnelle (BI) et la création de tableaux de bord.

🚀 Architecture du Projet & Workflow
Le projet est découpé en trois phases principales :

Nettoyage & Préparation : Récupération des données brutes depuis l'environnement de staging, gestion des types de données, traitement rigoureux des valeurs manquantes et des doublons, suppression des valeurs aberrantes (outliers) et ingénierie des fonctionnalités (Feature Engineering).

Modélisation du DWH : Création automatisée du schéma de Business Intelligence et de l'ensemble des tables (dimensions et faits) directement dans PostgreSQL.

Chargement du Data Warehouse : Extraction des données uniques pour alimenter les dimensions, récupération des clés primaires générées, jointure avec les données nettoyées, et chargement final de la table de faits centrale.

🛠️ Technologies Utilisées
Langage : Python 3

Traitement de données : Pandas, NumPy

Base de données : PostgreSQL

Connexion SQL : SQLAlchemy

Visualisation : Matplotlib (Analyse exploratoire de la distribution des prix)

Gestion de l'environnement : Python-dotenv

📐 Modélisation du Data Warehouse (Schéma en Étoile)
L'architecture choisie est un schéma en étoile, optimisé pour les requêtes analytiques rapides et la création de rapports performants :

Table de Faits : * fact_annonces : Centralise les indicateurs clés et les mesures quantitatives du projet (prix, surface, prix au mètre carré, et âge du bien). Elle est connectée à toutes les dimensions via des contraintes de clés étrangères.

Tables de Dimensions :

dim_temps : Permet l'analyse temporelle (par année, mois, et trimestre de publication).

dim_localisation : Permet l'analyse géographique (par ville et par quartier).

dim_bien : Regroupe la typologie de l'annonce (type de bien, nature de la transaction, ainsi que les catégories de prix et de surface).

dim_caracteristiques : Structure l'agencement du bien (nombre de chambres, nombre de salles de bain, et étage).

📁 Détail du Fonctionnement des Scripts
1. Nettoyage et Enrichissement
Le premier script charge les données brutes et effectue un nettoyage en profondeur. Les types de données pour les dates et les valeurs numériques sont corrigés. Les doublons sont éliminés, et les valeurs manquantes sont traitées de manière ciblée : méthode de propagation pour les dates, valeur la plus fréquente (mode) pour les variables textuelles, et médiane pour les compteurs (chambres, étages).

Après l'analyse graphique de la distribution, un filtre basé sur un groupement par type de bien supprime les prix aberrants. L'ingénierie des données calcule ensuite le prix au m², définit l'âge du bien par rapport à l'année actuelle, et segmente les biens en catégories avant d'exporter le résultat dans une table propre.

2. Création de la Structure BI
Le deuxième script s'occupe de la structure DDL (Data Definition Language). Il réinitialise de manière sécurisée le schéma cible en cascade s'il existe déjà. Ensuite, il crée l'ensemble des tables de dimensions en définissant des clés primaires auto-incrémentées, puis termine par la table de faits en configurant les relations de clés étrangères nécessaires à l'intégrité de la base.

3. Chargement et Mapping des Clés
Le dernier script gère la phase de chargement final (Load). Il isole d'abord les données uniques de chaque dimension à partir de la table nettoyée et les insère dans le DWH. Une fois les dimensions remplies, il recharge ces tables pour obtenir les identifiants uniques générés par la base de données. En effectuant une jointure avec le jeu de données d'origine, le script remplace les valeurs textuelles par leurs identifiants numériques correspondants, assemble la table de faits, et y insère les données de performance.

⚙️ Guide d'Utilisation Rapide
Configuration : Ajouter un fichier de configuration pour l'environnement à la racine du projet contenant les accès à la base de données PostgreSQL (utilisateur, mot de passe, hôte, port et nom de la base).

Dépendances : Installer les bibliothèques requises pour la manipulation de données, la connexion SQL et la gestion des variables d'environnement.

Exécution : Lancer séquentiellement le script de nettoyage des données, puis le script de création des tables, et enfin le script de chargement final pour alimenter le Data Warehouse.
