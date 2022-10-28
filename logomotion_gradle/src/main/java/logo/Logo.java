package logo;
import classes.EV3MovePilot;
public class Logo {
    public static void main(String[] args) {
        EV3MovePilot robot = new EV3MovePilot(5.6, 11.7);
        double temp1 = 100.0;
        robot.travel(temp1);
    }
}