package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.RectangleShape;

public class Wall extends Component{
	// Ajout du style pour les murs
    private static Color backgroundColor = new Color(0, 0, 0); // Noir
    private static float thickness = 1.0f; // Épaisseur du trait
    private static float[] dashPattern = null; // Pas de tirets

    // Création d'un objet BasicStroke pour le trait
    private static BasicStroke stroke = new BasicStroke(backgroundColor, thickness, dashPattern);

    // Création du style avec la couleur de fond et les caractéristiques du trait
    private static BasicStyle wallStyle = new BasicStyle(backgroundColor, stroke);

    // Création de la liste des murs
    public Wall(String name, double x, double y, double height, double width) {
        super(name, x, y, height, width, wallStyle);
    }

    public String toString() {
        return "Wall [name=" + getName() + ", x=" + getxCoordinate() + ", y=" + getyCoordinate() + ", height=" + getHeight() + ", width=" + getWidth() + "]";
    }

    @Override
    public RectangleShape getShape() {
        // Retourner une instance de BasicRectangle avec les dimensions de la zone
        return new BasicRectangle(this.getWidth(), this.getHeight());
    }
}
