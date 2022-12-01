#!/bin/sh
echo "Check if Python 3.x version is available and PyMongo is installed..."

if [[ "$(python -V)" =~ "Python 3" ]] || [[ "$(python3 -V)" =~ "Python 3" ]] && python -c "import pymongo" &> /dev/null ; then

    echo "Launching the Python/Demo.py"
    python Python/demo.py

else

    echo "Is not possible to launche the demo."

fi