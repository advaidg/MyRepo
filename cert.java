    private PrivateKey loadPrivateKey(String keyFilePath) throws Exception {
        File keyFile = new File(keyFilePath);
        byte[] keyBytes = new byte[(int) keyFile.length()];
        try (FileInputStream fis = new FileInputStream(keyFile)) {
            fis.read(keyBytes);
        }

        String privateKeyPEM = new String(keyBytes)
                .replace("-----BEGIN PRIVATE KEY-----", "")
                .replace("-----END PRIVATE KEY-----", "")
                .replaceAll("\\s", "");

        byte[] decoded = Base64.getDecoder().decode(privateKeyPEM);
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(decoded);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return keyFactory.generatePrivate(keySpec);
    }

    private PublicKey loadPublicKeyFromCert(String certFilePath) throws Exception {
        File certFile = new File(certFilePath);
        try (FileInputStream fis = new FileInputStream(certFile)) {
            CertificateFactory certificateFactory = CertificateFactory.getInstance("X.509");
            X509Certificate certificate = (X509Certificate) certificateFactory.generateCertificate(fis);
            return certificate.getPublicKey();
        }
    }
