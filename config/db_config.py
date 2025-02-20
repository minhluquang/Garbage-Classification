import MySQLdb as mdb

def connect_db():
  try:
    conn = mdb.connect(
      host="localhost",
      user="root",
      password="",
      database="python-db"
    )
    return conn
  except mdb.Error as e:
    print(f"Lỗi kết nối MySQL: {e}")
    return None
