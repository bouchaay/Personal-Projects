#ifndef VENTE_H
#define VENTE_H

#include "produit.h"
#include "client.h"

/** Structure d'une vente
 * idClient: Identifiant du client qui a effectué l'achat
 * idVente: Identifiant unique de la vente
 * idProduit: Identifiant du produit vendu
 * quantite: Quantité vendue
 * montantTotal: Montant total de la vente
 * date: Date de la vente
 */
typedef struct {
    int idClient; /* Identifiant du client qui a effectué l'achat */
    int idVente; /* Identifiant unique de la vente */
    int idProduit; /* Identifiant du produit vendu */
    int quantite; /* Quantité vendue */
    double montantTotal; /* Montant total de la vente */
    char date[20]; /* Date de la vente */
} Vente;

/** Récupérer une vente à partir de son identifiant
 * @param idVente L'identifiant de la vente à récupérer
 * @param nomFichier Le nom du fichier binaire où sont stockées les ventes
 * @return La vente correspondant à l'identifiant
 */
Vente recupererVente(int idVente, const char *nomFichierVentes);

/** Enregistrer une vente dans un fichier binaire
 * @param vente La vente à enregistrer
 * @param nomFichier Le nom du fichier binaire pour enregistrer les ventes
 */
void enregistrerVente(Vente vente, const char *nomFichierVentes, const char *nomFichierProduits);

/** Mettre à jour les stocks après une vente
 * @param idProduit L'identifiant du produit vendu
 * @param quantite La quantité vendue
 * @param nomFichier Le nom du fichier binaire où sont stockés les produits
 */
void mettreAJourStock(int idProduit, int quantiteAchete, const char *nomFichierProduits);

/** Consulter l'historique des ventes à partir d'un fichier binaire
 * @param nomFichier Le nom du fichier binaire où sont stockées les ventes
 */
void consulterHistoriqueVentes(const char *nomFichierVentes);

/** Historiques des achats d'un client
 * @param idClient L'identifiant du client
 * @param nomFichier Le nom du fichier binaire où sont stockées les ventes
 */
void historiqueAchatsClient(int idClient, const char *nomFichierVentes);

/** Obtenir le prochain identifiant de vente
 * @param nomFichierVentes Le nom du fichier binaire où sont stockées les ventes
 * @return Le prochain identifiant de vente
 */
int obtenirProchainIDVente(const char *nomFichierVentes);
#endif
