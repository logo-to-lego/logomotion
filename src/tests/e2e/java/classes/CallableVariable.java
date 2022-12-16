package classes;

import java.util.concurrent.Callable;

public class CallableVariable implements Variable {
    public Callable<Void> value;

    public CallableVariable(Callable<Void> value) {
        this.value = value;
    }
}
