package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.view.CanvasViewer;

public class SimulatorApplication {
    public static void main(String[] args) {
        // Créer un modèle d'usine
        Factory usine = new Factory("Usine de Robots",100,75);

        /*
        // Ajouter des machines de production aux aires de travail
        ProductionMachine machine1 = new ProductionMachine("Machine 1", 5, 5, 2.0, 2.0);
        ProductionMachine machine2 = new ProductionMachine("Machine 2", 6, 6, 3.0, 3.0);
        ProductionMachine machine3 = new ProductionMachine("Machine 3", 7, 7, 4.0, 4.0);
		*/

        // Ajouter des salles à l'usine
        usine.addRoom("Packaging Room", 5, 15, 30.0, 30.0);
        usine.addRoom("Stock Room", 5, 40, 25.0, 50.0);
        usine.addRoom("Delivery Room", 55, 40, 25.0, 20.0);
        usine.addRoom("Sorting Room", 35, 35, 30.0, 40.0);
        
        // Ajouter des aires de travail à chaque salle
        usine.addArea("Packaging Area (AP)", 7, 20, 10.0, 5.0);
        usine.addArea("Sorting Area (AS)", 40, 6, 4.0, 4.0);
        usine.addArea("Stock Delivery Area (ASD)", 52, 35, 3.0, 3.0);
        usine.addArea("Stock (ST)", 51, 35, 4.0, 5.0);
        
        // Ajouter une station de recharge à l'usine
        usine.addStation("Station de Recharge", 3, 3, 5.0, 5.0);
        
        // Créer les murs
        usine.createWalls();
        
        // Ajouter des robots à l'usine
        usine.addRobot("RoboCop", 6, 6, 3.0, 4.0, 5.5);
        usine.addRobot("Terminator", 16, 38, 3.0, 4.0, 7.0);
        usine.addRobot("Wall-E", 40, 50, 3.0, 4.0, 3.5);

        // Créer l'interface graphique avec CanvasViewer
        CanvasViewer viewer = new CanvasViewer(usine);

        // Afficher l'interface graphique
        viewer.setVisible(true);
    }
}

