package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.Shape;

public class Door extends Component {

    public Door(String name, double x, double y, double height, double width, BasicStyle style) {
        super(name, x, y, height, width, style);
    }

    @Override
    public Shape getShape() {
        // Retourner la forme rectangulaire de la porte avec les dimensions de la porte
        return new BasicRectangle(this.getWidth(), this.getHeight());
    }
}
