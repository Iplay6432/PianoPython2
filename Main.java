import javax.swing.JFrame;

public class Main {
   private static int screen = 0;
   private static String state;
   private static int stage = 0;
   private static boolean pass = false;

   public static void main(String[] args) {
      Server server = new Server();
      server.start();
      if (screen == 0) {
         JFrame f = new JFrame("PianoPython, 2");
         f.setExtendedState(JFrame.MAXIMIZED_BOTH);
         f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         f.setUndecorated(true);
         f.setVisible(true);
         SettingPanel settings = new SettingPanel(f.getSize());
         MainPanel main = new MainPanel(f.getSize());
         f.setContentPane(main);
         main.requestFocus();
         f.setVisible(true);
         while (true) {
            state = main.getState();
            pass = false;
            stage = 0;
            main.start();
            while (true) {
               if (state.equals("1")) {
                  server.close();
                  System.exit(0);
               } else if (state.equals("0,0")) {
                  f.setVisible(false);
                  server.startPython();
                  break;
               } else if (state.equals("0,1")) {
                  f.setVisible(false);
                  server.startPythonFreeplay();
                  break;
               } else if (state.equals("0,2")) {
                  f.setVisible(false);
                  f.setContentPane(settings);
                  settings.requestFocus();
                  f.setVisible(true);
                  stage = 1;
                  break;
               }
               state = main.getState();
            }
            if (stage == 1) {
               pass = true;
               while (true) {
                  state = settings.getState();
                  if (state.equals("1")) {
                     stage = 0;
                     f.setVisible(false);
                     f.setContentPane(main);
                     main.requestFocus();
                     f.setVisible(true);
                     main.setState("0");
                     settings.setState("0");
                     break;
                  }
               }
            }
            if (stage == 0 && !pass) {
               while (true) {
                  state = main.getState();
                  if (state.equals("1")) {
                     server.close();
                     System.exit(0);
                  }
                  if (server.startJava()) {
                     f.setVisible(true);
                     main.requestFocus();
                     main.setState("0");
                     main.start();
                     break;
                  }
               }
            }
         }

      }
   }
}