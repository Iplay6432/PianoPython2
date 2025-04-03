import javax.swing.JFrame;

public class Main {
   private static int screen;

   public static void main(String[] args) {
      Args s = new Screen();
      screen = Integer.parseInt(s.parseArg(args));

      if (screen == 1) {
         JFrame f = new JFrame("PianoPython, 2");
         f.setExtendedState(JFrame.MAXIMIZED_BOTH);
         f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         f.setUndecorated(true);
         f.setVisible(true);
         MainPanel main = new MainPanel(f.getSize());
         f.setContentPane(main);
         main.requestFocus();
         f.setVisible(true);
      }
   }
}