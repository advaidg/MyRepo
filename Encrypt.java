import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import javax.crypto.Cipher;
import javax.crypto.CipherOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.*;
import java.security.cert.CertificateException;
import java.util.Base64;

@SpringBootApplication
public class MainApplication {

    private static final String KEYSTORE_FILE = "keystore.jks";
    private static final String KEYSTORE_ALIAS = "mykey";
    private static final String KEYSTORE_PASSWORD = "mypassword";
    private static final String PUBLIC_KEY_FILE = "public_key.pem";

    public static void main(String[] args) throws Exception {
        Security.addProvider(new BouncyCastleProvider());
        SpringApplication.run(MainApplication.class, args);

        // Load public key from file
        PublicKey publicKey = loadPublicKeyFromFile(PUBLIC_KEY_FILE);

        // Load public key to keystore
        KeyStore keyStore = loadKeystore();
        keyStore.setCertificateEntry(KEYSTORE_ALIAS, publicKey);
        saveKeystore(keyStore);

        // Encrypt file using public key
        encryptFile(publicKey, new File("file_to_encrypt.gz"), new File("encrypted_file.gz"));
    }

    private static PublicKey loadPublicKeyFromFile(String filename) throws Exception {
        byte[] keyBytes = readAllBytes(filename);
        String keyString = new String(keyBytes);
        keyString = keyString.replaceAll("\\n", "").replace("-----BEGIN PUBLIC KEY-----", "")
                .replace("-----END PUBLIC KEY-----", "");
        byte[] decoded = Base64.getDecoder().decode(keyString);
        return KeyFactory.getInstance("RSA").generatePublic(new X509EncodedKeySpec(decoded));
    }

    private static KeyStore loadKeystore() throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        File file = new File(KEYSTORE_FILE);
        KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
        if (file.exists()) {
            keyStore.load(new FileInputStream(file), KEYSTORE_PASSWORD.toCharArray());
        } else {
            keyStore.load(null, null);
            saveKeystore(keyStore);
        }
        return keyStore;
    }

    private static void saveKeystore(KeyStore keyStore) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        File file = new File(KEYSTORE_FILE);
        keyStore.store(new FileOutputStream(file), KEYSTORE_PASSWORD.toCharArray());
    }

    private static void encryptFile(PublicKey publicKey, File inputFile, File outputFile) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding", "BC");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);

        try (FileInputStream inputStream = new FileInputStream(inputFile);
             GzipCompressorInputStream gzipInputStream = new GzipCompressorInputStream(inputStream);
             CipherOutputStream cipherOutputStream = new CipherOutputStream(new FileOutputStream(outputFile), cipher)) {

            byte[] buffer = new byte[8192];
            int len;
            while ((len = gzipInputStream.read(buffer)) != -1) {
                cipherOutputStream.write(buffer, 0, len);
            }
        }
    }

    private static byte[] readAllBytes(String filename) throws IOException {
        File file = new File(filename);
        byte[] bytes = new byte[(int) file.length()];
        try (FileInputStream inputStream = new FileInputStream(file)) {
            inputStream.read(bytes);
        }
        return bytes;
    }
}
