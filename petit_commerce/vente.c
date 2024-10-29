#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vente.h"

void enregistrerVente(Vente vente, const char *nomFichierVentes, const char *nomFichierProduits) {
    FILE *file = fopen(nomFichierVentes, "ab");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de ventes\n");
        return;
    }
    fwrite(&vente, sizeof(Vente), 1, file);
    fclose(file);
}


void mettreAJourStock(int idProduit, int quantiteAchete, const char *nomFichierProduits) {
    modifierQuantiteProduit(idProduit, quantiteAchete, nomFichierProduits);
}


void consulterHistoriqueVentes(const char *nomFichierVentes) {
    FILE *file = fopen(nomFichierVentes, "rb");
    Vente vente;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de ventes\n");
        return;
    }
    printf("Historique des ventes :\n");
    while (fread(&vente, sizeof(Vente), 1, file)) {
        printf("Vente ID: %d, Produit ID: %d, Quantité: %d, Montant Total: %.2f, Date: %s\n", vente.idVente, vente.idProduit, vente.quantite, vente.montantTotal, vente.date);
    }
    fclose(file);
}

void historiqueAchatsClient(int idClient, const char *nomFichierVentes) {
    FILE *file = fopen(nomFichierVentes, "rb");
    Vente vente;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de ventes\n");
        return;
    }
    printf("Historique des achats du client %d :\n", idClient);
    while (fread(&vente, sizeof(Vente), 1, file)) {
        if (vente.idClient == idClient) {
            printf("Vente ID: %d, Produit ID: %d, Quantité: %d, Montant Total: %.2f, Date: %s\n", vente.idVente, vente.idProduit, vente.quantite, vente.montantTotal, vente.date);
        }
    }
    fclose(file);
}

int obtenirProchainIDVente(const char *nomFichierVentes) {
    FILE *file = fopen(nomFichierVentes, "rb");
    int maxID = 0;
    Vente vente;
    
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de ventes\n");
        return -1;
    }

    while (fread(&vente, sizeof(Vente), 1, file)) {
        if (vente.idVente > maxID) {
            maxID = vente.idVente;
        }
    }

    fclose(file);

    return maxID + 1;
}
