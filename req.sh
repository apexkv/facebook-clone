#!/bin/bash

pip freeze > requirements.txt

rm ./users/requirements.txt
rm ./posts/requirements.txt
rm ./likes/requirements.txt
rm ./comments/requirements.txt

cp ./requirements.txt ./users/requirements.txt
cp ./requirements.txt ./posts/requirements.txt
cp ./requirements.txt ./likes/requirements.txt
cp ./requirements.txt ./comments/requirements.txt

rm ./requirements.txt