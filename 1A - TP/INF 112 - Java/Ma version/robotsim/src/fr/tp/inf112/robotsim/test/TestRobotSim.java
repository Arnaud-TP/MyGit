package fr.tp.inf112.robotsim.test;

import fr.tp.inf112.robotsim.model.Factory;
import fr.tp.inf112.robotsim.model.Robot;

public class TestRobotSim {
	
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Robot myRobot = new Robot("Robot 1", 5);
		System.out.println(myRobot);
		myRobot.setSpeed(10);
		System.out.println("New speed : "+myRobot.getSpeed());
		Factory factory1 = new Factory("factory1");
		factory1.addRobot("Robot1");
		factory1.addRobot("Robot2");
		factory1.printToConsole();
	}
}
