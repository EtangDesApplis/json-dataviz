# json-dataviz
flexiblly visualize json data using regex

Dash tutor: https://pbpython.com/plotly-dash-intro.html

Api to update data:
```
curl -POSTX localhost:5000/database/update/ json
```
database iss a single json, for example
```
{
    "cluster1": {
        "storage-zone-A": 30,
        "storage-zone-B": 10,
        "storage-total": 40,
        "vm": {
            "vm1": {
                "storage-zone-A":10,
                "storage-zone-B":0,
                "storage-total":10,
            },
            "vm2": {
                "storage-zone-A":20,
                "storage-zone-B":10,
                "storage-total":30,
            }
        }
    }
    "cluster2": {
        "storage-zone-A": 0,
        "storage-zone-B": 100,
        "storage-total": 100,
        "vm": {
            "vm3": {
                "storage-zone-A":0,
                "storage-zone-B":50,
                "storage-total":50,
            },
            "vm4": {
                "storage-zone-A":0,
                "storage-zone-B":45,
                "storage-total":45,
            },
            "vm5": {
                "storage-zone-A":0,
                "storage-zone-B":5,
                "storage-total":5,
            }
        }
    }
}
```
index: regex 'cluster*' to trace on clusterwide level, 'cluster1.vm.vm*' to have vm view of cluster 1,
'cluser*.vm.vm*' to have vm view over all clusters

pip install dash==0.18.3
pip install dash-renderer==0.10.0
pip install dash-html-components==0.7.0
pip install dash-core-components==0.12.6
pip install plotly --upgrade

Dash reference: https://dash.plotly.com/dash-core-components/input


## deployment with helm
helm install json-dataviz helm-chart --set filter='\w+'

helm install json-dataviz helm-chart --set front.tag=0.0.1-arm64 --set api.tag=0.0.1-arm64 --set filter='\w+' --set baseURL="localhost.com"

## CUSTOMIZATION

JSON_DATAVIZ_DATABASE_FILE : full path to database json file
JSON_DATAVIZ_REPORT_TITLE : name of dashboard
JSON_DATAVIZ_FILTER_HINTS : hints for some regex patterns (when filter is null string)
JSON_DATAVIZ_DEFAULT_FILTER : default filter
JSON_DATAVIZ_YAXIS_TITLE
JSON_DATAVIZ_XAXIS_TITLE

## update Database via api

curl https://localhost:5000/update -d '{"canada_poppulation":20,"france_population":100}' -H 'Content-Type: application/json'