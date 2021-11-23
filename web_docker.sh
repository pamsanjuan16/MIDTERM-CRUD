#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp test2.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" > tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile

echo "COPY  ./static /home/devasc/MidtermProject_G12/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/devasc/MidtermProject_G12/templates/" >> tempdir/Dockerfile
echo "COPY  test2.py /home/devasc/MidtermProject_G12/" >> tempdir/Dockerfile

echo "EXPOSE 8080" >> tempdir/Dockerfile

echo "CMD python3 /home/devasc/MidtermProject_G12/test2.py" >> tempdir/Dockerfile

cd tempdir
docker build -t test2 .

docker run -t -d -p 8080:8080 --name webrun test2

docker ps -a
