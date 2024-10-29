#ifndef FILES_H
#define FILES_H

extern char *nomFichierProduits;
extern char *nomFichierVentes;
extern char *nomFichierClients;
extern char *nomFichierFournisseurs;
extern char *nomFichierCommandes;
extern char *nomFichierEmployes;

/** Vider un fichier
 * @param nomFichier Le nom du fichier à vider
 */
void viderFichier(const char *nomFichier);

#endif
