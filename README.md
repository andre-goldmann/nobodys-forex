./kcadm.sh update realms/master -s sslRequired=NONE --server http://localhost:8080 --realm master --user username

# Create Key-Pair/Keystore
keytool -genkeypair -alias jdg.digital -keyalg RSA -keysize 2048 -storetype PKCS12 -keystore jdg.digital.p12 -validity 3650

# List certificates
keytool -list -v -keystore jdg.digital.p12

# Export ssl_certificate
keytool -exportcert -alias jdg.digital -keystore jdg.digital.p12 -file jdg.digital.crt

# Export ssl_certificate_key
openssl pkcs12 -in jdg.digital.p12 -nocerts -nodes -out jdg.digital.pem

# Enter docker container
docker exec -it <container_name_or_id> bash

# Import Certs into Keystore
https://github.com/craig-rueda/tomcat-native-spring-boot-sample

openssl req -x509 -newkey rsa:4096 -keyout jdg.digital.key -out jdg.digital.crt -days 365
openssl pkcs12 -export -out jdg.digital.p12 -inkey jdg.digital.key -in jdg.digital.crt

keytool -importkeystore -deststorepass password -destkeypass password -destkeystore keystore.jks -srckeystore keyStore.p12 -srcstoretype PKCS12 -srcstorepass password -alias 1

