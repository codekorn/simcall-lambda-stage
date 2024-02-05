import json
import psycopg2
from datetime import datetime, date
import os

host_env = os.environ['stage_db']

conn = psycopg2.connect(
    host=host_env,
    database="simcall_main",
    user="jupyter",
    password="9akKB%(f0Y)8zUY6F=u=)l£Mh]")
cur = conn.cursor()


def lambda_handler(event, context):
    query = """Select gl.line_id, l.sim_number, l.phone_number,
                  g.autopay, g.next_payment,
                  case when g.manager_id = l.id then 1 end
                  is_manager,
                  g.max_lines - count(*) over() open_lines
                from groups g
                join group_lines gl
                       on g.id = gl.group_id
                join lines l
                      on l.id = gl.line_id
                where g.id = %s
                order by group_line"""
    cur.execute(query, (1,))
    raw_data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    data_json = {str(i): {columns[j]: raw_data[i][j] for j in range(len(columns))} for i in range(len(raw_data))}
    return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(data_json, cls=DateTimeEncoder, indent=4 )
}



class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
