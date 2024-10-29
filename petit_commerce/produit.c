#include <stdio.h>
#include <string.h>
#include "produit.h"

void ajouterProduit(Produit nouveauProduit, const char *nomFichierProduits) {
    FILE *file = fopen(nomFichierProduits, "ab");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier.\n");
        return;
    }
    fwrite(&nouveauProduit, sizeof(Produit), 1, file);
    fclose(file);
}

void supprimerProduit(int idProduit, const char *nomFichierProduits) {
    FILE *fileTemp = fopen("temp.dat", "wb");
    FILE *file = fopen(nomFichierProduits, "rb");
    Produit produit;

    if (fileTemp == NULL) {
        printf("Erreur lors de l'ouverture du fichier temporaire\n");
        return;
    }

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier %s\n", nomFichierProduits);
        fclose(fileTemp);
        return;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        if (produit.id != idProduit) {
            fwrite(&produit, sizeof(Produit), 1, fileTemp);
        }
    }

    fclose(file);
    fclose(fileTemp);
    remove(nomFichierProduits);
    rename("temp.dat", nomFichierProduits);
}

void modifierNomProduit(int idProduit, const char *nouveauNom, const char *nomFichierProduits) {
    FILE *fileTemp = fopen("temp.dat", "wb");
    FILE *file = fopen(nomFichierProduits, "rb+");
    Produit produit;
    
    if (fileTemp == NULL) {
        printf("Erreur lors de l'ouverture du fichier temporaire\n");
        return;
    }

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier %s\n", nomFichierProduits);
        fclose(fileTemp);
        return;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        if (produit.id == idProduit) {
            strcpy(produit.nom, nouveauNom);
        }
        fwrite(&produit, sizeof(Produit), 1, fileTemp);
    }

    fclose(file);
    fclose(fileTemp);
    remove(nomFichierProduits);
    rename("temp.dat", nomFichierProduits);
}

void modifierPrixProduit(int idProduit, double nouveauPrix, const char *nomFichierProduits) {
    FILE *fileTemp = fopen("temp.dat", "wb");
    FILE *file = fopen(nomFichierProduits, "rb+");
    Produit produit;

    if (fileTemp == NULL) {
        printf("Erreur lors de l'ouverture du fichier temporaire\n");
        return;
    }

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier %s\n", nomFichierProduits);
        fclose(fileTemp);
        return;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        if (produit.id == idProduit) {
            produit.prix = nouveauPrix;
        }
        fwrite(&produit, sizeof(Produit), 1, fileTemp);
    }

    fclose(file);
    fclose(fileTemp);
    remove(nomFichierProduits);
    rename("temp.dat", nomFichierProduits);
}

void modifierQuantiteProduit(int idProduit, int quantiteAchete, const char *nomFichierProduits) {
    FILE *fileTemp = fopen("temp.dat", "wb");
    FILE *file = fopen(nomFichierProduits, "rb+");
    Produit produit;

    if (fileTemp == NULL) {
        printf("Erreur lors de l'ouverture du fichier temporaire\n");
        return;
    }

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier %s\n", nomFichierProduits);
        fclose(fileTemp);
        return;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        if (produit.id == idProduit) {
            produit.quantite = produit.quantite - quantiteAchete;
        }
        fwrite(&produit, sizeof(Produit), 1, fileTemp);
    }

    fclose(file);
    fclose(fileTemp);
    remove(nomFichierProduits);
    rename("temp.dat", nomFichierProduits);
}

void afficherStock(const char *nomFichierProduits) {
    FILE *file = fopen(nomFichierProduits, "rb");
    Produit produit;
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier %s\n", nomFichierProduits);
        return;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        printf("Produit %d :\n", produit.id);
        printf("Nom : %s\n", produit.nom);
        printf("Prix : %.2f\n", produit.prix);
        printf("Quantite : %d\n\n", produit.quantite);
        printf("------------------------------------------------\n");
    }

    fclose(file);
}

int obtenirProchainIDProduit(const char *nomFichierProduits) {
    FILE *file = fopen(nomFichierProduits, "rb");
    int maxID = 0;
    Produit produit;
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de produits\n");
        return -1;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        if (produit.id > maxID) {
            maxID = produit.id;
        }
    }

    fclose(file);

    return maxID + 1;
}

double obtenirPrixProduit(int idProduit, const char *nomFichierProduits) {
    FILE *file = fopen(nomFichierProduits, "rb");
    Produit produit;
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de produits\n");
        return -1;
    }

    while (fread(&produit, sizeof(Produit), 1, file)) {
        if (produit.id == idProduit) {
            fclose(file);
            return produit.prix;
        }
    }

    fclose(file);
    return -1;
}

