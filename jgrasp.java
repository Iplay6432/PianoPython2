import java.io.*;
import java.awt.Desktop;

public class jgrasp {
    public static void main(String[] args) {
        try {
            ProcessBuilder pb1 = new ProcessBuilder("java", "-jar", "Main.jar");
            Process p1 = pb1.start();
            Desktop d = Desktop.getDesktop();
            d.open(new File("PianoPythonApp.exe"));
            ProcessBuilder pb2 = new ProcessBuilder("start", "PianoPythonApp.exe");
            pb2.directory(new File(""));

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}