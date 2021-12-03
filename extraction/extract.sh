#!/bin/sh

echo "+++++ Begin to extract information.+++++++++++++++++++++++++"
echo "Max txt file id: $1";

pwd
cd ./extraction
python ./extract_email.py $1
python ./extract_phone.py $1
#python ./extract_names.py
#python ./get_location.py
cd ..
pwd
echo "+++++ End to extract information.+++++++++++++++++++++++++"