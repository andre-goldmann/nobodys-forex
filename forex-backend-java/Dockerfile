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


COPY --from=builder /app/target/forex-backend-java-0.0.1-SNAPSHOT.jar .
# Copy the packaged JAR file into the container
#COPY target/forex-backend-java-0.0.1-SNAPSHOT.jar /app/forex-backend-java.jar

# Copy the application-prod.yml file into the container
#COPY src/main/resources/application-prod.yml /app/application-prod.yml

# Expose the port that the application runs on
EXPOSE 5080

# Define the command to run the application when the container starts
CMD ["java", "-jar", "-Dspring.profiles.active=prod", "forex-backend-java-0.0.1-SNAPSHOT.jar"]