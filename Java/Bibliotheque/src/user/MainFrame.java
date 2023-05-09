package user;

import javax.swing.*;
import java.awt.*;

// Fenetre principale de l'application
public class MainFrame extends JFrame {

    // Constructeur
    public MainFrame() {
        super("Bibliothèque");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(800, 600);
        this.setLocationRelativeTo(null);
        this.setResizable(false);
        this.setLayout(new BorderLayout());

        // 4 panels pour les 4 coins de la fenetre
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(3, 3));

        // Label et textfield pour le nom
        JLabel nomLabel = new JLabel("Nom");
        JTextField nomTextField = new JTextField();
        panel.add(nomLabel);

        // Label et textfield pour le prenom
        JLabel prenomLabel = new JLabel("Prenom");
        JTextField prenomTextField = new JTextField();
        panel.add(prenomLabel);

        // Label et textfield pour l'email
        JLabel emailLabel = new JLabel("Email");
        JTextField emailTextField = new JTextField();
        panel.add(emailLabel);

        // Bouton pour ajouter un utilisateur
        JButton ajouterUtilisateurButton = new JButton("Ajouter utilisateur");
        ajouterUtilisateurButton.addActionListener(e -> {
            String nom = nomTextField.getText();
            String prenom = prenomTextField.getText();
            String email = emailTextField.getText();
            if (nom.equals("") || prenom.equals("") || email.equals("")) {
                JOptionPane.showMessageDialog(null, "Veuillez remplir tous les champs");
                return;
            }
            utilisateur utilisateur = new utilisateur(-1, nom, prenom, email);
            BaseDonnee.executeInsert("INSERT INTO utilisateurs (nom, prenom, email) VALUES ('" + nom + "', '" + prenom + "', '" + email + "')");
            JOptionPane.showMessageDialog(null, "Utilisateur ajouté avec succès");
        });

        // Boutton supprimer utilisateur
        JButton supprimerUtilisateurButton = new JButton("Supprimer utilisateur");
        supprimerUtilisateurButton.addActionListener(e -> {
            String nom = nomTextField.getText();
            String prenom = prenomTextField.getText();
            String email = emailTextField.getText();
            if (nom.equals("") || prenom.equals("") || email.equals("")) {
                JOptionPane.showMessageDialog(null, "Veuillez remplir tous les champs");
                return;
            }
            utilisateur utilisateur = new utilisateur(-1, nom, prenom, email);
            BaseDonnee.executeInsert("DELETE FROM utilisateurs WHERE nom = '" + nom + "' AND prenom = '" + prenom + "' AND email = '" + email + "'");
            JOptionPane.showMessageDialog(null, "Utilisateur supprimé avec succès");
        });

        // Boutton pour afficher les utilisateurs
        JButton afficherUtilisateursButton = new JButton("Afficher utilisateurs");
        afficherUtilisateursButton.addActionListener(e -> {
            String[] columnNames = {"ID", "Nom", "Prenom", "Email", "Nombre d'emprunts"};
            String[][] data = BaseDonnee.executeSelect("SELECT * FROM utilisateurs");
            JTable table = new JTable(data, columnNames);
            JScrollPane scrollPane = new JScrollPane(table);
            JFrame frame = new JFrame("Utilisateurs");
            frame.add(scrollPane);
            frame.setSize(800, 600);
            frame.setVisible(true);
        });
        // Ajouter les composants au panel l'une sous l'autre
        panel.add(nomTextField);
        panel.add(prenomTextField);
        panel.add(emailTextField);
        panel.add(ajouterUtilisateurButton);
        panel.add(supprimerUtilisateurButton);
        panel.add(afficherUtilisateursButton);

        // Ajouter le panel au centre de la fenetre
        this.add(panel, BorderLayout.CENTER);


        this.setVisible(true);
    }

    public static void main(String[] args) {
        new MainFrame();
    }
}
