./kcadm.sh update realms/master -s sslRequired=NONE --server http://localhost:8080 --realm master --user username

# Create Key-Pair/Keystore
keytool -genkeypair -alias jdg.digital -keyalg RSA -keysize 2048 -storetype PKCS12 -keystore jdg.digital.p12 -validity 3650
keytool -importkeystore -srckeystore jdg.digital.p12 -destkeystore intermediate.p12 -deststoretype PKCS12
openssl pkcs12 -in intermediate.p12 -out certificate.pem -nokeys
openssl pkcs12 -in intermediate.p12 -out private.key -nocerts

# List certificates
keytool -list -v -keystore jdg.digital.p12

# Need always/sometimes
sudo service docker start