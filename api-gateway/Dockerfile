FROM maven:latest AS builder

# Set the working directory
WORKDIR /app

# Copy the Maven project file
COPY pom.xml .
COPY spotbugs-security-exclude.xml .
COPY spotbugs-security-include.xml .

# Copy the source code
COPY src ./src
COPY interface ./interface


# Build the application with Maven
RUN mvn clean install -DskipTests

# Use a base image with OpenJDK
FROM eclipse-temurin:21

# Set the working directory in the container
WORKDIR /app

# Create a non-root user for running the application
RUN adduser --disabled-password --gecos '' springuser
USER springuser

# Set JAVA_HOME environment variable
#ENV JAVA_HOME /opt/java/openjdk

COPY certs/certificate.pem .

#RUN update-ca-certificates

# Import the CA certificate(s) into the Java truststore
#RUN keytool -import -alias jdg.digital -keystore -cacerts -storepass Blade1708 -file /usr/local/share/ca-certificates/certificate.pem -noprompt

RUN keytool -import -alias jdg.digital -keystore $JAVA_HOME/lib/security/cacerts -file certificate.pem -noprompt -storepass Blade1708

COPY --from=builder /app/target/api-gateway-0.0.1-SNAPSHOT.jar .

# Expose the port that the application runs on
EXPOSE 9080

# Define the command to run the application when the container starts
CMD ["java", "-jar", "-Dspring.profiles.active=prod", "api-gateway-0.0.1-SNAPSHOT.jar"]