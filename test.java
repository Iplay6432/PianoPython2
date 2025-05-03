
import java.io.*;
import java.net.*;
import java.lang.Thread;

public class test {
    private static int port = 12345;

    private Socket s = null;
    private ServerSocket ss = null;
    private DataInputStream in = null;
    private DataOutputStream out = null;

    public test() throws InterruptedException {
        try {
            ss = new ServerSocket(port);
            s = ss.accept();
            System.out.println("connected");
            in = new DataInputStream(s.getInputStream());
            out = new DataOutputStream(s.getOutputStream());
            out.writeUTF("0");
            out.flush();
            String m = "";
            while (true) {
                m = in.readUTF();
                System.out.println("Client Says: " + m);

                Thread.sleep(1000);

                out.writeUTF("0");
                out.flush();
            }
            // System.out.println("close");
            // s.close();
            // out.close();
            // in.close();
        } catch (IOException i) {
            System.out.println(i);
            System.out.println(i);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        test s = new test();
    }
}