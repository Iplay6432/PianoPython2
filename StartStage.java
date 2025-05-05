import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;

public class StartStage {

    private Graphics m;
    private Dimension size;
    private int NUMBER_OF_OPTIONS = 3 - 1;

    private int BOX_HEIGHT;
    private int BOX_WIDTH;
    private int BOX_X;
    private int BOX_Y;
    private int BOX_ARC;

    private int ARROW_HEIGHT;
    private int ARROW_WIDTH;
    private int POSTION_1_X;
    private int POSTION_1_Y;
    private int SPACE_BETWEEN_POSITIONS;
    private int SPACE_BETWEEN_POSITIONS_ARROW;
    private int pos;
    private int FONT_WIDTH;
    private int FONT_SIZE;
    private int ARROW_ARC;
    private Image image;
    private String[] options = new String[NUMBER_OF_OPTIONS + 1];

    public StartStage(Dimension size, Graphics m, int pos) {
        this.m = m;
        this.size = size;
        this.pos = pos;
        setVals();
        int aspectRatio = (int) (size.getWidth() / size.getHeight());
        try {
            if (aspectRatio == (int) (4 / 3)) {
                image = ImageIO.read(new File("img/4x3.png"));
            } else if (aspectRatio == (int) (16 / 9)) {
                image = ImageIO.read(new File("img/16x9.png"));
            } else if (aspectRatio == (int) (16 / 10)) {
                image = ImageIO.read(new File("img/16x10.png"));
            } else {
                image = ImageIO.read(new File("img/16x10.png"));
            }
        } catch (IOException e) {
            System.out.println(e);
        }

    }

    private void setVals() {
        BOX_HEIGHT = (int) (size.getHeight() / 2);
        BOX_WIDTH = (int) (size.getWidth() / 2);
        BOX_X = BOX_WIDTH - (BOX_WIDTH / 2);
        BOX_Y = BOX_HEIGHT - (BOX_HEIGHT / 2);
        BOX_ARC = (int) (size.getHeight() / 30);

        ARROW_HEIGHT = (int) (size.getHeight() / 10);
        ARROW_WIDTH = (int) (size.getWidth() / 20);
        ARROW_ARC = (int) (BOX_ARC / 10);
        POSTION_1_X = BOX_X - ARROW_WIDTH - (int) (size.getHeight() / 30);
        POSTION_1_X = (int) (size.getWidth() / 2);
        POSTION_1_Y = BOX_Y + (int) (size.getHeight() / 30);

        SPACE_BETWEEN_POSITIONS = (int) ((BOX_HEIGHT - 2 * (POSTION_1_Y - BOX_Y)) / (NUMBER_OF_OPTIONS));
        SPACE_BETWEEN_POSITIONS_ARROW = SPACE_BETWEEN_POSITIONS - ARROW_HEIGHT / 2;
        FONT_WIDTH = ARROW_WIDTH;
        FONT_SIZE = (int) (96.0 * FONT_WIDTH / Toolkit.getDefaultToolkit().getScreenResolution());

        options[0] = "Levels";
        options[1] = "Freeplay";
        options[2] = "Settings";
    }

    public void draw() {
        m.setColor(Color.WHITE);

        m.fillRect(0, 0, (int) size.getWidth(), (int) size.getHeight());
        m.drawImage(image, 0, 0, (int) size.getWidth(), (int) size.getHeight(), null);
        // Graphics2D g2 = (Graphics2D) m;
        // g2.drawRoundRect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, BOX_ARC, BOX_ARC);
        m.setColor(Color.BLUE.brighter());
        m.setFont(new Font("New Times Roman", Font.BOLD, FONT_SIZE));
        FontMetrics fm = m.getFontMetrics();
        drawArrow(pos, fm);
        drawText(fm.getHeight(), fm);
    }

    public int getPos() {
        return pos;
    }

    public void setPos(int p) {
        pos = p;
    }

    private void drawText(int height, FontMetrics fm) {
        int i = 0;
        Graphics2D g2 = (Graphics2D) m;
        g2.setColor(new Color(137, 89, 217));
        for (int y = POSTION_1_Y + height; y < POSTION_1_Y + height
                + SPACE_BETWEEN_POSITIONS * NUMBER_OF_OPTIONS; y += SPACE_BETWEEN_POSITIONS_ARROW) {
            int width = fm.stringWidth(options[i]);
            g2.drawString(options[i], POSTION_1_X - (width / 2), y);
            i += 1;
        }
    }

    private void drawArrow(int pos, FontMetrics fm) {
        m.setColor(new Color(137, 89, 217));
        int width = fm.stringWidth(options[pos]);
        int x = POSTION_1_X - width;
        int[] xs = { x, x, x + ARROW_WIDTH }; // draw it based on the center
        int[] ys = { POSTION_1_Y + SPACE_BETWEEN_POSITIONS_ARROW * pos,
                POSTION_1_Y + SPACE_BETWEEN_POSITIONS_ARROW * pos + ARROW_HEIGHT,
                POSTION_1_Y + SPACE_BETWEEN_POSITIONS_ARROW * pos + ARROW_HEIGHT / 2 };
        RoundPolygon.fillRoundPolygon(m, new Polygon(xs, ys, 3), ARROW_ARC);

    }
}
