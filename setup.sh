#!/bin/bash 

{ 
    python setup.py build
    python setup.py install 
} &> /dev/null

hackip