./kcadm.sh update realms/master -s sslRequired=NONE --server http://localhost:8080 --realm master --user username

# Create Key-Pair/Keystore
keytool -genkeypair -alias jdg.digital -keyalg RSA -keysize 2048 -storetype PKCS12 -keystore jdg.digital.p12 -validity 3650
keytool -importkeystore -srckeystore jdg.digital.p12 -destkeystore intermediate.p12 -deststoretype PKCS12
openssl pkcs12 -in intermediate.p12 -out certificate.pem -nokeys
openssl pkcs12 -in intermediate.p12 -out private.key -nocerts
# TODO here
keytool -importcert -file jdg.digital.p12 -alias jdg.digital -keystore $JDK_HOME/jre/lib/security/cacerts

# List certificates
keytool -list -v -keystore jdg.digital.p12

# Need always/sometimes
sudo service docker start
docker exec -it <container_name_or_id> /bin/bash

# Update Prod
apt-get update && sudo apt-get upgrade && sudo apt-get autoremove
nano api-gateway/src/main/resources/application-prod.yml
nano forex-backend-java/src/main/resources/application-prod.yml
nano keycloak.dev.env

apt-get update && apt-get upgrade && apt-get autoremove
cd development/nobodys-forex/
docker compose down
docker compose up --build -d

# to check when out of space
C:\Users\username\AppData\Local\Packages

#Nmap-Scans
* sudo nmap -sT IP
* sudo nmap -sT IP
* sudo nmap -sS IP
* sudo nmap -O IP
* sudo nmap -A IP
* sudo nmap --script vuln IP

Docker disc usage:
* docker system df 

17:10 23.04.2024

|TYPE           |TOTAL    |ACTIVE   |SIZE     |RECLAIMABLE    |
  |---------------|---------|---------|---------|---------------|
|Images         |5        |0        |1.281GB  |1.281GB (100%) |
|Containers     |0        |0        |0B       |0B             |
|Local Volumes  |0        |0        |0B       |0B             |
|Build Cache    |49       |0        |438.7MB  |438.7MB        |

TODO:
https://confluence.atlassian.com/kb/how-to-import-a-public-ssl-certificate-into-a-jvm-867025849.html

Read:
https://confluence.atlassian.com/kb/connecting-to-ssl-services-802171215.html
https://confluence.atlassian.com/kb/unable-to-connect-to-ssl-services-due-to-pkix-path-building-failed-error-779355358.html