import java.io.*;
import java.net.*;
import java.lang.Thread;

public class Server extends Thread {
    private Socket s = null;
    private ServerSocket ss = null;
    private DataInputStream in = null;
    private DataOutputStream out = null;

    private static int port = 12345;

    public void startPython() {
        try {
            out.writeUTF("0");
            out.flush();
        } catch (IOException i) {
            System.out.println(i);
        }
    }

    public void startPythonFreeplay() {
        try {
            out.writeUTF("1");
            out.flush();
        } catch (IOException e) {
            System.out.print(e);
        }
    }

    public void close() {
        try {
            out.writeUTF("2");
            out.flush();
        } catch (IOException i) {
            System.out.print(i);
        }
    }

    public boolean startJava() {
        try {
            String m = in.readUTF();
            if (m.equals("0")) {
                return true;
            } else {
                return false;
            }
        } catch (IOException i) {
            System.out.println(i);
            return false;
        }
    }

    public void run() {
        try {
            ss = new ServerSocket(port);
            s = ss.accept();
            System.out.println("connected");
            in = new DataInputStream(s.getInputStream());
            out = new DataOutputStream(s.getOutputStream());
        } catch (IOException i) {
            System.out.println(i);
        }
    }
}
