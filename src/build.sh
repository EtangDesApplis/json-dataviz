#usage: sh build.sh [version]
cd api
docker build -t etangdesapplis/json-dataviz-api:$1 .
docker push etangdesapplis/json-dataviz-api:$1
cd ../
cd front
docker build -t etangdesapplis/json-dataviz:$1 .
docker push etangdesapplis/json-dataviz:$1