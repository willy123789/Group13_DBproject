import oracledb

connection = oracledb.connect(
    user="GROUP13",
    password="fXDJskHxL2",
    dsn=oracledb.makedsn("140.117.69.60", 1521, service_name='ORCLPDB1')
)




'''import sqlite3

connection = sqlite3.connect('ebookstore.db', check_same_thread = False)
cursor = connection.cursor()'''