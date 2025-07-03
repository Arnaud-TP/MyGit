package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.RectangleShape;

public class BasicRectangle implements RectangleShape {
    private int width;
    private int height;

    public BasicRectangle(int d, int e) {
        this.width = d;
        this.height = e;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }
}
