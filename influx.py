#INFLUXDB
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv('.env')

__token = os.environ.get('INFLUXDB_TOKEN')
__org = os.environ.get('INFLUXDB_ORG')
__url = os.environ.get('INFLUXDB_URL')
__bucket = os.environ.get('INFLUXDB_BUCKET')
__write_client = influxdb_client.InfluxDBClient(url=__url, token=__token, org=__org)
__write_api = __write_client.write_api(write_options=SYNCHRONOUS)

def __export_2darray(data, host, pointi, name, value):
  print(host)
  for i in range(len(data[0])):
    point = (
      Point(pointi) 
      .tag('host', host)   
      .field(data[0][i], data[1][i])
    )
    print(name + str(data[0][i]) + value + str(data[1][i]))
    __write_api.write(bucket=__bucket, org=__org, record=point)

def export_temps(data, host):
  __export_2darray(data, host, 'temps', 'Name: ', ' Temp: ')

def export_watts(data, host):
  print(host)
  point = (
    Point('watts')
    .tag('host', host)
    .field('usage:', data)
  )
  print('Watts: ' + str(data))
  __write_api.write(bucket=__bucket, org=__org, record=point)

def export_fans(data, host):
  __export_2darray(data, host, 'fans', 'Fan Name: ', ' Speed: ')