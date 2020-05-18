#! /bin/sh

touch log.txt        # create log file if not exist already

. /var/www/html/hosted/gaze-detection/venv/bin/activate
python /var/www/html/hosted/gaze-detection/gaze_detection/app.py > log.txt
