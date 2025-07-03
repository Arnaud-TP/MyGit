package fr.tp.inf112.robotsim.model;

import java.util.ArrayList;

import fr.tp.inf112.projects.canvas.model.Shape;

public class Robot extends Component {
    private double speed;
    private ArrayList<Component> componentsToVisit;
    private int currentTargetIndex;
    private Factory factory;
    
    // Ajout du style pour le Robot
    private static Color backgroundColor = new Color(255, 0, 0); // Rouge vif
    private static float thickness = 1.0f; // Épaisseur du trait
    private static float[] dashPattern = {5.0f, 2.0f}; // Motif de tirets

    // Création d'un objet BasicStroke pour le trait
    private static BasicStroke stroke = new BasicStroke(backgroundColor, thickness, dashPattern);

    // Création du style avec la couleur de fond et les caractéristiques du trait
    private static BasicStyle robotStyle = new BasicStyle(backgroundColor, stroke);

    // Constructeur
    public Robot(String name, double x, double y, double height, double width, double speed,Factory factory) {
        super(name, x, y, height, width, robotStyle);  // Appel au constructeur de Component
        this.speed = speed;
    }

    // Getter pour speed
    public double getSpeed() {
        return speed;
    }

    // Setter pour speed
    public void setSpeed(double speed) {
        this.speed = speed;
    }

    // Redéfinir la méthode toString() pour inclure les détails spécifiques à Robot
    @Override
    public String toString() {
        return "Je m'appelle " + getName() + ", j'avance à " + speed + " km/h. Ma position est (" + getxCoordinate() + ", " + getyCoordinate() + ") et mes dimensions sont " + getHeight() + "x" + getWidth() + ".";
    }

    @Override
    public Shape getShape() {
        // Retourner une forme ovale pour le robot
        return new BasicOval((int) getWidth(), (int) getHeight());
    }
    
    public void setComponentsToVisit(ArrayList<Component> components) {
        this.componentsToVisit = components;
    }

    @Override
    public void behave() {
        if (componentsToVisit != null && !componentsToVisit.isEmpty()) {
            Component target = componentsToVisit.get(currentTargetIndex);
            if (hasReached(target)) {
                currentTargetIndex = (currentTargetIndex + 1) % componentsToVisit.size();
                target = componentsToVisit.get(currentTargetIndex);
            }
            moveTowards(target);
        }
    }

    private boolean hasReached(Component target) {
        return this.getxCoordinate() == target.getxCoordinate() && this.getyCoordinate() == target.getyCoordinate();
    }

    private void moveTowards(Component target) {
        double targetX = target.getxCoordinate();
        double targetY = target.getyCoordinate();
        double deltaX = targetX - this.getxCoordinate();
        double deltaY = targetY - this.getyCoordinate();
        double distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

        if (distance > speed) {
            this.setX(this.getX() + (deltaX / distance) * speed);
            this.setY(this.getY() + (deltaY / distance) * speed);
        } else {
            this.setX(targetX);
            this.setY(targetY);
        }
        factory.notifyObservers();
    }
}
