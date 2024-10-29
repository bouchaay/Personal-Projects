#include "files.h"
#include <stdio.h>

char *nomFichierProduits = "data/produits.dat";
char *nomFichierVentes = "data/ventes.dat";
char *nomFichierClients = "data/clients.dat";
char *nomFichierFournisseurs = "data/fournisseurs.dat";
char *nomFichierCommandes = "data/commandes.dat";
char *nomFichierEmployes = "data/employers.dat";

void viderFichier(const char *nomFichier) {
    FILE *file = fopen(nomFichier, "wb");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier %s\n", nomFichier);
        return;
    }
    fclose(file);
}
