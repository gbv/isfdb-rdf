#!/usr/bin/env python3

import re
import json
import mysql.connector

# read configuration file
config={
    "host":'localhost'
}
with open("config.sh", "r") as file:
    for m in [re.match('([a-zA-Z_0-9]+)\s*=\s*"(.*)"', line) for line in file]:
        if m:
            config[m.group(1)]=m.group(2)

mydb = mysql.connector.connect(**{key:config[key] for key in ['host','user','password','db']})
cursor = mydb.cursor(dictionary=True)

def reduce(data):
    if isinstance(data, dict):
        data = {key: reduce(value) for key, value in data.items()}
        data = {key: value for key, value in data.items() if value != None}
        return data if data else None
    elif isinstance(data, list):
        data = [reduce(value) for value in data]
        data = [value for value in data if value != None]
        return data if data else None
    else:
        return data

cursor.execute("""
SELECT p.pub_id, p.pub_title, p.pub_isbn, CAST(p.pub_year AS CHAR) AS date, p.pub_pages, p.pub_ptype, p.publisher_id, u.publisher_name 
FROM pubs p
LEFT JOIN publishers u ON (p.publisher_id IS NULL) OR (p.publisher_id=u.publisher_id )
LIMIT 10
""")

for p in cursor:
    publisher_id = p["publisher_id"]

    date = None
    if p["date"]:
        date=p["date"].replace("-00","")

    pub = {
        "@context" : "http://lobid.org/resources/context.jsonld",
        "id": f'{config["pub_ns"]}{p["pub_id"]}',
        "title": p["pub_title"],
        "isbn": [ p["pub_isbn"] ],
        "publication": {
            "startDate": date,
            "type": [ "PublicationEvent"],
            "publishedBy": [ p["publisher_name"] ]
        } if date or p["publisher_name"] else None,
        "extent": p["pub_pages"],
        "type": ["BibliographicResource"],
        "contribution": []
    }

    if publisher_id:
        pub["contribution"].append({
            "agent": {
                "id": f'{config["publisher_ns"]}{p["publisher_id"]}',
                "label": p["publisher_name"],
                 "type": [ "CorporateBody" ],
            },
            "role": {
              "id" : "http://id.loc.gov/vocabulary/relators/pbl",
              "label": "Publisher"
            },
            "type": [ "Contribution" ]
        })

    # TODO: pub_price
    # TODO: note_id
    # TODO: pub_ptype 'ANTHOLOGY','CHAPBOOK','COLLECTION','MAGAZINE','NONFICTION','NOVEL','OMNIBUS','FANZINE'
    # TODO: pub_series_id, pub_series_num, catalog_id
    # TODO: pub_ctype - Type of the publication

    print(json.dumps(reduce(pub), indent=2))
