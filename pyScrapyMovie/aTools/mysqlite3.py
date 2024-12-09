import sqlite3
from pathlib import Path

tableModle = {
    'id': {'tip': '唯一id值'},
    'carno': {'tip': '番号'},
    'title': {'tip': '标题'},
    'actor': {'tip': '女优'},
    'release': {'tip': '发布时间'},
    'desc': {'tip': '描述'},
    'thumb': {'tip': '海报链接'},
    'website': {'tip': '网址'},
    'filename': {'tip': '唯一id值'},
    'type': {'tip': 'av类型'},
    'tags': {'tip': '标签'},
    'maker': {'tip': '厂商'},
    'series': {'tip': '系列'},
}

keys_tuple = tuple(tableModle.keys())
unknown_tuple = ('?',) * len(keys_tuple)


# 把 json 的数据按 keys_tuple 顺序 获取 元祖（插入数据需要元祖格式）
def parserData(jsondata):
    result_tuple = []
    for key in keys_tuple:
        value = ''
        if key in jsondata:
            value = jsondata[key]
        result_tuple.append(value)
    result_tuple = tuple(result_tuple)
    return result_tuple


class MyDBOption:
    def __init__(self, db_link):
        self.link = db_link
        self.conn = ''

    def connect_to_database(self):
        curr_path = Path(__file__)
        relative_path = Path(self.link)
        db_path = (curr_path.parent / relative_path).resolve()
        print(db_path)
        self.conn = sqlite3.connect(db_path)

    def close_to_database(self):
        self.conn.close()

    def insert_data(self, jsonData):
        cursor = self.conn.cursor()
        data = parserData(jsonData)

        keys = ", ".join(keys_tuple)
        unknowns = ", ".join(unknown_tuple)
        exec_sql = f"INSERT OR IGNORE  INTO master ({keys}) VALUES ({unknowns})"
        print(exec_sql)
        print(data)
        cursor.execute(exec_sql, data)
        self.conn.commit()

        # 判断受影响的行数，如果为0则可能是因为id重复导致插入被忽略
        rows_affected = cursor.rowcount
        if rows_affected == 0:
            message = "插入失败，该id已存在，请更换id后重新尝试。"
        else:
            message = "数据插入成功"
        print(id, '：', message)

        cursor.close()
        # return cursor.lastrowid

# E:\桌面\pyForAVHub\pyScrapyMovie\assets
# E:\桌面\pyForAVHub\pyScrapyMovie\aTools\assets\avhub.db

myDBOption = MyDBOption('../assets/avhub.db')


def batch_insert_data(conn, data_list):
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO your_table (column1, column2,...) VALUES (?,?,...)", data_list)
    conn.commit()

def check_id_exists(conn, id_value):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table WHERE id=?", (id_value,))
    return cursor.fetchone() is not None

def get_id_info(conn, id_value):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table WHERE id=?", (id_value,))
    return cursor.fetchone()

def update_data(conn, id_value, new_data):
    cursor = conn.cursor()
    cursor.execute("UPDATE your_table SET column1=?, column2=?,... WHERE id=?", (*new_data, id_value))
    conn.commit()

def delete_data(conn, id_value):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM your_table WHERE id=?", (id_value,))
    conn.commit()