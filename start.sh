#! /bin/bash

raspivid -o - -t 0 -n -w 1280 -h 720 -fps 25 | testRaspi