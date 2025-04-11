import java.io.*;

public class Python {
    public static void run(int screen) throws Exception {
        ProcessBuilder pb = new ProcessBuilder("python", "Main.py", "-s " + screen);
        System.out.println(pb.command());
        pb.redirectErrorStream(true);
        Process p = pb.start();
    }
}
