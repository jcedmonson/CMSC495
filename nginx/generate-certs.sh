#!/usr/bin/env zsh

CERTS_DIR=./certs
rm -rf $CERTS_DIR
mkdir $CERTS_DIR

openssl req -x509 -newkey rsa:2048 -keyout $CERTS_DIR/keytmp.pem -out $CERTS_DIR/cert.pem -days 365
openssl rsa -in $CERTS_DIR/keytmp.pem -out $CERTS_DIR/key.pem
