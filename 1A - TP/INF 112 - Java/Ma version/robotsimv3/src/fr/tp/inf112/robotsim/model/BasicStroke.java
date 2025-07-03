package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.Stroke;

public class BasicStroke implements Stroke {
    private Color color;
    private float thickness;
    private float[] dashPattern;

    public BasicStroke(Color color, float thickness, float[] dashPattern) {
        this.color = color;
        this.thickness = thickness;
        this.dashPattern = dashPattern;
    }
    public Color getColor() {
        return color;
    }
    public float getThickness() {
        return thickness;
    }

    public float[] getDashPattern() {
        return dashPattern;
    }
}
