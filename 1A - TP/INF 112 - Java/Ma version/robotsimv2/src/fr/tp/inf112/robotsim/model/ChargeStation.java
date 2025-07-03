package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.RectangleShape;

public class ChargeStation extends Component {
	
	// Ajout du style pour les points de chargement
    private static Color backgroundColor = new Color(255, 165, 0); // Orange clair
    private static float thickness = 2.0f; // Épaisseur du trait
    private static float[] dashPattern = null; // Motif de tirets

    // Création d'un objet BasicStroke pour le trait
    private static BasicStroke stroke = new BasicStroke(backgroundColor, thickness, dashPattern);

    // Création du style avec la couleur de fond et les caractéristiques du trait
    private static BasicStyle chargeStationStyle = new BasicStyle(backgroundColor, stroke);

    public ChargeStation(String name, double x, double y, double height, double width) {
        super(name, x, y, height, width, chargeStationStyle);
    }

    @Override
    public RectangleShape getShape() {
        // Retourner la forme rectangulaire de la station de recharge avec les dimensions spécifiées
        return new BasicRectangle(getWidth(), getHeight());
    }
}