#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "client.h"


void enregistrerClient(Client client, const char *nomFichierClients) {
    FILE *file;
    file = fopen(nomFichierClients, "ab");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de clients\n");
        return;
    }
    fwrite(&client, sizeof(Client), 1, file);
    fclose(file);
}


void supprimerClient(int idClient, const char *nomFichierClients) {
    FILE *fileTemp;
    Client client;
    FILE *file;
    int trouve = 0;

    fileTemp = fopen("temp.dat", "wb");
    if (fileTemp == NULL) {
        printf("Erreur lors de l'ouverture du fichier temporaire\n");
        return;
    }

    file = fopen(nomFichierClients, "rb");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de clients\n");
        fclose(fileTemp);
        return;
    }

    while (fread(&client, sizeof(Client), 1, file)) {
        if (client.idClient != idClient) {
            fwrite(&client, sizeof(Client), 1, fileTemp);
        } else {
            trouve = 1;
        }
    }

    fclose(file);
    fclose(fileTemp);

    if (!trouve) {
        printf("Client non trouvé\n");
        remove("temp.dat");
        return;
    } else {
        remove(nomFichierClients);
        rename("temp.dat", nomFichierClients);
    }
}


void mettreAJourMontantAchats(int idClient, int achatsEffectues, const char *nomFichierClients) {
    FILE *file;
    Client client;
    int trouve = 0;
    file = fopen(nomFichierClients, "r+b");
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de clients\n");
        return;
    }

    while (fread(&client, sizeof(Client), 1, file)) {
        if (client.idClient == idClient) {
            client.montantAchatsTotal += achatsEffectues;
            client.montantBonus += achatsEffectues / 100;
            fseek(file, -sizeof(Client), SEEK_CUR);
            fwrite(&client, sizeof(Client), 1, file);
            trouve = 1;
            break;
        }
    }

    fclose(file);

    if (!trouve) {
        printf("Client non trouvé\n");
    }
}


void consulterClient(int idClient, const char *nomFichierClients) {
    FILE *file = fopen(nomFichierClients, "rb");
    Client client;
    int trouve = 0;

    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de clients\n");
        return;
    }

    while (fread(&client, sizeof(Client), 1, file)) {
        if (client.idClient == idClient) {
            printf("Informations du client :\n");
            printf("ID du client : %d\n", client.idClient);
            printf("Nom du client : %s\n", client.nom);
            printf("Montant total des achats : %d\n", client.montantAchatsTotal);
            printf("Montant total des bonus : %d\n", client.montantBonus);
            trouve = 1;
            break;
        }
    }

    if (!trouve) {
        printf("Client non trouvé\n");
    }

    fclose(file);
}

int obtenirProchainIDClient(const char *nomFichierClients) {
    FILE *file = fopen(nomFichierClients, "rb");
    int maxID = 0;
    Client client;
    
    if (file == NULL) {
        printf("Erreur lors de l'ouverture du fichier de clients\n");
        return -1;
    }

    while (fread(&client, sizeof(Client), 1, file)) {
        if (client.idClient > maxID) {
            maxID = client.idClient;
        }
    }

    fclose(file);

    return maxID + 1;
}
