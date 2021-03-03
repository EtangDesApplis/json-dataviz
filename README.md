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

