package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.Color;
import fr.tp.inf112.projects.canvas.model.Stroke;
import fr.tp.inf112.projects.canvas.model.Style;

public class BasicStyle implements Style {
    private Color backgroundColor;
    private Stroke stroke;

    public BasicStyle(Color backgroundColor, Stroke stroke) {
        this.backgroundColor = backgroundColor;
        this.stroke = stroke;
    }

    public Color getBackgroundColor() {
        return backgroundColor;
    }

    public Stroke getStroke() {
        return stroke;
    }
}
