package fr.tp.inf112.robotsim.model;

import java.util.ArrayList;
import java.util.Collection;

import fr.tp.inf112.projects.canvas.model.*;

public class Factory implements Canvas {
	
	private String Id;
	private String name;
	private int width;
	private int height;
	private ArrayList<Robot> robots;
	private ArrayList<Room> rooms;
	private ArrayList<Area> areas;
	private ArrayList<ChargeStation> chargeStations;
	private ArrayList<Wall> walls;
	
	public Factory(String name, int width, int height) {
        this.name = name;
        this.width = width;
        this.height = height;
        this.robots = new ArrayList<Robot>();
        this.rooms = new ArrayList<Room>();
        this.areas = new ArrayList<Area>();
        this.chargeStations =  new ArrayList<ChargeStation>();
        this.walls = new ArrayList<Wall>();
    }

	// Méthode pour ajouter un robot à l'usine
    public boolean addRobot(String name, double x, double y, double height, double width, double speed) {
        if (!checkRobotName(name)) {
            System.out.println("Le nom du robot doit être unique. Impossible d'ajouter le robot.");
            return false;
        }
        // Le nom du robot est unique, donc ajouter le robot à l'usine
        Robot newRobot = new Robot(name, x, y, height, width, speed); // Créer un nouveau robot avec une vitesse de 0.0
        robots.add(newRobot);
        System.out.println("Robot ajouté avec succès à l'usine.");
        return true;
    }

    // Méthode pour vérifier l'unicité d'un nom de robot
    private boolean checkRobotName(String name) {
        for (Robot robot : robots) {
            if (robot.getName().equals(name)) {
                return false; // Le nom du robot n'est pas unique
            }
        }
        return true; // Le nom du robot est unique
    }
    
    public boolean addRoom(String name, double x, double y, double height, double width) {
    	for (Room room : rooms) {
            if (room.getName().equals(name)) {
                return false; // Le nom de la salle n'est pas unique
            }
        }
        Room newRoom = new Room(name, x, y, height, width);
        rooms.add(newRoom);
        System.out.println("Salle ajoutée avec succès à l'usine.");
        return true;
    }
    
    public boolean addArea(String name, double x, double y, double height, double width) {
    	for (Area area : areas) {
            if (area.getName().equals(name)) {
                return false; // Le nom de la zone n'est pas unique
            }
        }
    	Area newArea = new Area(name, x, y, height, width);
        areas.add(newArea);
        System.out.println("Zone ajoutée avec succès à l'usine.");
        return true;
    }
    
    public boolean addStation(String name, double x, double y, double height, double width) {
    	for (ChargeStation chargeStation : chargeStations) {
            if (chargeStation.getName().equals(name)) {
                return false; // Le nom de la station de charge n'est pas unique
            }
        }
    	ChargeStation newChargeStation = new ChargeStation((String) name, x, y, height, width);
        chargeStations.add(newChargeStation);
        System.out.println("Station de charge ajoutée avec succès à l'usine.");
        return true;
		
	}

 // Méthode pour afficher le nom de l'usine et la liste de ses robots, Rooms, Areas et ChargeStations à la console
    public void printToConsole() {
        System.out.println("Nom de l'usine : " + name);
        System.out.println("Liste des robots :");
        for (Robot robot : robots) {
            System.out.println("- " + robot.getName());
        }
        System.out.println("Liste des Rooms :");
        for (Room room : rooms) {
            System.out.println("- " + room.getName());
        }
        System.out.println("Liste des Areas :");
        for (Area area : areas) {
            System.out.println("- " + area.getName());
        }
        System.out.println("Liste des ChargeStations :");
        for (ChargeStation chargeStation : chargeStations) {
            System.out.println("- " + chargeStation.getName());
        }
    }
    
    public String getName() {
        return name;
    }

    public Collection<Figure> getFigures() {
        // Retourner une collection de figures représentant les éléments de l'usine
        ArrayList<Figure> figures = new ArrayList<Figure>();
        figures.addAll(robots);
        figures.addAll(rooms);
        figures.addAll(areas);
        figures.addAll(chargeStations)    ;    
        return figures;
    }
    
    public void createWalls() {
    	for (Room room : rooms) {
    		double topLeftx = room.getxCoordinate();
    		double topLefty = room.getyCoordinate();
    		double height = room.getHeight();
    		double width = room.getWidth();
    		Wall newWall = new Wall(null, topLeftx, topLefty, height, 0.0);
    		walls.add(newWall); // Celui du haut
			newWall = new Wall(null, topLeftx, topLefty, 0.0, width);
			walls.add(newWall); // Celui de gauche
			newWall = new Wall(null, topLeftx+width, topLefty, height, 0.0);
			walls.add(newWall);
			newWall = new Wall(null, topLeftx, topLefty+height, 0.0, width);
			walls.add(newWall);	
    	}
    }
    
    // Déclaration des méthodes de Canvas
    public Style getStyle() {
        return null;
    }
    public String getId() {
        return Id;
    }
    public void setId(String id) {
        this.Id = id;
    }
     public int getWidth() {
        return width;
     }
    public int getHeight() {
        return height;
    }
}