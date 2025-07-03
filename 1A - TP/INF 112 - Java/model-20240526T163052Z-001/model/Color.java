package fr.tp.inf112.robotsim.model;

public class Color implements fr.tp.inf112.projects.canvas.model.Color{
	
	private int red;
	private int green;
	private int blue;
	
	public Color(int red, int green, int blue) {
        this.red = red;
        this.green = green;
        this.blue = blue;
    }

	public int getRedComponent() {
		return this.red;
	}
	
	public int getGreenComponent() {
		return this.green;
	}
	
	public int getBlueComponent() {
		return this.blue;
	}
}
