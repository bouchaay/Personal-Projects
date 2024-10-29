#ifndef PRODUIT_H
#define PRODUIT_H

/** Structure d'un produit
 * id: L'identifiant du produit
 * nom: Le nom du produit
 * prix: Le prix du produit
 * quantite: La quantité de produit en stock
 */
typedef struct {
    int id;
    char nom[50];
    double prix;
    int quantite;
} Produit;

/** Ajouter un produit à la liste des produits
 * @param nouveauProduit Le produit à ajouter
 * @param nomFichier Le nom du fichier binaire où les produits sont stockés
 */
void ajouterProduit(Produit nouveauProduit, const char *nomFichierProduits);

/** Supprimer un produit de la liste des produits
 * @param idProduit L'identifiant du produit à supprimer
 * @param nomFichier Le nom du fichier binaire où les produits sont stockés
 */
void supprimerProduit(int idProduit, const char *nomFichierProduits);

/** Modifier le nom d'un produit
 * @param idProduit L'identifiant du produit à modifier
 * @param nouveauNom Le nouveau nom du produit
 * @param nomFichier Le nom du fichier binaire où les produits sont stockés
 */
void modifierNomProduit(int idProduit, const char *nouveauNom, const char *nomFichierProduits);

/** Modifier le prix d'un produit
 * @param idProduit L'identifiant du produit à modifier
 * @param nouveauPrix Le nouveau prix du produit
 * @param nomFichier Le nom du fichier binaire où les produits sont stockés
 */
void modifierPrixProduit(int idProduit, double nouveauPrix, const char *nomFichierProduits);

/** Modifier la quantité d'un produit
 * @param idProduit L'identifiant du produit à modifier
 * @param nouvelleQuantite La nouvelle quantité du produit
 * @param nomFichier Le nom du fichier binaire où les produits sont stockés
 */
void modifierQuantiteProduit(int idProduit, int quantiteAchete, const char *nomFichierProduits);

/** Afficher la liste des produits
 * @param nomFichier Le nom du fichier binaire où les produits sont stockés
 */
void afficherStock(const char *nomFichierProduits);

/** Obtenir le prochain identifiant de produit disponible
 * @param nomFichierProduits Le nom du fichier binaire où les produits sont stockés
 * @return Le prochain identifiant de produit disponible
 */
int obtenirProchainIDProduit(const char *nomFichierProduits);

/** Obtenir le prix d'un produit à partir de son identifiant
 * @param idProduit L'identifiant du produit
 * @param nomFichierProduits Le nom du fichier binaire où les produits sont stockés
 * @return Le prix du produit
 */
double obtenirPrixProduit(int idProduit, const char *nomFichierProduits);


#endif
