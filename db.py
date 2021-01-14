import sqlite3
conn = sqlite3.connect(":memory:")
c = conn.cursor()

table="projects"
columns = ["title", "dev", "tools", "link", "repo", "progress"]
def init():
    # I didn't know what to call the santize string for SQL commands,
    # so it's columnsSQL. :( sorry if tha'ts cringe 
    columnsSQL=''.join(map(lambda i:i+" text, ", columns[0:-1]))
    columnsSQL=(columnsSQL+columns[-1]+" text")
        
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table}  ({columnsSQL})""")
    conn.commit()

def insertentry(entry)->None:
    values= ', '.join(list(map(lambda i: "'"+ i.replace("'", "''")+"'", entry.values())))
    columnsSQL = ', '.join(list(entry.keys()))
    execme = f"INSERT INTO {table} ({columnsSQL}) VALUES (%s)" % (values,)
    c.execute(f"INSERT INTO {table} ({columnsSQL}) VALUES (%s)" % (values,))
    conn.commit()

def getall():
    c.execute(f"SELECT * from {table}")
    data= c.fetchall()
    makeentry = lambda entry: {columns[i] : entry[i] for i in range(0, len(entry))}
    return list(map(makeentry, data))

