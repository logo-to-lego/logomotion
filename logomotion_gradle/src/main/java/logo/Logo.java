package logo;

import classes.EV3MovePilot;

public class Logo {
    // Generate Java here
    public static void main(String[] args) {
        System.out.println("Initializing robot");
        EV3MovePilot robot = new EV3MovePilot(5.6, 11.7);
        System.out.println("Robot initialized");
        System.out.println("Moving");
        robot.setSpeed(500);
        robot.travel(100);
        robot.rotate(90);
        robot.travel(50);
        robot.rotate(-180);
        robot.travel(-50);
    }
}
