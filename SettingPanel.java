import javax.swing.*;
import settings.*;
import java.awt.*;
import java.io.File;
import java.awt.event.FocusListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class SettingPanel extends JPanel {
    private int numOfSettings = 8;
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
        setLayout(new GridLayout(numOfSettings + 1, 1));
        int FONT_WIDTH = (int) (d.getHeight() / 30);
        int FONT_SIZE = (int) (96.0 * FONT_WIDTH / Toolkit.getDefaultToolkit().getScreenResolution());
        int[] set = new int[numOfSettings];
        try {
            File f = new File("settings.txt");
            Scanner s = new Scanner(f);
            int i = 0;
            while (s.hasNextLine()) {
                set[i] = (int) ((Double.parseDouble(s.nextLine())) * 100.0);
                i += 1;
            }
        } catch (IOException e) {
            System.out.println(e);
        }
        settings[0] = new FallingVolume((int) d.getWidth(), (int) d.getHeight(), set[0]);
        settings[1] = new UserVolume((int) d.getWidth(), (int) d.getHeight(), set[1]);
        JLabel s = new JLabel("Settings", SwingConstants.CENTER);
        s.setFont(new Font("Times New Roman", Font.BOLD, FONT_SIZE));
        add(s);
        for (Setting i : settings) {
            if (i != null)
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
                int save = JOptionPane.showConfirmDialog(null, "Do you want to save changes?", "Setings",
                        JOptionPane.YES_NO_OPTION);
                if (save == JOptionPane.YES_OPTION) {
                    try {
                        FileWriter f = new FileWriter("settings.txt");
                        for (Setting i : settings)
                            if (i != null)
                                f.write(i.getData() + "\n");
                        f.close();
                        state = 1;
                    } catch (IOException n) {
                        System.out.println(n);
                        state = 1;
                    }
                } else {
                    state = 1;
                }
            }
        }
    }
}
