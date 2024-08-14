import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Enumeration;

public class ClasspathDebugger {

    public static void main(String[] args) {
        try {
            printClasspathResources();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void printClasspathResources() throws IOException {
        ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
        Enumeration<URL> resources = classLoader.getResources("");

        while (resources.hasMoreElements()) {
            URL resource = resources.nextElement();
            File dir = new File(resource.getFile());
            if (dir.isDirectory()) {
                printDirectoryContents(dir, "");
            } else {
                System.out.println(dir.getAbsolutePath());
            }
        }
    }

    private static void printDirectoryContents(File dir, String indent) {
        File[] files = dir.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    System.out.println(indent + "[DIR] " + file.getName());
                    printDirectoryContents(file, indent + "  ");
                } else {
                    System.out.println(indent + "[FILE] " + file.getName());
                }
            }
        }
    }
}
