import json
import psycopg2
from datetime import datetime, date

conn = psycopg2.connect(
    host="stage-database.c2gt8sxyfb4d.us-east-1.rds.amazonaws.com",
    database="simcall_main",
    user="jupyter",
    password="9akKB%(f0Y)8zUY6F=u=)l£Mh]")
cur = conn.cursor()


def lambda_handler(event, context):
    cur.execute('select * from lines limit 2')
    raw_data = cur.fetchall()
    d={i :{desc[0]: data for desc,data in zip(cur.description, raw_data[i])} for i in range(len(raw_data))}
    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(d, cls=DateTimeEncoder, indent=4 )
}



class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
