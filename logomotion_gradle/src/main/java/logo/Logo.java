package logo;

import lejos.hardware.motor.Motor;
import lejos.robotics.chassis.Chassis;
import lejos.robotics.chassis.Wheel;
import lejos.robotics.chassis.WheeledChassis;
import lejos.robotics.navigation.MovePilot;

public class Logo {
    // Generate Java here
    public static void main(String[] args) {
        Wheel wheel1 = WheeledChassis.modelWheel(Motor.A, 43.2).offset(-72);
        Wheel wheel2 = WheeledChassis.modelWheel(Motor.D, 43.2).offset(72);
        Chassis chassis = new WheeledChassis(new Wheel[]{wheel1, wheel2},WheeledChassis.TYPE_DIFFERENTIAL); 
        MovePilot robot = new MovePilot(chassis);
        robot.setLinearSpeed(30);  // cm per second
        robot.travel(50);         // cm
        robot.rotate(-90);        // degree clockwise
        robot.travel(-50,true);  //  move backward for 50 cm
        while(robot.isMoving())Thread.yield();
        robot.rotate(-90);
        robot.stop();
    }
}
