FROM openjdk:19-jdk-alpine3.16

RUN apk update && \
    apk add tar curl

# Get the fuseki tools
RUN curl -o apache-jena-fuseki-5.4.0.tar.gz https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.4.0.tar.gz
RUN tar -xf apache-jena-fuseki-5.4.0.tar.gz
RUN mv apache-jena-fuseki-5.4.0 fuseki

## Trying to use geosparql with fuseki
#RUN curl https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-geosparql/5.2.0/jena-fuseki-geosparql-5.2.0.jar --output jena-fuseki-geosparql-5.2.0.jar
#RUN mkdir fuseki
#RUN mv jena-fuseki-geosparql-5.2.0.jar fuseki

WORKDIR /fuseki

EXPOSE 3030

## Launch the fuseki server
CMD ["./fuseki-server", "--file=/rdf/samples.ttl", "--file=/rdf/genes.ttl", "--file=/rdf/observations.ttl", "--file=/rdf/platforms.ttl", "--file=/rdf/strains.ttl", "--file=/rdf/observableProperties.ttl", "--file=/rdf/people.ttl", "--file=/rdf/procedures.ttl", "--file=/rdf/sensors.ttl", "/abromics-kg"]

## Test geosparql
# CMD ["java", "-jar", "jena-fuseki-geosparql-5.2.0.jar", "-rf", "/rdf/samples.ttl", "-rf", "/rdf/genes.ttl", "-rf", "/rdf/observations.ttl", "-rf", "/rdf/platforms.ttl", "-rf", "/rdf/strains.ttl", "-rf", "/rdf/observableProperties.ttl", "-rf", "/rdf/people.ttl", "-rf", "/rdf/procedures.ttl", "-rf", "/rdf/sensors.ttl", "-rf", "/rdf/geosparql-test.rdf", "/abromics-kg"]
