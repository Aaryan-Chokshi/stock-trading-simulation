import influxdb_client, os, time
from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# token = os.environ.get("INFLUXDB_TOKEN")
# token = "YQBJ31AtVzFf8YOBKdQWSp62Sl4RwM-QLWrAIMjsD79g4S6LHsAnTcChhH8PZMrGp5I6dW8vi-UWDZIlmS49eA=="
token = "yzLYLV6K8ffWPElz2R68E4EhlMv7f2vOvnQ1fb4N-5rEaq36wWmEXEA6-ggZgb277TDgn6sWhND56iQrRrq__w=="
org = "stocker"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# YQBJ31AtVzFf8YOBKdQWSp62Sl4RwM-QLWrAIMjsD79g4S6LHsAnTcChhH8PZMrGp5I6dW8vi-UWDZIlmS49eA==
bucket="stock_transactions"
# bucket = "transactions_history"

def add_transaction(dbid, share, qty, price, status):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point('transactions')
        .tag("dbid", dbid)
        .field("Share", share)
        .field(field="qty", value=str(qty))
        .field(field="price", value=str(price))
        .field(field="status", value=status)
    )
    print(point)
    write_api.write(bucket=bucket, org="stocker", record=point)
    pass


def read_transactions(dbid):

    query_api = client.query_api()

    query = f"""from(bucket: "{bucket}")
    |> range(start: 2019-08-28T22:00:00Z)
    |> filter(fn: (r) => r._measurement == "transactions" and r.dbid == "{dbid}")"""
    tables = query_api.query(query, org="stocker")

    # print(tables)
    if(len(tables) == 0):
        return []
    time_series = []
    for i in range(len(tables[0].records)):
        data = {}
        data['time'] = tables[0].records[i].values['_time'].strftime("%Y-%m-%d %H:%M:%S")
        data['share'] = tables[0].records[i].values['_value']
        data['price'] = tables[1].records[i].values['_value']
        data['qty'] = tables[2].records[i].values['_value']
        data['status'] = tables[3].records[i].values['_value']
        time_series.append(data)
        pass
    return time_series

# print(read_transactions("45"))
# add_transaction("45", "AAPL", 10, 100, "success")


# start = "2009-01-02T23:00:00Z"
# stop = "2024-11-30T23:00:00Z"
# client.delete_api().delete(start=start, stop=stop, bucket=bucket, org="stocker", predicate="_measurement=\"transactions\"")

