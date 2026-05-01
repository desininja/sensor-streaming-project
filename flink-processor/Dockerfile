# Stage 1: Build the Jar
FROM maven:3.8.5-openjdk-11 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package

# Stage 2: Run the Jar
FROM flink:1.18.0
WORKDIR /app
COPY --from=build /app/target/flink-processor-1.0-SNAPSHOT.jar ./app.jar
# Submit the job to the local Flink cluster
CMD ["flink", "run", "app.jar"]