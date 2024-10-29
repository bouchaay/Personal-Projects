#ifndef MENUAPP_H
#define MENUAPP_H

#include <stdio.h>
#include <stdlib.h>
#include "files.h"
#include "produit.h"
#include "vente.h"
#include "client.h"
#include "fournisseur.h"
#include "stdbool.h"
#include "connexion.h"

int afficherMenu(bool isManager);
void gestionProduits(const char *nomFichierProduits, bool isManager);
void gestionVentes(const char *nomFichierVentes, const char *nomFichierProduits, bool isManager);
void gestionClients(const char *nomFichierClients, bool isManager);
void gestionFournisseurs(const char *nomFichierFournisseurs, bool isManager);
void gestionEmployes(const char *nomFichierEmployes);
void menuPrincipal();
void menuPrincipalNonManager();
void menuConnexion();
bool premiereUtilisation();

#endif
