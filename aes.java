import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.KeyStore;
import java.util.Base64;

public class KeyExtractor {
    public static void main(String[] args) throws Exception {
        if (args.length != 5) {
            System.err.println("Usage: java KeyExtractor <keystore-file> <keystore-password> <alias> <alias-password> <output-file>");
            System.exit(1);
        }

        String keystoreFile = args[0];
        String keystorePassword = args[1];
        String alias = args[2];
        String aliasPassword = args[3];
        String outputFile = args[4];

        KeyStore keystore = KeyStore.getInstance("JKS");
        FileInputStream inputStream = new FileInputStream(keystoreFile);
        keystore.load(inputStream, keystorePassword.toCharArray());

        SecretKey key = (SecretKey) keystore.getKey(alias, aliasPassword.toCharArray());
        byte[] encoded = key.getEncoded();
        String base64Key = Base64.getEncoder().encodeToString(encoded);

        try (FileOutputStream outputStream = new FileOutputStream(outputFile)) {
            outputStream.write(base64Key.getBytes());
        }

        System.out.println("Key extracted and saved to " + outputFile);
    }
}
