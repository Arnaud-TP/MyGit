package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.model.Figure;
import fr.tp.inf112.projects.canvas.model.Style;
import fr.tp.inf112.projects.canvas.model.Shape;

public abstract class Component implements Figure {
    private String name;
    private double x;
    private double y;
    private int height;
    private int width;
    protected BasicStyle style;

    public Component(String name, double x, double y, double height, double width, BasicStyle style) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.height = (int) height;
        this.width = (int) width;
        this.style = (BasicStyle) style;
    }

    public String getName() {
        return name;
    }

    public int getxCoordinate() {
        return (int) x;
    }

    public int getyCoordinate() {
        return (int) y;
    }

    public Style getStyle() {
        return style;
    }

    public abstract Shape getShape(); //La méthode getShape() est implémentée par chaque objet qui dérive de Component

	protected int getHeight() {
		return height;
	}

	protected int getWidth() {
		return width;
	}
}
