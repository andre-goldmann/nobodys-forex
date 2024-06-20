FROM maven:latest AS builder

# Set the working directory
WORKDIR /app

# Copy the Maven project file
COPY pom.xml .
COPY spotbugs-security-exclude.xml .
COPY spotbugs-security-include.xml .
COPY forex-domain-0.0.1-SNAPSHOT.jar .

# Copy the source code
COPY src ./src


# Build the application with Maven
RUN mvn install:install-file -Dfile=forex-domain-0.0.1-SNAPSHOT.jar -DgroupId=jdg.digital -Dversion=0.0.1-SNAPSHOT -Dpackaging=jar
RUN mvn clean install -DskipTests

# Use a base image with OpenJDK
FROM eclipse-temurin:21

# Set the working directory in the container
WORKDIR /app

COPY certificate.pem .
# TODO remove this
RUN keytool -import -alias jdg.digital -keystore $JAVA_HOME/lib/security/cacerts -file certificate.pem -noprompt -storepass Blade1708

COPY --from=builder /app/target/api-gateway-0.0.1-SNAPSHOT.jar .

# Expose the port that the application runs on
EXPOSE 9080

# Define the command to run the application when the container starts
CMD ["java", "-jar", "-Dspring.profiles.active=prod", "api-gateway-0.0.1-SNAPSHOT.jar"]