package fr.tp.inf112.robotsim.model;

public class Robot {

	private String name;
	private double speed;
	
	public Robot(String name, double speed) {
		super();
		this.name = name;
		this.speed = speed;
	}
	
	@Override
	public String toString() {
		return "Je m'appelle "+name+" et j'avance à "+speed+" km/h.";
	}
	
	/* Permet d'accéder au nom du robot*/
	public String getName() {
		return name;
	}
	
	/* Permet d'accéder à la vitesse du robot*/
	public double getSpeed() {
		return speed;
	}
	
	/* Permet de modifier la vitesse du robot*/
	public void setSpeed(double new_speed) {
		this.speed = new_speed;
	}
}