package fr.tp.inf112.robotsim.model;

import fr.tp.inf112.projects.canvas.controller.CanvasViewerController;
import fr.tp.inf112.projects.canvas.controller.Observer;
import fr.tp.inf112.projects.canvas.model.Canvas;
import fr.tp.inf112.projects.canvas.model.CanvasPersistenceManager;



public class SimulateurController implements CanvasViewerController {

    private Factory factory;

    public SimulateurController(Factory factory) {
    	this.factory = factory;
    }
        

    public boolean addObserver(Observer observer) {
        return factory.addObserver(observer);
    }
         

    public boolean removeObserver(Observer observer) {
        return factory.removeObserver(observer);
    }

    public Canvas getCanvas() {
        return factory;
    }

    

    public CanvasPersistenceManager getPersistenceManager() {
        // Implémentez votre méthode pour retourner le gestionnaire de persistance
        return null;
    }

    public void startAnimation() {
    	while (factory.isSimulationStarted()) { factory.behave();
        try {
            Thread.sleep( 200 );
        }
        catch (InterruptedException ex) {
            ex.printStackTrace();
        }
    }
    }

    public void stopAnimation() {
        factory.stopSimulation();
        // Ajoutez votre logique pour arrêter l'animation
    }

    public boolean isAnimationRunning() {
        return factory.isSimulationStarted();
    }


	public void setCanvas(Canvas canvasModel) {
		
		
	}
}
