package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.Shape;

public class Area extends Component {
	
	// Ajout du style pour le Robot
    private static Color backgroundColor = new Color(255, 255, 224); // Jaune clair
    private static float thickness = 1.0f; // Épaisseur du trait
    private static float[] dashPattern = null; // Motif de tirets

    // Création d'un objet BasicStroke pour le trait
    private static BasicStroke stroke = new BasicStroke(backgroundColor, thickness, dashPattern);

    // Création du style avec la couleur de fond et les caractéristiques du trait
    private static BasicStyle areaStyle = new BasicStyle(backgroundColor, stroke);

    public Area(String name, double x, double y, double height, double width) {
        super(name, x, y, height, width, areaStyle);
    }

    public String toString() {
        return "Area [name=" + getName() + ", x=" + getxCoordinate() + ", y=" + getyCoordinate() + ", height=" + getHeight() + ", width=" + getWidth() + "]";
    }

    @Override
    public Shape getShape() {
        // Retourner une instance de BasicRectangle avec les dimensions de la zone
        return new BasicRectangle(this.getWidth(), this.getHeight());
    }
}
