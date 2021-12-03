#!/bin/sh

echo "Max txt file id: $1";

echo "***** Begin to preprocess data.*************************"
pwd
./extraction/extract.sh $1

echo "-------- Begin to output data.-------------------"
pwd
python ./write_file_names.py
rm -rf ./FacultyDataset-idx/*
echo "-------- End to output data.-------------------"

echo "***** End to preprocess data.*************************"