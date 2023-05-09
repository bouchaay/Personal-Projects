package user;

// Classe de l'utilisateur
public class utilisateur {

    private int id;
    private String nom;
    private String prenom;
    private String email;
    private int nombreEmprunt;

    // Constructeur
    public utilisateur(int id, String nom, String prenom, String email) {
        this.id = id;
        this.nom = nom;
        this.prenom = prenom;
        this.email = email;
        this.nombreEmprunt = 0;
    }

    public int getId() {
        return id;
    }

    public String getNom() {
        return nom;
    }

    public String getPrenom() {
        return prenom;
    }

    public String getEmail() {
        return email;
    }

    public int getNombreEmprunt() {
        return nombreEmprunt;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public void setPrenom(String prenom) {
        this.prenom = prenom;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void incrementerEmprunt() {
        this.nombreEmprunt++;
    }
}


