import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;

public class Screen extends Args {
    @Parameter(names = "--screen", description = "what to start on", required = true)
    private String screen;

    public String parseArg(String[] args) {
        Screen jArgs = new Screen();
        JCommander.newBuilder().addObject(jArgs).build().parse(args);

        return jArgs.screen;
    }
}
