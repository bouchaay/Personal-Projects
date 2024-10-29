#include "connexion.h"
#include <stdio.h>
#include <string.h>


bool seConnecter(const char *username, const char *password, const char *fichierEmployes) {
    FILE *fichier = fopen(fichierEmployes, "rb");
    Employe employe;
    bool estConnecte = false;
    
    if (fichier == NULL) {
        printf("Erreur de connexion !\n");
        return false;
    }

    
    while (fread(&employe, sizeof(Employe), 1, fichier) == 1) {
        if (strcmp(employe.username, username) == 0 && strcmp(employe.password, password) == 0) {
            estConnecte = true;
            break;
        }
    }

    fclose(fichier);
    return estConnecte;
}


void ajouterEmploye(Employe manager, Employe employe, const char *fichierEmployes) {
    FILE *fichier = fopen(fichierEmployes, "ab");

    if (!manager.isManager) {
        printf("Seuls les managers peuvent ajouter des employés.\n");
        return;
    }

    if (fichier == NULL) {
        perror("Erreur lors de l'ouverture du fichier");
        return;
    }

    
    fwrite(&employe, sizeof(Employe), 1, fichier);
    fclose(fichier);

    printf("Employé ajouté avec succès.\n");
}

void supprimerEmploye(Employe manager, const char *username, const char *fichierEmployes) {
    
    Employe employe;
    FILE *fichier = fopen(fichierEmployes, "rb");
    FILE *temp = fopen("data/temp.dat", "wb");

    if (!manager.isManager) {
        printf("Seuls les managers peuvent supprimer des employés.\n");
        return;
    }

    if (fichier == NULL) {
        perror("Erreur lors de l'ouverture du fichier");
        return;
    }

    if (temp == NULL) {
        perror("Erreur lors de l'ouverture du fichier temporaire");
        fclose(fichier);
        return;
    }

    
    while (fread(&employe, sizeof(Employe), 1, fichier) == 1) {
        if (strcmp(employe.username, username) != 0) {
            fwrite(&employe, sizeof(Employe), 1, temp);
        }
    }

    fclose(fichier);
    fclose(temp);

    remove(fichierEmployes);
    rename("data/temp.dat", fichierEmployes);

    printf("Employé supprimé avec succès.\n");
}

bool estManager(const char *username, const char *fichierEmployes) {
    FILE *fichier = fopen(fichierEmployes, "rb");
    Employe employe;
    bool estManager = false;

    if (fichier == NULL) {
        printf("Erreur de connexion !\n");
        exit(1);
    }

    while (fread(&employe, sizeof(Employe), 1, fichier) == 1) {
        if (strcmp(employe.username, username) == 0) {
            estManager = employe.isManager;
            break;
        }
    }

    fclose(fichier);
    return estManager;
}
