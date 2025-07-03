package fr.tp.inf112.robotsim.model;

import java.util.ArrayList;
import java.util.Collection;

import fr.tp.inf112.projects.canvas.controller.Observer;
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
    private ArrayList<Observer> observers;
    private boolean simulationStarted;

    public Factory(String name, int width, int height) {
        this.name = name;
        this.width = width;
        this.height = height;
        this.robots = new ArrayList<Robot>();
        this.rooms = new ArrayList<Room>();
        this.areas = new ArrayList<Area>();
        this.chargeStations = new ArrayList<ChargeStation>();
        this.walls = new ArrayList<Wall>();
        this.observers = new ArrayList<Observer>();
        this.simulationStarted = false;
    }

    // Méthode pour ajouter un robot à l'usine
    public boolean addRobot(String name, double x, double y, double height, double width, double speed) {
        if (!checkRobotName(name)) {
            System.out.println("Le nom du robot doit être unique. Impossible d'ajouter le robot.");
            return false;
        }
        Robot newRobot = new Robot(name, x, y, height, width, speed, this); 
        robots.add(newRobot);
        System.out.println("Robot ajouté avec succès à l'usine.");
        return true;
    }

    // Cela permet de vérifier que le nom du robot est unique
    private boolean checkRobotName(String name) {
        for (Robot robot : robots) {
            if (robot.getName().equals(name)) {
                return false; 
            }
        }
        return true;
    }
    
    public Robot getRobot(String name) {
        for (Robot robot : robots) {
            if (robot.getName().equals(name)) {
                return robot;
            }
        }
        return null;
    }

    public boolean addRoom(String name, double x, double y, double height, double width) {
        for (Room room : rooms) {
            if (room.getName().equals(name)) {
                return false; 
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
                return false; 
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
                return false; 
            }
        }
        ChargeStation newChargeStation = new ChargeStation(name, x, y, height, width);
        chargeStations.add(newChargeStation);
        System.out.println("Station de charge ajoutée avec succès à l'usine.");
        return true;
    }

    public void addWall(Wall wall) {
        walls.add(wall);
    }

    public void createWalls() {
        for (Room room : rooms) {
            double topLeftx = room.getxCoordinate();
            double topLefty = room.getyCoordinate();
            double height = room.getHeight();
            double width = room.getWidth();
            
            walls.add(new Wall(" ", topLeftx, topLefty, 0, width)); // Mur du haut
            walls.add(new Wall(" ", topLeftx, topLefty + height, 0, width)); // Mur du bas
            walls.add(new Wall(" ", topLeftx, topLefty, height, 0)); // Mur de gauche
            walls.add(new Wall(" ", topLeftx + width, topLefty, height, 0)); // Mur de droite
        }
    }

    // Méthode pour afficher le nom de l'usine et la liste de ses composants à la console
    public void printToConsole() {
        System.out.println("Nom de l'usine : " + name);
        System.out.println("Liste des robots :");
        for (Robot robot : robots) {
            System.out.println("- " + robot.getName());
        }
        System.out.println("Liste des salles :");
        for (Room room : rooms) {
            System.out.println("- " + room.getName());
        }
        System.out.println("Liste des zones :");
        for (Area area : areas) {
            System.out.println("- " + area.getName());
        }
        System.out.println("Liste des stations de charge :");
        for (ChargeStation chargeStation : chargeStations) {
            System.out.println("- " + chargeStation.getName());
        }
    }
    
    public void behave() {
        for (Robot robot : robots) {
            robot.behave();
        }
        notifyObservers();
    }

    public void startSimulation() {
        simulationStarted = true;
        notifyObservers();
    }

    public void stopSimulation() {
        simulationStarted = false;
        notifyObservers();
    }

    public boolean isSimulationStarted() {
        return simulationStarted;
    }

    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.modelChanged();
        }
    }

    public boolean addObserver(Observer observer) {
        if (!observers.contains(observer)) {
            observers.add(observer);
            return true;
        }
        return false;
    }

    public boolean removeObserver(Observer observer) {
        return observers.remove(observer);
    }
    
    public String getName() {
        return name;
    }

    public Collection<Figure> getFigures() {
        ArrayList<Figure> figures = new ArrayList<Figure>();
        figures.addAll(robots);
        figures.addAll(rooms);
        figures.addAll(areas);
        figures.addAll(chargeStations);
        figures.addAll(walls);
        return figures;
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
