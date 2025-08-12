#!/bin/bash

# Check if the file path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <file-containing-sparql-query>"
  echo "[options]:      -o <output-file> : replace the content of a file with the query result"
  echo "                -h <host>        : direct the request to a certain sparql endpoint"
  exit 1
fi

# Read the SPARQL query from the file
SPARQL_QUERY=$(<"$1")

## Change the host if needed
HOST="http://localhost:8081/sparql"
if [ "$2" == "-h" ]; then
    HOST=$3
fi

if [ "$4" == "-h" ]; then
    HOST=$5
fi

# Case a file is provided
if [ "$2" == "-o" ]; then
  # Check if the file path is provided after the -o flag
  if [ -z "$3" ]; then
    echo "Usage: $0 <file-containing-sparql-query>"
    echo "[options]:      -o <output-file> : replace the content of a file with the query result"
    exit 1
  fi

  # Send the query to the Virtuoso SPARQL endpoint
  RESPONSE=$(curl -s --data-urlencode "query=$SPARQL_QUERY" \
                -H "Accept: application/sparql-results+json" \
                $HOST)
  
  # Check if the response is not empty
  if [ -z "$RESPONSE" ]; then
    echo "No response received from the SPARQL endpoint."
    exit 1
  fi
  
  # Get the file path from the second argument
  FILE_PATH=$3
  
  # Write the response to the file indicated
  echo "$RESPONSE" > "$FILE_PATH"
else
  # Case no file is provided (display directly on the console)

  # Send the query to the Virtuoso SPARQL endpoint
  RESPONSE=$(curl -s --data-urlencode "query=$SPARQL_QUERY" \
                -H "Accept: text/tab-separated-values" \
                $HOST)
  
  # Check if the response is not empty
  if [ -z "$RESPONSE" ]; then
    echo "No response received from the SPARQL endpoint."
    exit 1
  fi

  # Format the result to be readable in the terminal
  echo -e "\n--- Query Result ---\n"
  echo "$RESPONSE" | column -t -s $'\t'
  echo -e "\n--- End of Result ---\n"
fi


