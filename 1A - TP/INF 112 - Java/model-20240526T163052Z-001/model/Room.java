package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.RectangleShape;

public class Room extends Component {

	// Ajout du style pour les salles
    private static Color backgroundColor = new Color(173, 216, 230); // Bleu clair
    private static float thickness = 3.0f; // Épaisseur du trait
    private static float[] dashPattern = null; // Motif de tirets

    // Création d'un objet BasicStroke pour le trait
    private static BasicStroke stroke = new BasicStroke(backgroundColor, thickness, dashPattern);

    // Création du style avec la couleur de fond et les caractéristiques du trait
    private static BasicStyle roomStyle = new BasicStyle(backgroundColor, stroke);

	
    public Room(String name, double x, double y, double height, double width) {
    	super(name, x, y, height, width, roomStyle);
    }

    @Override
    public String toString() {
        return "Room [name=" + getName() + ", x=" + getxCoordinate() + ", y=" + getyCoordinate() + ", height=" + getHeight() + ", width=" + getWidth() + "]";
    }
    @Override
    public RectangleShape getShape() {
        // Retourner une forme rectangulaire avec les dimensions de la salle
        return new BasicRectangle(this.getWidth(), this.getHeight());
    }
}