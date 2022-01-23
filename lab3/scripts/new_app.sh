#! /bin/bash
project=$1
appname=$2
mkdir -p  ${project}/${appname}
touch ${project}/${appname}/models.py
touch ${project}/${appname}/schemas.py
touch ${project}/${appname}/crud.py
touch ${project}/${appname}/routers.py
