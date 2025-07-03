package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.OvalShape;

public class BasicOval implements OvalShape {
    private int width;
    private int height;

    public BasicOval(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }
}
