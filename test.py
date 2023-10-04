import os
import adal
import struct
import pyodbc
import pandas as pd

def connect_oauth():
  tenant_id = '72f988bf-86f1-41af-91ab-2d7cd011db47'
  clientId = '35ddfcdd-48a7-4978-9be4-27ab1eb52b6b'
  clientSecret = 'uwQ8Q~CwGz4Tu2SGvclcyMesphIoo-OCuuxXnbH2'
  server = 'azsqlv3.sql.azuresynapse.net'
  database = 'azsqldw'
  print(tenant_id,clientId,clientSecret,server,database)
  
  authorityHostUrl = "https://login.microsoftonline.com"
  authority_url = authorityHostUrl + "/" + tenant_id
  context = adal.AuthenticationContext(authority_url,   api_version=None)
  token = context.acquire_token_with_client_credentials("https://database.windows.net/", clientId, clientSecret)
  print(token)
  driver = "{ODBC Driver 17 for SQL Server}"
  conn_str = "DRIVER=" + driver + ";server=" + server + ";database="+ database + ";Authentication=ActiveDirectoryServicePrincipal"
  print(conn_str)
  SQL_COPT_SS_ACCESS_TOKEN = 1256
  tokenb = bytes(token["accessToken"], "UTF-8")
  print(tokenb)
  exptoken = b''
  for i in tokenb:
    exptoken += bytes({i})
    exptoken += bytes(1)
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken
    print(tokenstruct)
    db_engine = pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN:tokenstruct})
  return db_engine

if __name__ == "__main__":
   engine=connect_oauth()
   print(engine)
