import javax.swing.*;
import settings.*;
import java.awt.*;
import java.awt.event.FocusListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.FileWriter;
import java.io.IOException;

public class SettingPanel extends JPanel {
    private int numOfSettings = 2;
    private int state = 0;
    private Setting[] settings = new Setting[numOfSettings];

    public String getState() {
        return "" + state;
    }

    public void setState(String s) {
        state = Integer.parseInt(s);
    }

    public SettingPanel(Dimension d) {
        addKeyListener(new Key());
        setFocusable(true);
        setLayout(new GridLayout(numOfSettings, 1));
        settings[0] = new FallingVolume((int) d.getWidth(), (int) d.getHeight());
        settings[1] = new UserVolume((int) d.getWidth(), (int) d.getHeight());
        for (Setting i : settings) {
            add(i.getPanel());
        }
        addFocusListener(new Focus());
    }

    private class Focus implements FocusListener {
        public void focusGained(java.awt.event.FocusEvent e) {
        }

        public void focusLost(java.awt.event.FocusEvent e) {
            requestFocus();
        }
    }

    private class Key extends KeyAdapter {
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == 27) {
                try {
                    FileWriter f = new FileWriter("settings.txt");
                    for (Setting i : settings)
                        f.write(i.getData() + "\n");
                    f.close();
                    state = 1;
                } catch (IOException n) {
                    System.out.println(n);
                    state = 1;
                }
            }
        }
    }
}
