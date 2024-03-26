# Use a base image with OpenJDK
FROM eclipse-temurin:17.0.10_7-jre-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the packaged JAR file into the container
COPY target/forex-backend-java-0.0.1-SNAPSHOT.jar /app/forex-backend-java.jar

# Copy the application-prod.yml file into the container
COPY src/main/resources/application-prod.yml /app/application-prod.yml

# Expose the port that the application runs on
EXPOSE 8080

# Define the command to run the application when the container starts
CMD ["java", "-jar", "forex-backend-java.jar", "--spring.profiles.active=prod"]