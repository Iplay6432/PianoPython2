
//Name______________________________ Date_____________
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;
import java.io.File;
import java.io.IOException;

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
        try {
            File f = new File("played");
            if (f.createNewFile()) {
                JOptionPane.showMessageDialog(null, "Controls:\r\n" + //
                        "\r\n" + //
                        "Navigate with arrow keys and Enter\r\n" +
                        "- Escape → go back / exit (on title screen)\r\n" + //
                        "- Keys s-k → play in current octave, white notes\r\n" + //
                        "- Keys e, r, y, u, i →; play in current octave, black notes\r\n" + //
                        "- Keys z-m →; play octave below if not at lowest octave, if it is play octave up, white notes\r\n"
                        + //
                        "- Keys 2-6 →; play octave below if not at lowest octave, if it is play octave up, black notes\r\n"
                        + //
                        "- Space →; move up 1 octave\r\n" + //
                        "- Left Alt →; move down 1 octave ");
            }
        } catch (IOException t) {
            System.out.println(t);
        }

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