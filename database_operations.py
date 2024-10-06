import sqlite3 as sql

connection=sql.connect('test06-21.db')

cursor=connection.cursor()

tbname = '' # actual user database
tb2name = '' # for notification counter 
tb3name = '' #for options menu

def checktable():
    global tbname
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;",(tbname,))
    result = cursor.fetchone()
    # print(result)
    if(result == None):
        cursor.execute(f"""CREATE TABLE {tbname}(
                   Label string,
                   Date string,
                   Time string,
                   DocDate string,
                   TimeLeft string
                   )
                    """)
    connection.commit()

def checktable2():
    global tb2name
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;",(tb2name,))
    result = cursor.fetchone()
    # print(result)
    if(result == None):
        cursor.execute(f"""CREATE TABLE {tb2name}(
                   notified string,
                   Label string,
                   Date string,
                   Time string
                   )
                    """)
    connection.commit()

def checktable3():
    global tb3name
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;",(tb3name,))
    result = cursor.fetchone()
    # print(result)
    if(result == None):
        cursor.execute(f"""CREATE TABLE {tb3name}(
                   theme string,
                   widgettheme string,
                   notifdura string,
                   firsttime string,
                   frame_home string
                   )
                    """)
    connection.commit()

def tablename(tablenames):
    global tbname
    tbname=tablenames
    checktable()

def table2name(tablenames):
    global tb2name
    tb2name=tablenames
    checktable2()

def table3name(tablenames):
    global tb3name
    tb3name=tablenames
    checktable3()

def add_one(label,date,time,docdate,timeleft='COUNTDOWN NOT VISIBLE'): 
    cursor.execute(f"INSERT INTO {tbname} VALUES(?,?,?,?,?)",(label,date,time,docdate,timeleft))
    connection.commit()

def add_one2(notified,label,date,time): 
    cursor.execute(f"INSERT INTO {tb2name} VALUES(?,?,?,?)",(notified,label,date,time))
    connection.commit()

def add_one3(theme,widgettheme,notifdura,language,frame_home): 
    cursor.execute(f"INSERT INTO {tb3name} VALUES(?,?,?,?,?)",(theme,widgettheme,notifdura,language,frame_home))
    connection.commit()

def query_all():
    cursor.execute(f"SELECT rowid,* FROM {tbname}")
    results=cursor.fetchall()
    return results

def query_all2():
    cursor.execute(f"SELECT rowid,* FROM {tb2name}")
    results=cursor.fetchall()
    return results

def query_all3():
    cursor.execute(f"SELECT rowid,* FROM {tb3name}")
    results=cursor.fetchall()
    return results

def query_indexed():
    cursor.execute(f"SELECT rowid FROM {tbname}")
    results=cursor.fetchall()
    return results

def query_limited(limit):
    cursor.execute(f"SELECT rowid,* FROM {tbname} LIMIT {str(limit)}")
    results=cursor.fetchall()
    return results
    
def query_specific(attribute,value):
    cursor.execute(f"SELECT rowid,* FROM {tbname} WHERE {attribute} = ?",(value,))
    results=cursor.fetchall()
    return results

def update_table(attribute2,value,attribute,new_value):
    if attribute2 == 'ID':
        attribute2 = 'rowid'
    cursor.execute(f"UPDATE {tbname} SET {attribute} = ? WHERE rowid = ?",(new_value,value,))
    connection.commit()

def update_table2(attribute2,value,attribute,new_value):
    if attribute2 == 'ID':
        attribute2 = 'rowid'
    cursor.execute(f"UPDATE {tb2name} SET {attribute} = ? WHERE {attribute2} = ?",(new_value,value,))
    connection.commit()

def update_table3(attribute,value):
    cursor.execute(f"UPDATE {tb3name} SET {attribute} = ? WHERE rowid = 1",(value,))
    connection.commit()

def delete(attribute,value):
    cursor.execute(f"DELETE FROM {tbname} WHERE {attribute} = ?",(value,))
    connection.commit()

def delete2(attribute,value):
    cursor.execute(f'''DELETE FROM {tb2name} WHERE {attribute} = ?''',(value,))
    connection.commit()

def delete3(value):
    cursor.execute(f'''DELETE FROM {tb3name} WHERE rowid = ?''',(value,))
    connection.commit()

def entry_validator(attribute,value): #checks whether an entry exists or not
    val2check = value
    query = (f'SELECT 1 FROM {tbname} WHERE {attribute} = ? LIMIT 1')
    cursor.execute(query,(val2check,))
    result = cursor.fetchone()
    return result

tablename('reminders3')
table2name('notificationz3')
table3name('optionsmenu3')

result = query_all3()
if len(result) == 0:
    add_one3('solar','info','10000','Yes','Keep')

# res = query_all2()
# for r in res:
#     print(r)
# print('---------------------------------')

# bes = query_all()
# for i in bes:
#     print(i)
#     print('-------------------------------------------------------------------------------------------------')

# bes = query_all2()
# for i in bes:
#     print(i)
#     print('-------------------------------------------------------------------------------------------------')

