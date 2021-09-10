# from pyhive import hive
# conn = hive.Connection(host="localhost", port=10001, username="hiveuser", auth='NOSASL')

# cursor = conn.cursor()
# cursor.execute("describe employee;")
# for result in cursor.fetchall():
#   use_result(result)



# from impala.dbapi import connect

# conn = connect(host='127.0.0.1', port=10000, user='hiveuser', password='hivepassword', auth_mechanism='NOSASL')
# cursor = conn.cursor()
# cursor.execute('show tables')
# results = cursor.fetchall()
# print(results)
# from pyhive import hive

# hive.connect('localhost', configuration={'hive.server2.thrift.sasl.qop': 'auth-conf'})

# from pyhive import hive
# conn = hive.Connection(host='127.0.0.1', port=10000, auth='NOSASL')
# import pandas as pd
# import sys
# df = pd.read_sql("SELECT * FROM my_table", conn)
# print(sys.getsizeof(df))
# df.head()




# import contextlib
# from pyhive.hive import connect

# def get_conn():
#     return connect(
#         host='127.0.0.1',
#         port=10000,
#         auth='NOSASL',
#         username='hiveuser'
#     )

# with contextlib.closing(get_conn()) as conn, \
#         contextlib.closing(conn.cursor()) as cur:
#     cur.execute('My long insert statement')

# import pyhs2

# with pyhs2.connect(host='127.0.0.1',
#                     port=10000,
#                     authMechanism="KERBEROS")as conn:

# 	with conn.cursor()as cur:
# 		print(cur.getDatabases())

# import jaydebeapi
# conn = jaydebeapi.connect("org.apache.hive.jdbc.HiveDriver",
#        "jdbc:hive2://127.0.0.1:10001/default;transportMode=http;ssl=false;httpPath=/hive2",
#        ["username", "password"],
#        "hive-jdbc-2.3.7.jar")


# import pyhs2
# import logging

# try:
#     hive_con =  pyhs2.connect(
#         host='', # Hive server2 IP or host
#         port=10000,
#         authMechanism="NOSASL",
#         user='', # Username
#         password='', #User password,
#         database='default')
#     hive_cur = hive_con.cursor()
#     table_body  = '(`Id` BIGINT, `some_field_1` STRING, `some_field_2` STRING ) '
#     db_name = "my_db"
#     table_name = "my_first_parquete_table"
#     table_format = ("PARQUET", "TEXTFILE", "AVRO",)

#     # Creating internal Parquet table
#     create_tb = ('CREATE TABLE IF NOT EXISTS `%s`.`%s` %s STORED AS %s') % (db_name, tb_name, table_body, table_format[0])
#     hive_cur.execute(create_tb)

#     # Creating internal Textfile table
#     create_tb = ('CREATE TABLE IF NOT EXISTS `%s`.`%s` %s STORED AS %s') % (db_name, tb_name, table_body, table_format[1])
#     hive_cur.execute(create_tb)
#     hive_cur.close()
#     hive_con.close()
# except Exception as e:
#     logging.error(str(e))