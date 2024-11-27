
## Using alpine but may require a open jdk or java in some capacity (so the initial image have too be changed potentially)
FROM alpine:3.14

RUN apk add tar
RUN wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.2.0.tar.gz

## Unpack
RUN tar -xf apache-jena-fuseki-5.2.0.tar.gz

## Mount the volume for the ttl files
VOLUME rdf /rdf

##! Also check if some port have to be exposed for this to work 

## Launch the fuseki server
##! concatenate the ttl files or find a way to add all the content of all the files in the fuseki graph
CMD ["fuseki-server", "--file=/rdf/samples.ttl", "/abromics-kg"]
