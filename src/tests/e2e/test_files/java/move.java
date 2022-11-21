package logo;

import classes.EV3MovePilot;
import java.lang.Runnable;

public class Logo {
    public static void main(String[] args) {
        EV3MovePilot robot = new EV3MovePilot(5.6, 11.7);
        Logo logo = new Logo();
        double temp1 = 2.0;
        robot.travel(temp1);
        double temp2 = 4.0;
        double temp3 = -temp2;
        robot.rotate(-temp3);
        double temp4 = 6.5;
        robot.travel(-temp4);
        double temp5 = 8.23;
        double temp6 = -temp5;
        robot.rotate(temp6);
    }
}