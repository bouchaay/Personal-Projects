#include <stdio.h>
#include <stdlib.h>
#include "menuapp.h"
#include <string.h>

int afficherMenu(bool isManager) {
    int choix;

    printf("1. Gestion des produits\n");
    printf("2. Gestion des ventes\n");
    printf("3. Gestion des clients\n");
    printf("4. Gestion des fournisseurs\n");
    if (!isManager) {
        printf("5. Quitter\n");
    } else {
        printf("5. Gestion des employés\n");
        printf("6. Quitter\n");
    }
    printf("Choix : ");
    scanf("%d", &choix);
    return choix;
}

void gestionProduits(const char *nomFichierProduits, bool isManager) {
    int choix;
    Produit nouveauProduit;
    int idProduit;
    char nouveauNom[50];
    int choixModification;
    double nouveauPrix;
    int nouvelleQuantite;
    int idProduitSupprimer;

    do {
        printf("1. Ajouter un produit\n");
        printf("2. Modifier un produit\n");
        printf("3. Supprimer un produit\n");
        printf("4. Consulter la liste des produits\n");
        printf("5. Vidage du stock\n");
        printf("6. Retour au menu principal\n");
        printf("Choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                nouveauProduit.id = obtenirProchainIDProduit(nomFichierProduits);
                printf("Nom du produit : ");
                scanf("%s", nouveauProduit.nom);
                printf("Prix du produit : ");
                scanf("%lf", &nouveauProduit.prix);
                printf("Quantite du produit : ");
                scanf("%d", &nouveauProduit.quantite);
                ajouterProduit(nouveauProduit, nomFichierProduits);
                break;
            case 2:
                printf("Identifiant du produit à modifier : ");
                scanf("%d", &idProduit);
                printf("1. Modifier le nom\n");
                printf("2. Modifier le prix\n");
                printf("3. Modifier la quantite\n");
                printf("Choix : ");
                scanf("%d", &choixModification);
                switch (choixModification) {
                    case 1:
                        
                        printf("Nouveau nom : ");
                        scanf("%s", nouveauNom);
                        modifierNomProduit(idProduit, nouveauNom, nomFichierProduits);
                        break;
                    case 2:
                        
                        printf("Nouveau prix : ");
                        scanf("%lf", &nouveauPrix);
                        modifierPrixProduit(idProduit, nouveauPrix, nomFichierProduits);
                        break;
                    case 3:
                        
                        printf("Nouvelle quantite : ");
                        scanf("%d", &nouvelleQuantite);
                        modifierQuantiteProduit(idProduit, nouvelleQuantite, nomFichierProduits);
                        break;
                    default:
                        printf("Choix invalide\n");
                }
                break;
            case 3:
                
                printf("Identifiant du produit à supprimer : ");
                scanf("%d", &idProduitSupprimer);
                supprimerProduit(idProduitSupprimer, nomFichierProduits);
                break;
            case 4:
                afficherStock(nomFichierProduits);
                break;
            case 5:
                viderFichier(nomFichierProduits);
                break;
            case 6:
                if (isManager) {
                    menuPrincipal();
                } else {
                    menuPrincipalNonManager();
                }
                break;
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 6);
}

void gestionVentes(const char *nomFichierVentes, const char *nomFichierProduits, bool isManager) {
    int choix;
    Vente nouvelleVente;
    do {
        printf("1. Ajouter une vente\n");
        printf("2. Consulter l'historique' des ventes\n");
        printf("3. Vidage de l'historique des ventes\n");
        printf("4. Retour au menu principal\n");
        printf("Choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                nouvelleVente.idVente = obtenirProchainIDVente(nomFichierVentes);
                printf("Identifiant du client : ");
                scanf("%d", &nouvelleVente.idClient);
                printf("Identifiant du produit : ");
                scanf("%d", &nouvelleVente.idProduit);
                printf("Quantite Acheté : ");
                scanf("%d", &nouvelleVente.quantite);
                nouvelleVente.montantTotal = nouvelleVente.quantite * obtenirPrixProduit(nouvelleVente.idProduit, nomFichierProduits);
                enregistrerVente(nouvelleVente, nomFichierVentes, nomFichierProduits);
                mettreAJourStock(nouvelleVente.idProduit, nouvelleVente.quantite, nomFichierProduits);
                break;
            case 2:
                consulterHistoriqueVentes(nomFichierVentes);
                break;
            case 3:
                viderFichier(nomFichierVentes);
                break;
            case 4:
                if (isManager) {
                    menuPrincipal();
                } else {
                    menuPrincipalNonManager();
                }
                break;
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 3);
}

void gestionClients(const char *nomFichierClients, bool isManager) {
    int choix;
    Client nouveauClient;
    int idClientSupprimer;
    int idClientConsulter;
    int idClientHistorique;
    do {
        printf("1. Ajouter un client\n");
        printf("2. Supprimer un client\n");
        printf("3. Consulter les informations d'un client\n");
        printf("4. Consulter l'histoirque des achats d'un client\n");
        printf("5. Vidage de la liste des clients\n");
        printf("6. Retour au menu principal\n");
        printf("Choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                
                nouveauClient.idClient = obtenirProchainIDClient(nomFichierClients);
                printf("Nom du client : ");
                scanf("%s", nouveauClient.nom);
                nouveauClient.montantAchatsTotal = 0;
                nouveauClient.montantBonus = 0;
                enregistrerClient(nouveauClient, nomFichierClients);
                break;
            case 2:
                
                printf("Identifiant du client à supprimer : ");
                scanf("%d", &idClientSupprimer);
                supprimerClient(idClientSupprimer, nomFichierClients);
                break;
            case 3:
                
                printf("Identifiant du client à consulter : ");
                scanf("%d", &idClientConsulter);
                consulterClient(idClientConsulter, nomFichierClients);
                break;
            case 4:
                
                printf("Identifiant du client à consulter : ");
                scanf("%d", &idClientHistorique);
                historiqueAchatsClient(idClientHistorique, nomFichierVentes);
                break;
            case 5:
                viderFichier(nomFichierClients);
                break;
            case 6:
                if (isManager) {
                    menuPrincipal();
                } else {
                    menuPrincipalNonManager();
                }
                break;
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 5);
}

void gestionFournisseurs(const char *nomFichierFournisseurs, bool isManager) {
    int choix;
    int choixGestionFournisseurs;
    Fournisseur nouveauFournisseur;
    int idFournisseurSupprimer;
    int idFournisseurConsulter;
    int choixGestionCommandes;
    Commande nouvelleCommande;
    int idFournisseurMAJ, idCommandeMAJ, statutReceptionMAJ;
    int idFournisseurCommandes;

    do {
        printf("1. Gérer les fournisseurs\n");
        printf("2. Consulter les commandes\n");
        printf("3. Retour au menu principal\n");
        printf("Choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                printf("1. Ajouter un fournisseur\n");
                printf("2. Supprimer un fournisseur\n");
                printf("3. Consulter les informations d'un fournisseur\n");
                printf("4. Vidage de la liste des fournisseurs\n");
                printf("5. Retour au menu précédent\n");
                printf("Choix : ");
                scanf("%d", &choixGestionFournisseurs);
                switch (choixGestionFournisseurs) {
                    case 1:
                        
                        nouveauFournisseur.idFournisseur = obtenirProchainIDFournisseur(nomFichierFournisseurs);
                        printf("Nom du fournisseur : ");
                        scanf("%s", nouveauFournisseur.nom);
                        enregistrerFournisseur(nouveauFournisseur, nomFichierFournisseurs);
                        break;
                    case 2:
                        
                        printf("Identifiant du fournisseur à supprimer : ");
                        scanf("%d", &idFournisseurSupprimer);
                        supprimerFournisseur(idFournisseurSupprimer, nomFichierFournisseurs);
                        break;
                    case 3:
                        
                        printf("Identifiant du fournisseur à consulter : ");
                        scanf("%d", &idFournisseurConsulter);
                        consulterFournisseur(idFournisseurConsulter, nomFichierFournisseurs);
                        break;
                    case 4:
                        viderFichier(nomFichierFournisseurs);
                        break;
                    case 5:
                        gestionFournisseurs(nomFichierFournisseurs, isManager);
                        break;
                    default:
                        printf("Choix invalide\n");
                }
                break;
            case 2:
                printf("1. Enregistre une commande\n");
                printf("2. Consulter les commandes non reçues\n");
                printf("3. Mettre à jour le statut de réception d'une commande\n");
                printf("4. Consulter les commandes d'un fournisseur\n");
                printf("5. Vidage de la liste des commandes\n");
                printf("6. Retour au menu précédent\n");
                printf("Choix : ");
                scanf("%d", &choixGestionCommandes);
                switch (choixGestionCommandes) {
                    case 1:
                        
                        nouvelleCommande.idCommande = obtenirProchainIDCommande(nomFichierFournisseurs);
                        printf("Identifiant du fournisseur : ");
                        scanf("%d", &nouvelleCommande.idFournisseur);
                        nouvelleCommande.statutReception = 0;
                        enregistrerCommande(nouvelleCommande, nomFichierFournisseurs);
                        break;
                    case 2:
                        consulterCommandesNonRecues(nomFichierFournisseurs);
                        break;
                    case 3:
                        
                        printf("Identifiant du fournisseur : ");
                        scanf("%d", &idFournisseurMAJ);
                        printf("Identifiant de la commande : ");
                        scanf("%d", &idCommandeMAJ);
                        printf("Statut de réception (0 pour non reçue, 1 pour reçue) : ");
                        scanf("%d", &statutReceptionMAJ);
                        mettreAJourStatutReception(idFournisseurMAJ, idCommandeMAJ, statutReceptionMAJ, nomFichierFournisseurs);
                        break;
                    case 4:
                        
                        printf("Identifiant du fournisseur à consulter : ");
                        scanf("%d", &idFournisseurCommandes);
                        consulterCommandesFournisseur(idFournisseurCommandes, nomFichierFournisseurs);
                        break;
                    case 5:
                        viderFichier(nomFichierFournisseurs);
                        break;
                    case 6:
                        break;
                    default:
                        printf("Choix invalide\n");
                }
                break;
            case 3:
                if (isManager) {
                    menuPrincipal();
                } else {
                    menuPrincipalNonManager();
                }
                break;
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 3);
}

void gestionEmployes(const char *nomFichierEmployes) {
    int choix;
    Employe manager, employe;
    char username[50];

    manager.isManager = true;
    do {
        printf("1. Ajouter un employé\n");
        printf("2. Supprimer un employé\n");
        printf("3. Retour au menu principal\n");
        printf("Choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                
                printf("Nom d'utilisateur : ");
                scanf("%s", employe.username);
                printf("Mot de passe : ");
                scanf("%s", employe.password);
                employe.isManager = false;
                ajouterEmploye(manager, employe, nomFichierEmployes);
                break;
            case 2:
                
                printf("Nom d'utilisateur de l'employé à supprimer : ");
                scanf("%s", username);
                supprimerEmploye(manager, username, nomFichierEmployes);
                break;
            case 3:
                menuPrincipal();
                break;
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 3);
}

void menuPrincipal() {
    int choix;
    do {
        choix = afficherMenu(true);
        switch (choix) {
            case 1:
                gestionProduits(nomFichierProduits , true);
                break;
            case 2:
                gestionVentes(nomFichierVentes, nomFichierProduits, true);
                break;
            case 3:
                gestionClients(nomFichierClients , true);
                break;
            case 4:
                gestionFournisseurs(nomFichierFournisseurs, true);
                break;
            case 5:
                gestionEmployes(nomFichierEmployes);
                break;
            case 6:
                printf("Au revoir\n");
                exit(EXIT_SUCCESS);
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 5);
}

void menuPrincipalNonManager() {
    int choix;
    do {
        choix = afficherMenu(false);
        switch (choix) {
            case 1:
                gestionProduits(nomFichierProduits, false);
                break;
            case 2:
                gestionVentes(nomFichierVentes, nomFichierProduits, false);
                break;
            case 3:
                gestionClients(nomFichierClients, false);
                break;
            case 4:
                printf("Seuls les managers peuvent gérer les fournisseurs.\n");
                break;
            case 5:
                printf("Au revoir\n");
                exit(EXIT_SUCCESS);
            default:
                printf("Choix invalide\n");
        }
    } while (choix != 5);
}

void menuConnexion() {
    char username[50];
    char password[50];
    bool connexionReussie = false;
    if (premiereUtilisation()) {
        printf("Le manager a été ajouté avec succès.\n");
        menuPrincipal();
    } else {
        printf("Bienvenue dans le système de gestion du petit commerce !\n");
        printf("Veuillez vous connecter pour continuer.\n");
        while (!connexionReussie) {
            printf("Veuillez entrer votre nom d'utilisateur : ");
            scanf("%s", username);
            printf("Veuillez entrer votre mot de passe : ");
            scanf("%s", password);
            if (seConnecter(username, password, nomFichierEmployes)) {
                printf("Connexion réussie !\n");
                connexionReussie = true;
            } else {
                printf("Nom d'utilisateur ou mot de passe incorrect.\n\n");
            }
        }
        if (estManager(username, nomFichierEmployes)) {
            menuPrincipal();
        } else {
            menuPrincipalNonManager();
        }
    }
}

bool premiereUtilisation() {
    bool premiereConnexion = false;
    FILE *fichier = fopen(nomFichierEmployes, "rb");
    long taille = ftell(fichier);
    Employe manager;

    if (fichier == NULL) {
        printf("Erreur lors de l'ouverture du fichier des employés.\n");
        exit(EXIT_FAILURE);
    }

    fseek(fichier, 0, SEEK_END);

    if (taille == 0) {
        premiereConnexion = true;
        fclose(fichier);

        fichier = fopen(nomFichierEmployes, "wb");
        if (fichier == NULL) {
            printf("Erreur lors de l'ouverture du fichier des employés en mode écriture.\n");
            exit(EXIT_FAILURE);
        }

        printf("Aucun employé n'est enregistré dans le système, veuillez enregistrer le manager.\n");
        printf("Nom d'utilisateur : ");
        scanf("%s", manager.username);
        printf("Mot de passe : ");
        scanf("%s", manager.password);
        manager.isManager = true;

        fwrite(&manager, sizeof(Employe), 1, fichier);
    }

    fclose(fichier);
    return premiereConnexion;
}