import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class AESDecryption {

    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            System.err.println("Usage: java AESDecryption <base64_encoded_string> <aes_key_file> <output_file>");
            System.exit(1);
        }

        String base64EncodedString = args[0];
        String aesKeyFile = args[1];
        String outputFile = args[2];

        // Split the input string into IV and encrypted content
        String[] parts = base64EncodedString.split("\\.");
        if (parts.length != 2) {
            throw new IllegalArgumentException("Invalid input string format.");
        }

        String ivBase64 = parts[0];
        String encryptedContentBase64 = parts[1];

        // Decode the IV and encrypted content
        byte[] iv = Base64.getUrlDecoder().decode(ivBase64);
        byte[] encryptedContent = Base64.getUrlDecoder().decode(encryptedContentBase64);

        // Read the AES key from the file and decode it
        String aesKeyBase64 = new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(aesKeyFile)));
        byte[] aesKey = Base64.getDecoder().decode(aesKeyBase64);

        // Ensure IV and AES key lengths are correct
        if (iv.length != 16) {
            throw new IllegalArgumentException("IV length is incorrect. Expected 16 bytes, got " + iv.length + " bytes.");
        }
        if (aesKey.length != 32) {
            throw new IllegalArgumentException("AES key length is incorrect. Expected 32 bytes, got " + aesKey.length + " bytes.");
        }

        // Perform the decryption
        byte[] decryptedContent = decrypt(encryptedContent, aesKey, iv);

        // Write the decrypted content to the output file
        java.nio.file.Files.write(java.nio.file.Paths.get(outputFile), decryptedContent);

        System.out.println("Decryption complete. Decoded content saved to " + outputFile);
    }

    public static byte[] decrypt(byte[] encryptedContent, byte[] key, byte[] iv) throws Exception {
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        SecretKeySpec keySpec = new SecretKeySpec(key, "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(iv);
        cipher.init(Cipher.DECRYPT_MODE, keySpec, ivSpec);
        return cipher.doFinal(encryptedContent);
    }
}
