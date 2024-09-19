#!/bin/sh

if [ -z "${PRODUCER_PORT}" ]; then
    export PRODUCER_PORT=5005
fi


export FLASK_APP=app

flask run -p $PRODUCER_PORT

