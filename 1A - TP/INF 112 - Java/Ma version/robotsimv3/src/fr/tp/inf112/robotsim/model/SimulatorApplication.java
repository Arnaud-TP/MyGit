package fr.tp.inf112.robotsim.model;

import java.util.ArrayList;
import fr.tp.inf112.projects.canvas.view.CanvasViewer;

public class SimulatorApplication {
    public static void main(String[] args) {
        // On crée le modèle de l'usine
        Factory usine = new Factory("Usine de Robots",100,75);

        /*
        // Ajouter des machines de production aux aires de travail
        ProductionMachine machine1 = new ProductionMachine("Machine 1", 5, 5, 2.0, 2.0);
        ProductionMachine machine2 = new ProductionMachine("Machine 2", 6, 6, 3.0, 3.0);
        ProductionMachine machine3 = new ProductionMachine("Machine 3", 7, 7, 4.0, 4.0);
		*/

        // On ajoute les salles
        usine.addRoom("Packaging Room", 5, 10, 30.0, 30.0);
        usine.addRoom("Stock Room", 5, 40, 25.0, 50.0);
        usine.addRoom("Delivery Room", 55, 40, 25.0, 20.0);
        usine.addRoom("Sorting Room", 35, 10, 30.0, 40.0);
        
        // On ajoute les aires
        usine.addArea("Packaging Area (AP)", 7, 20, 10.0, 5.0);
        usine.addArea("Sorting Area (AS)", 50, 25, 4.0, 4.0);
        usine.addArea("Stock Delivery Area (ASD)", 72, 40, 3.0, 3.0);
        usine.addArea("Stock (ST)", 5, 61, 4.0, 5.0);
        
        // On ajoute la sation de recharge
        usine.addStation("Station de Recharge", 50, 40, 5.0, 5.0);
        
        // On crée les murs
        usine.createWalls();
        
        // On ajoute les robots à l'usine
        usine.addRobot("RoboCop", 6, 6, 3.0, 4.0, 5.5);
        usine.addRobot("Terminator", 16, 38, 3.0, 4.0, 7.0);
        usine.addRobot("Wall-E", 40, 50, 3.0, 4.0, 3.5);

     // On récupère les robots et les composants à visiter
        Robot roboCop = usine.getRobot("RoboCop");
        Robot terminator = usine.getRobot("Terminator");
        Robot wallE = usine.getRobot("Wall-E");

        if (roboCop != null) {
        	ArrayList<Component> componentsToVisit;
        	componentsToVisit.add(packagingRoom)
            roboCop.setComponentsToVisit(ArrayList(packagingRoom, stockRoom, sortingRoom));
        }
        if (terminator != null) {
            terminator.setComponentsToVisit(ArraysList(stockRoom, sortingRoom, packagingRoom));
        }
        if (wallE != null) {
            wallE.setComponentsToVisit(ArraysList(sortingRoom, packagingRoom, stockRoom));
        }

        // On crée l'interface graphique avec CanvaViewer
        CanvasViewer viewer = new CanvasViewer(new CanvasViewerController(usine));

        // On affiche l'interface graphique
        viewer.setVisible(true);

        // On lance la simulation
        new Thread(() -> {
            usine.startSimulation();
            while (usine.isSimulationStarted()) {
                usine.behave();
                try {
                    Thread.sleep(200);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                }
            }
        }).start();
    
}

