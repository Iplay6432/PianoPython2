
//Name______________________________ Date_____________
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

public class MainPanel extends JPanel {
    private int pos = 0;
    private int MAX_POS = 3 - 1;
    private Dimension size;
    private Timer t;
    private BufferedImage myImage;
    private Graphics m;
    private StartStage start;

    public MainPanel(Dimension size) {
        addKeyListener(new Key());
        setFocusable(true);
        this.size = size;
        myImage = new BufferedImage((int) size.getWidth(), (int) size.getHeight(), BufferedImage.TYPE_INT_RGB);
        m = myImage.getGraphics();
        start = new StartStage(size, m, pos);

        t = new Timer(5, new main());
        t.start();
    }

    private class main implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            start.setPos(pos);
            start.draw();
            repaint();
        }
    }

    private class Key extends KeyAdapter {
        boolean up;
        boolean down;

        public Key() {
            up = true;
            down = true;
        }

        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == 38 && up) {
                if (pos > 0)
                    pos -= 1;
                up = false;
            }
            if (e.getKeyCode() == 40 && down) {
                if (pos < MAX_POS)
                    pos += 1;
                down = false;
            }
            if (e.getKeyCode() == 10) {
                System.out.println("WOW!");
            }
        }

        public void keyReleased(KeyEvent e) {
            if (e.getKeyCode() == 38 && !up) {
                up = true;
            }
            if (e.getKeyCode() == 40 && !down) {
                down = true;
            }
        }
    }

    public void paintComponent(Graphics g) {
        g.drawImage(myImage, 0, 0, (int) size.getWidth(), (int) size.getHeight(), null);
    }
}