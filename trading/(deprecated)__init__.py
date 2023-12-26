import influxdb_client, os, time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "stocker"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


bucket="stock_transactions"

def add_transaction(dbid, share, exchange, price, status):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(dbid)
        .tag("Share", share)
        .field("qty", exchange)
        .field("price", price)
        .field("status", status)
    )
    write_api.write(bucket=bucket, org="stocker", record=point)


def read_transactions(dbid):

    query_api = client.query_api()

    query = """from(bucket: "stock_transactions")
    |> range(start: 2019-08-28T22:00:00Z)
    |> filter(fn: (r) => r._measurement == "1")"""
    tables = query_api.query(query, org="stocker")

    print("Printing Time | Share | Qty | Price | Status")
    time_series = []
    data = {}
    for i in range(len(tables[0].records)):
        data['time'] = tables[0].records[i].values['_time'].strftime("%Y-%m-%d %H:%M:%S")
        data['share'] = tables[0].records[i].values['Share']
        data['qty'] = tables[0].records[i].values['_value']
        data['price'] = tables[1].records[i].values['_value']
        data['status'] = tables[2].records[i].values['_value']
        time_series.append(data)
        pass
    print(time_series)
# add_transaction('1', 'AAPL', 100, 100, 'success')
# read_transactions('1')
# for table in tables:
#   for record in table.records:
    # print(record)
    # print(record.values['_time'], record.values['Share'])
    # pass
#   break
# print(tables[0].records)



# query_api = write_client.query_api()

# query = """from(bucket: "bucket1")
#   |> range(start: -10m)
#   |> filter(fn: (r) => r._measurement == "measurement1")
#   |> mean()"""
# tables = query_api.query(query, org="stocker")

# for table in tables:
#     for record in table.records:
#         print(record)




# Deleting api
# start = "2009-01-02T23:00:00Z"
# stop = "2023-11-22T23:00:00Z"
# client.delete_api().delete(start=start, stop=stop, bucket=bucket, org="stocker", predicate="_measurement=\"1\"")