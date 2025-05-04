
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
    private String state = "0";
    private int stage = 0;

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

    public void start() {
        t.start();
        stage = 0;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    private class main implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (stage == 0) {
                start.setPos(pos);
                start.draw();
                repaint();
            }
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
            if (stage == 0) {
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
                    pos = start.getPos();
                    if (pos == 0) {
                        try {
                            state = "0," + start.getPos();
                            t.stop();
                        } catch (Exception m) {
                            System.out.println(m);
                        }
                    } else if (pos == 2) {
                        t.stop();
                        state = "0," + start.getPos();
                    }
                }
            }
            if (e.getKeyCode() == 27) {
                if (stage == 0)
                    state = "1";
                else
                    stage = 0;
            }
        }

        public void keyReleased(KeyEvent e) {
            if (stage == 0) {
                if (e.getKeyCode() == 38 && !up) {
                    up = true;
                }
                if (e.getKeyCode() == 40 && !down) {
                    down = true;
                }
            }
        }
    }

    public void paintComponent(Graphics g) {
        g.drawImage(myImage, 0, 0, (int) size.getWidth(), (int) size.getHeight(), null);
    }
}