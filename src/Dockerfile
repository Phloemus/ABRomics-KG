FROM python:3.12-slim

# RUN apk add --no-cache python3 py3-pip py3-virtualenv
RUN mkdir src

COPY app.py src
COPY data src/data

WORKDIR /src

RUN python3 -m venv .venv
RUN . .venv/bin/activate # . is the same as source
RUN pip install pyarrow
RUN pip install streamlit
RUN pip install rdflib

CMD ["streamlit", "run", "app.py"]

