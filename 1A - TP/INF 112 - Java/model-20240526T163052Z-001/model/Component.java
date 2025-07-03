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
        this.setX(x);
        this.setY(y);
        this.height = (int) height;
        this.width = (int) width;
        this.style = (BasicStyle) style;
    }

    public String getName() {
        return name;
    }

    public int getxCoordinate() {
        return (int) getX();
    }

    public int getyCoordinate() {
        return (int) getY();
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
	public void behave() {
        // Comportement par défaut, à redéfinir dans les sous-classes
    }

	public double getX() {
		return x;
	}

	public void setX(double x) {
		this.x = x;
	}

	public double getY() {
		return y;
	}

	public void setY(double y) {
		this.y = y;
	}
}
