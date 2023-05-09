package user;

public class livre {

    private int id;
    private String nom;
    private int idEmprunteur;

    // Constructeur
    public livre(int id, String nom) {
        this.id = id;
        this.nom = nom;
        this.idEmprunteur = -1;
    }

    public int getId() {
        return id;
    }

    public String getNom() {
        return nom;
    }

    public int getIdEmprunteur() {
        return idEmprunteur;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public void setIdEmprunteur(int idEmprunteur) {
        this.idEmprunteur = idEmprunteur;
    }
}
