#ifndef CLIENT_H
#define CLIENT_H

/** Structure d'un client
 * idClient: Identifiant unique du client
 * nom: Nom du client
 * montantAchatsTotal: Montant total des achats effectués par le client
 * montantBonus: Montant total des bonus accumulés par le client = 1% des achats
 */
typedef struct {
    int idClient; /* Identifiant unique du client */
    char nom[50]; /* Nom du client */
    int montantAchatsTotal; /* Montant total des achats effectués par le client */
    int montantBonus; /* Montant total des bonus accumulés par le client = 1% des achats */
} Client;

/** Enregistrer un nouveau client dans le système
 * @param client Le client à enregistrer
 * @param nomFichier Le nom du fichier binaire pour enregistrer les clients
 */
void enregistrerClient(Client client, const char *nomFichierClients);

/** Supprimer un client du système
 * @param idClient L'identifiant du client à supprimer
 * @param nomFichier Le nom du fichier binaire où sont stockés les clients
 */
void supprimerClient(int idClient, const char *nomFichierClients);

/** Mise à jour du montant total des achats d'un client
 * @param idClient L'identifiant du client
 * @param montantAchats Le montant total des achats effectués par le client
 * @param nomFichier Le nom du fichier binaire où sont stockés les clients
 */
void mettreAJourMontantAchats(int idClient, int achatsEffectues, const char *nomFichierClients);

/** Consulter les informations d'un client
 * @param idClient L'identifiant du client à consulter
 * @param nomFichier Le nom du fichier binaire où sont stockés les clients
 */
void consulterClient(int idClient, const char *nomFichierClients);

/** Récupérer le prochain identifiant de client disponible
 * @param nomFichierClients Le nom du fichier binaire où sont stockés les clients
 * @return Le prochain identifiant de client disponible
 */
int obtenirProchainIDClient(const char *nomFichierClients);

#endif
