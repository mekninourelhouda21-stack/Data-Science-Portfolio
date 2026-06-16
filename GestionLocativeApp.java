import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

// ==========================================
// 1. MODÈLE DE DONNÉES (POO) : Classe BienImmobilier
// ==========================================
class BienImmobilier {
    private String id;
    private String type; // Appartement, Maison, Studio
    private String ville;
    private double prixLoyer;
    private boolean disponible;

    public BienImmobilier(String id, String type, String ville, double prixLoyer, boolean disponible) {
        this.id = id;
        this.type = type;
        this.ville = ville;
        this.prixLoyer = prixLoyer;
        this.disponible = disponible;
    }

    // Getters et Setters (Principes d'Encapsulation POO)
    public String getId() { return id; }
    public String getType() { return type; }
    public String getVille() { return ville; }
    public double getPrixLoyer() { return prixLoyer; }
    public boolean isDisponible() { return disponible; }
}

// ==========================================
// 2. APPLICATION PRINCIPALE ET INTERFACE GRAPHIQUE (GUI)
// ==========================================
public class GestionLocativeApp extends JFrame {
    private List<BienImmobilier> baseDeDonnees = new ArrayList<>();
    private DefaultTableModel tableModel;
    
    // Composants du formulaire de recherche multicritères
    private JComboBox<String> filterType;
    private JTextField filterVille;
    private JTextField filterPrixMax;

    public GestionLocativeApp() {
        // Configuration de la fenêtre principale Java Swing
        setTitle("SUNe Loc - Gestion Locative & Optimisation de Flux");
        setSize(850, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(10, 10));

        // Initialisation de la base de données avec quelques exemples
        baseDeDonnees.add(new BienImmobilier("B001", "Studio", "Lyon", 550.0, true));
        baseDeDonnees.add(new BienImmobilier("B002", "Appartement", "Villeurbanne", 850.0, true));
        baseDeDonnees.add(new BienImmobilier("B003", "Maison", "Lyon", 1400.0, false));
        baseDeDonnees.add(new BienImmobilier("B004", "Studio", "Lyon", 480.0, true));

        // --- PANNEAU DE RECHERCHE MULTICRITÈRES (Haut) ---
        JPanel searchPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 15, 10));
        searchPanel.setBorder(BorderFactory.createTitledBorder("Moteur de Recherche Multicritères (Flux de Données)"));

        searchPanel.add(new JLabel("Type :"));
        filterType = new JComboBox<>(new String[]{"Tous", "Studio", "Appartement", "Maison"});
        searchPanel.add(filterType);

        searchPanel.add(new JLabel("Ville :"));
        filterVille = new JTextField(10);
        searchPanel.add(filterVille);

        searchPanel.add(new JLabel("Loyer Max (€) :"));
        filterPrixMax = new JTextField(6);
        searchPanel.add(filterPrixMax);

        JButton btnSearch = new JButton("Filtrer les Biens");
        btnSearch.setBackground(new Color(43, 108, 176));
        btnSearch.setForeground(Color.WHITE);
        searchPanel.add(btnSearch);
        
        add(searchPanel, BorderLayout.NORTH);

        // --- TABLEAU DE VISUALISATION (Centre) ---
        String[] colonnes = {"ID Bien", "Type de Bien", "Ville", "Loyer Mensuel", "Statut Disponibilité"};
        tableModel = new DefaultTableModel(colonnes, 0);
        JTable table = new JTable(tableModel);
        add(new JScrollPane(table), BorderLayout.CENTER);

        // --- PANNEAU DES ACTIONS CRUD (Bas) ---
        JPanel crudPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 10));
        JButton btnCreate = new JButton("[C] Ajouter un Bien");
        JButton btnDelete = new JButton("[D] Supprimer Sélection");
        crudPanel.add(btnCreate);
        crudPanel.add(btnDelete);
        add(crudPanel, BorderLayout.SOUTH);

        // Affichage initial des données
        rafraichirTableau(baseDeDonnees);

        // ==========================================
        // 3. LOGIQUE ALGORITHMIQUE & ÉVÉNEMENTS
        // ==========================================

        // Action Recherche Multicritères (Algorithme de filtrage via l'API Stream de Java)
        btnSearch.addActionListener(e -> {
            String typeSelectionne = (String) filterType.getSelectedItem();
            String villeSaisie = filterVille.getText().trim().toLowerCase();
            String prixSaisi = filterPrixMax.getText().trim();

            List<BienImmobilier> resultats = baseDeDonnees.stream()
                .filter(b -> typeSelectionne.equals("Tous") || b.getType().equalsIgnoreCase(typeSelectionne))
                .filter(b -> villeSaisie.isEmpty() || b.getVille().toLowerCase().contains(villeSaisie))
                .filter(b -> {
                    if (prixSaisi.isEmpty()) return true;
                    try { return b.getPrixLoyer() <= Double.parseDouble(prixSaisi); } 
                    catch (NumberFormatException ex) { return true; }
                })
                .collect(Collectors.toList());

            rafraichirTableau(resultats);
        });

        // Action CREATE (Ajouter un élément dans le flux)
        btnCreate.addActionListener(e -> {
            JTextField idIn = new JTextField();
            JTextField typeIn = new JTextField();
            JTextField villeIn = new JTextField();
            JTextField prixIn = new JTextField();
            
            Object[] message = {
                "ID Unique:", idIn,
                "Type (Studio/Appartement/Maison):", typeIn,
                "Ville:", villeIn,
                "Loyer (€):", prixIn
            };

            int option = JOptionPane.showConfirmDialog(null, message, "Ajouter un nouveau bien locatif", JOptionPane.OK_CANCEL_OPTION);
            if (option == JOptionPane.OK_OPTION && !idIn.getText().isEmpty()) {
                try {
                    BienImmobilier nouveauBien = new BienImmobilier(
                        idIn.getText(),
                        typeIn.getText(),
                        villeIn.getText(),
                        Double.parseDouble(prixIn.getText()),
                        true
                    );
                    baseDeDonnees.add(nouveauBien);
                    rafraichirTableau(baseDeDonnees);
                    JOptionPane.showMessageDialog(this, "Bien ajouté avec succès au système !");
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(this, "Erreur : Format du prix invalide.");
                }
            }
        });

        // Action DELETE (Supprimer un élément du flux)
        btnDelete.addActionListener(e -> {
            int ligneSelectionnee = table.getSelectedRow();
            if (ligneSelectionnee != -1) {
                String idASupprimer = (String) tableModel.getValueAt(ligneSelectionnee, 0);
                baseDeDonnees.removeIf(b -> b.getId().equals(idASupprimer));
                rafraichirTableau(baseDeDonnees);
                JOptionPane.showMessageDialog(this, "Bien supprimé de la base de données.");
            } else {
                JOptionPane.showMessageDialog(this, "Veuillez sélectionner une ligne dans le tableau à supprimer.");
            }
        });
    }

    // Méthode utilitaire pour mettre à jour la vue de la GUI
    private void rafraichirTableau(List<BienImmobilier> liste) {
        tableModel.setRowCount(0); // Vider le tableau actuel
        for (BienImmobilier b : liste) {
            tableModel.addRow(new Object[]{
                b.getId(), 
                b.getType(), 
                b.getVille(), 
                b.getPrixLoyer() + " €", 
                b.isDisponible() ? "Disponible" : "Loué"
            });
        }
    }

    // Point d'entrée de la JVM (Java Virtual Machine)
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new GestionLocativeApp().setVisible(true);
        });
    }
}