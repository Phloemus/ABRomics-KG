FROM openjdk:19-jdk-alpine3.16

RUN apk update && \
    apk add tar

# Get the fuseki tools
RUN wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.2.0.tar.gz
RUN tar -xf apache-jena-fuseki-5.2.0.tar.gz
RUN mv apache-jena-fuseki-5.2.0 fuseki

WORKDIR /fuseki

EXPOSE 3030

## Launch the fuseki server
CMD ["./fuseki-server", "--file=/rdf/samples.ttl", "--file=/rdf/genes.ttl", "--file=/rdf/observations.ttl", "--file=/rdf/platforms.ttl", "--file=/rdf/strains.ttl", "--file=/rdf/observableProperties.ttl", "--file=/rdf/people.ttl", "--file=/rdf/procedures.ttl", "--file=/rdf/sensors.ttl", "/abromics-kg"]
