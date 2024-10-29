#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "fournisseur.h"


void enregistrerFournisseur(Fournisseur fournisseur, const char *nomFichierFournisseurs) {
    FILE *file = fopen(nomFichierFournisseurs, "ab");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de fournisseurs\n");
        return;
    }
    fwrite(&fournisseur, sizeof(Fournisseur), 1, file);
    fclose(file);
}


void supprimerFournisseur(int idFournisseur, const char *nomFichierFournisseurs) {
    FILE *fileTemp = fopen("temp.dat", "wb");
    FILE *file = fopen(nomFichierFournisseurs, "rb");
    Fournisseur fournisseur;
    int trouve = 0;

    if (fileTemp == NULL) {
        printf("Erreur lors de l'ouverture du fichier temporaire\n");
        return;
    }


    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de fournisseurs\n");
        fclose(fileTemp);
        return;
    }

    while (fread(&fournisseur, sizeof(Fournisseur), 1, file)) {
        if (fournisseur.idFournisseur != idFournisseur) {
            fwrite(&fournisseur, sizeof(Fournisseur), 1, fileTemp);
        } else {
            trouve = 1;
        }
    }

    fclose(file);
    fclose(fileTemp);

    if (!trouve) {
        printf("Fournisseur non trouvé\n");
        remove("temp.dat");
    } else {
        remove(nomFichierFournisseurs);
        rename("temp.dat", nomFichierFournisseurs);
    }
}


void consulterFournisseur(int idFournisseur, const char *nomFichierFournisseurs) {
    FILE *file = fopen(nomFichierFournisseurs, "rb");
    Fournisseur fournisseur;
    int trouve = 0;
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de fournisseurs\n");
        return;
    }

    while (fread(&fournisseur, sizeof(Fournisseur), 1, file)) {
        if (fournisseur.idFournisseur == idFournisseur) {
            printf("Informations du fournisseur :\n");
            printf("ID du fournisseur : %d\n", fournisseur.idFournisseur);
            printf("Nom du fournisseur : %s\n", fournisseur.nom);
            trouve = 1;
            break;
        }
    }

    if (!trouve) {
        printf("Fournisseur non trouvé\n");
    }

    fclose(file);
}


void enregistrerCommande(Commande commande, const char *nomFichierCommandes) {
    FILE *file = fopen(nomFichierCommandes, "ab");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de commandes\n");
        return;
    }
    fwrite(&commande, sizeof(Commande), 1, file);
    fclose(file);
}


void consulterCommandesFournisseur(int idFournisseur, const char *nomFichierCommandes) {
    FILE *file = fopen(nomFichierCommandes, "rb");
    Commande commande;
    int trouve = 0;
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de commandes\n");
        return;
    }

    while (fread(&commande, sizeof(Commande), 1, file)) {
        if (commande.idFournisseur == idFournisseur) {
            printf("Informations de la commande :\n");
            printf("ID du fournisseur : %d\n", commande.idFournisseur);
            printf("ID de la commande : %d\n", commande.idCommande);
            printf("Nombre de produits dans la commande : %d\n", commande.nombreProduits);
            printf("Statut de réception de la commande : %s\n", commande.statutReception ? "Reçue" : "Non reçue");
            trouve = 1;
        }
    }

    if (!trouve) {
        printf("Aucune commande trouvée pour ce fournisseur\n");
    }

    fclose(file);
}


void mettreAJourStatutReception(int idFournisseur, int idCommande, int statutReception, const char *nomFichierCommandes) {
    FILE *file = fopen(nomFichierCommandes, "r+b");
    Commande commande;
    int trouve = 0;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de commandes\n");
        return;
    }

    while (fread(&commande, sizeof(Commande), 1, file)) {
        if (commande.idFournisseur == idFournisseur && commande.idCommande == idCommande) {
            commande.statutReception = statutReception;
            fseek(file, -sizeof(Commande), SEEK_CUR);
            fwrite(&commande, sizeof(Commande), 1, file);
            trouve = 1;
            break;
        }
    }

    if (!trouve) {
        printf("Commande non trouvée\n");
    }

    fclose(file);
}


void consulterCommandesNonRecues(const char *nomFichierCommandes) {
    FILE *file = fopen(nomFichierCommandes, "rb");
    Commande commande;
    int trouve = 0;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de commandes\n");
        return;
    }

    while (fread(&commande, sizeof(Commande), 1, file)) {
        if (!commande.statutReception) {
            printf("Commande non reçue pour le fournisseur avec l'ID : %d\n", commande.idFournisseur);
            trouve = 1;
        }
    }

    if (!trouve) {
        printf("Toutes les commandes ont été reçues\n");
    }

    fclose(file);
}

int obtenirProchainIDFournisseur(const char *nomFichierFournisseurs) {
    FILE *file = fopen(nomFichierFournisseurs, "rb");
    int maxID = 0;
    Fournisseur fournisseur;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier des fournisseurs\n");
        return -1;
    }

    while (fread(&fournisseur, sizeof(Fournisseur), 1, file)) {
        if (fournisseur.idFournisseur > maxID) {
            maxID = fournisseur.idFournisseur;
        }
    }

    fclose(file);

    return maxID + 1;
}

int obtenirProchainIDCommande(const char *nomFichierCommandes) {
    FILE *file = fopen(nomFichierCommandes, "rb");
    int maxID = 0;
    Commande commande;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier des commandes\n");
        return -1;
    }

    while (fread(&commande, sizeof(Commande), 1, file)) {
        if (commande.idCommande > maxID) {
            maxID = commande.idCommande;
        }
    }

    fclose(file);

    return maxID + 1;
}
