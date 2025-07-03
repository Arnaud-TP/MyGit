package fr.tp.inf112.robotsim.model;
import java.util.ArrayList;

public class Factory {
	
	private String name;
	private ArrayList<Robot> robots = new ArrayList<Robot>();
	
	public Factory(String name) {
		super();
		this.name = name;
	}
	
	private boolean checkRobotName(String name) {
		for (Robot robot : robots) {
			if (robot.getName().equals(name)) {
				return false; /* Nom déjà utilisé */
			}
		}
		return true; /* Pas de robot déjà présent dans la liste avec ce nom*/
	}
	
	public boolean addRobot(String name) {
		if (checkRobotName(name)) {
			robots.add(new Robot(name,0.0));
			return true;
			}
		else {
			return false;
		}
	}
	
	/* Permet d'accéder au nom de l'usine*/
	public String getName() {
		return name;
	}
	
	@Override
	public String toString() {
		return "Nom de l'usine : "+name;
	}
	
	public void printToConsole() {
		System.out.println("\n"+toString()); /*Ajout d'un saut de ligne au début*/
		System.out.println("Cette usine contient les robots : ");
		for (Robot robot : robots) {
			System.out.println(robot.getName());
		}
		System.out.println(); /*Ajout d'un saut de ligne à la fin*/
	}
}
