#!/bin/bash

rm -rf app.db db_repository
sudo service apache2 restart
./db_create.py
