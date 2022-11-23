package logo;

import classes.EV3MovePilot;
import java.lang.Runnable;

public class Logo {

    public static void main(String[] args) {
        EV3MovePilot robot = new EV3MovePilot(5.6, 11.7);
        Logo logo = new Logo();
        double temp1 = 5.123;
        var var2 = temp1;

        double temp3 = 20.6;
        double temp4 = -temp3;
        var var5 = temp4;

        double temp6 = 1.0;
        var var7 = temp6;

        double temp8 = var2 + var5;
        var var9 = temp8;

        double temp10 = var5 - var7;
        var var11 = temp10;

        double temp12 = var2 * var7;
        var var13 = temp12;

        double temp14 = var5 / var2;
        var var15 = temp14;
    }
}