FROM maven:3.8.4-openjdk-17 AS builder

# Set the working directory
WORKDIR /app

# Copy the Maven project file
COPY pom.xml .
COPY spotbugs-security-exclude.xml .
COPY spotbugs-security-include.xml .

# Copy the source code
COPY src ./src

# Build the application with Maven
RUN mvn clean install -DskipTests -Pprod

# Use a base image with OpenJDK
FROM eclipse-temurin:17.0.10_7-jre-alpine

# Set the working directory in the container
WORKDIR /app

COPY certs/certificate.pem /usr/local/share/ca-certificates/

RUN update-ca-certificates

# Import the CA certificate(s) into the Java truststore
RUN keytool -importcert -alias jdg.digital -keystore -cacerts -storepass Blade1708 -file /usr/local/share/ca-certificates/certificate.pem -noprompt

COPY --from=builder /app/target/forex-frontend-vaadin-0.0.1-SNAPSHOT.jar .

# Expose the port that the application runs on
EXPOSE 7080

# Define the command to run the application when the container starts
CMD ["java", "-jar", "-Dspring.profiles.active=prod", "forex-frontend-vaadin-0.0.1-SNAPSHOT.jar"]