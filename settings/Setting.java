package settings;

import javax.swing.*;

public abstract class Setting<T> extends JPanel {
    public abstract void saveData();

    public abstract T getData();

    public abstract JPanel getPanel();
}