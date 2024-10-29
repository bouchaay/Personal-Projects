#ifndef FOURNISSEUR_H
#define FOURNISSEUR_H
#include "produit.h"

/** Structure d'un fournisseur
 * idFournisseur: Identifiant unique du fournisseur
 * nom: Nom du fournisseur
 */
typedef struct {
    int idFournisseur; /* Identifiant unique du fournisseur */
    char nom[50]; /* Nom du fournisseur */
} Fournisseur;

/** Structure d'une commande
 * idFournisseur: Identifiant du fournisseur
 * idCommande: Identifiant unique de la commande
 * produits: Liste des produits commandés (maximum 10 produits)
 * nombreProduits: Nombre de produits dans la commande
 * statutReception: Statut de réception de la commande (0 pour non reçue, 1 pour reçue)
 */
typedef struct {
    int idFournisseur; /* Identifiant du fournisseur */
    int idCommande; /* Identifiant unique de la commande */
    Produit produits[10]; /* Liste des produits commandés (maximum 10 produits) */
    int nombreProduits; /* Nombre de produits dans la commande */
    int statutReception; /* Statut de réception de la commande (0 pour non reçue, 1 pour reçue) */
} Commande;

/** Enregistrer un nouveau fournisseur dans le système
 * @param fournisseur Le fournisseur à enregistrer
 * @param nomFichier Le nom du fichier binaire pour enregistrer les fournisseurs
 */
void enregistrerFournisseur(Fournisseur fournisseur, const char *nomFichierFournisseurs);

/** Supprimer un fournisseur du système
 * @param idFournisseur L'identifiant du fournisseur à supprimer
 * @param nomFichier Le nom du fichier binaire où sont stockés les fournisseurs
 */
void supprimerFournisseur(int idFournisseur, const char *nomFichierFournisseurs);

/** Consulter les informations d'un fournisseur
 * @param idFournisseur L'identifiant du fournisseur à consulter
 * @param nomFichier Le nom du fichier binaire où sont stockés les fournisseurs
 */
void consulterFournisseur(int idFournisseur, const char *nomFichierFournisseurs);

/** Enregistrer une commande dans un fichier binaire
 * @param commande La commande à enregistrer
 * @param nomFichier Le nom du fichier binaire pour enregistrer les commandes
 */
void enregistrerCommande(Commande commande, const char *nomFichierCommandes);

/** Consulter les commandes d'un fournisseur
 * @param idFournisseur L'identifiant du fournisseur
 * @param nomFichier Le nom du fichier binaire où sont stockées les commandes
 */
void consulterCommandesFournisseur(int idFournisseur, const char *nomFichierCommandes);

/** Mettre à jour le statut de réception d'une commande
 * @param idFournisseur L'identifiant du fournisseur
 * @param idCommande L'identifiant de la commande
 * @param statutReception Le statut de réception de la commande
 * @param nomFichier Le nom du fichier binaire où sont stockées les commandes
 */
void mettreAJourStatutReception(int idFournisseur, int idCommande, int statutReception, const char *nomFichierCommandes);

/** Consulter les commandes non reçues
 * @param nomFichier Le nom du fichier binaire où sont stockées les commandes
 */
void consulterCommandesNonRecues(const char *nomFichierCommandes);

/** Obtenir le prochain identifiant de fournisseur disponible
 * @param nomFichierFournisseurs Le nom du fichier binaire où sont stockés les fournisseurs
 * @return Le prochain identifiant de fournisseur disponible
 */
int obtenirProchainIDFournisseur(const char *nomFichierFournisseurs);

/** Obtenir le prochain identifiant de commande disponible
 * @param nomFichierCommandes Le nom du fichier binaire où sont stockées les commandes
 * @return Le prochain identifiant de commande disponible
 */
int obtenirProchainIDCommande(const char *nomFichierCommandes);

#endif
