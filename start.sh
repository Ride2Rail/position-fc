#!/bin/bash
app="position-fc"
docker build -t ${app} .
docker run -d -p 5007:5007 \
  --name=${app} \
  -v $PWD:/app ${app}
