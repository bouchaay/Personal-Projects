#ifndef CONNEXION_H
#define CONNEXION_H

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/** Structure d'un employé
 * username: Le nom d'utilisateur
 * password: Le mot de passe
 * isManager: true si l'employé est un manager, false sinon
 */
typedef struct {
    char username[50]; /* Le nom d'utilisateur */
    char password[50]; /* Le mot de passe */
    bool isManager; /* true si l'employé est un manager, false sinon */
} Employe;

/** Fonction pour se connecter
 * @param username Le nom d'utilisateur
 * @param password Le mot de passe
 * @param fichierEmployes Le fichier contenant les employés
 * @return true si la connexion est réussie, false sinon
 */
bool seConnecter(const char *username, const char *password, const char *fichierEmployes);

/** Fonction pour ajouter un employé
 * @param manager L'employé qui ajoute l'autre employé
 * @param employe L'employé à ajouter
 * @param fichierEmployes Le fichier contenant les employés
 */
void ajouterEmploye(Employe manager, Employe employe, const char *fichierEmployes);

/** Supprimer un employé
 * @param manager L'employé qui supprime l'autre employé
 * @param username Le nom d'utilisateur de l'employé à supprimer
 * @param fichierEmployes Le fichier contenant les employés
 */
void supprimerEmploye(Employe manager, const char *username, const char *fichierEmployes);

/** Fonction pour vérifier si un employé est un manager
 * @param username Le nom d'utilisateur
 * @param fichierEmployes Le fichier contenant les employés
 * @return true si l'employé est un manager, false sinon
 */
bool estManager(const char *username, const char *fichierEmployes);

#endif
