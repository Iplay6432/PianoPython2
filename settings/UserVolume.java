package settings;

import java.io.FileWriter;
import java.io.IOException;

import javax.swing.*;
import java.awt.*;

public class UserVolume extends Setting<Double> {
    private JPanel p;
    private JSlider slider;
    private JLabel label;

    public UserVolume(int width, int height, int val) {
        super();
        int FONT_WIDTH = height / 30;
        int FONT_SIZE = (int) (96.0 * FONT_WIDTH / Toolkit.getDefaultToolkit().getScreenResolution());
        p = new JPanel();
        p.setLayout(new GridLayout(2, 1));

        label = new JLabel("This is the volume of notes that you play", SwingConstants.CENTER);
        label.setFont(new Font("Times New Roman", Font.BOLD, FONT_SIZE));

        slider = new JSlider(0, 100, 100);
        slider.setValue(val);
        p.add(label);
        p.add(slider);
        p.setBorder(BorderFactory.createEmptyBorder(height / 50, width / 50, height / 50, width / 50));
    }

    public Double getData() {
        return slider.getValue() / 100.0;
    }

    public void saveData() {
        try {
            FileWriter f = new FileWriter("settings.txt");
            f.append("1*" + (slider.getValue() / 100.0));
            f.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public JPanel getPanel() {
        return p;
    }
}
