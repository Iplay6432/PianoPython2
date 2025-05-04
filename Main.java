import javax.swing.JFrame;

public class Main {
   private static int screen = 0;
   private static String state;

   public static void main(String[] args) {
      Server server = new Server();
      server.start();
      if (screen == 0) {
         JFrame f = new JFrame("PianoPython, 2");
         f.setExtendedState(JFrame.MAXIMIZED_BOTH);
         f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         f.setUndecorated(true);
         f.setVisible(true);
         MainPanel main = new MainPanel(f.getSize());
         f.setContentPane(main);
         main.requestFocus();
         f.setVisible(true);
         while (true) {
            state = main.getState();
            while (true) {
               if (state.equals("1")) {
                  server.close();
                  System.exit(0);
               }
               if (state.equals("0,0")) {
                  f.setVisible(false);
                  server.startPython();
                  break;
               }
               state = main.getState();
            }
            while (true) {
               if (state.equals("1")) {
                  server.close();
                  System.exit(0);
               }
               if (server.startJava()) {
                  f.setVisible(true);
                  main.setState("0");
                  main.start();
                  break;
               }
            }
         }

      }
   }
}