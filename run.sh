#!/bin/bash
#
# continually_retry.sh
#

while true; do
    echo "Running westword.sh..."
    ./westword.py
    
    # Check the exit status of your_script.sh
    if [ $? -eq 0 ]; then
        echo "Script succeeded!"
        break
    else
        echo "Script failed. Retrying in 5 seconds..."
        sleep 5
    fi
done