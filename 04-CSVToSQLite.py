#!/usr/bin/env python
# coding: utf-8

# # References
# 
# ## UDACITY
# 
# 4. Data Wrangling With MongoDB
# 
# LESSON 5 DATA QUALITY
# 
# 8. Example Using our Blueprint
# 
# https://classroom.udacity.com/nanodegrees/nd002-airbus/parts/35305c70-58f5-4614-b7d6-302fa3f916a3/modules/2166796a-7560-4387-ac5e-c6a4b8d2d61c/lessons/699689362/concepts/7796785460923
# 
# 
# python syntax
# 
# https://developer.rhino3d.com/guides/rhinopython/python-statements/
# 
# 
# reads file
# 
# https://www.w3schools.com/python/python_file_open.asp
# 
# 
# Db size
# 
# https://stackoverflow.com/questions/6364577/how-to-get-the-current-sqlite-database-size-or-package-size-in-android
# 
# 
# SQLite 3
# 
# 
# 
# https://stackoverflow.com/questions/46028456/import-csv-files-into-sql-database-using-sqlite-in-python
# 
# 
# 
# https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
# 
# 
# https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
# 
# 
# https://stackoverflow.com/questions/30927802/retrieve-value-from-a-fetchone-call-in-python-3
# 
# 
# SQL
# 
# (FR)
# https://www.sqlfacile.com/apprendre_bases_de_donnees/count_et_group_by
# 
# 
# ## NOTA
# 
# As a python beginner, I put details I discovered learning on the documentation, tutorials, projects and trials in order to refer to my own work afterwards.

# # CSV & OSM file size
# 
# Code is pretty straight forward

# In[150]:


import os


NODES_PATH = "csv/nodes.csv"
NODE_TAGS_PATH = "csv/nodes_tags.csv"
WAYS_PATH = "csv/ways.csv"
WAY_NODES_PATH = "csv/ways_nodes.csv"
WAY_TAGS_PATH = "csv/ways_tags.csv"

print("XML Data","\n")
print("map.osm :",round(os.stat("data/map.osm").st_size/1024/1024),"Mo")
print("data/small_sample_map.osm :",round(os.stat("data/small_sample_map.osm").st_size/1024/1024),"Mo")
print("\n")
print("CSV Data","\n")
print(NODES_PATH," :",round(os.stat(NODES_PATH).st_size/1024/1024),"Mo")
print(NODE_TAGS_PATH," :",round(os.stat(NODE_TAGS_PATH).st_size/1024/1024),"Mo")
print(WAYS_PATH," :",round(os.stat(WAYS_PATH).st_size/1024/1024),"Mo")
print(WAY_NODES_PATH," :",round(os.stat(WAY_NODES_PATH).st_size/1024/1024),"Mo")
print(WAY_TAGS_PATH," :",round(os.stat(WAY_TAGS_PATH).st_size/1024/1024),"Mo")


# # SQL Database creation, import of data, data check  
# 
# SQL coding is way more easy than the iterative parsing and the CSV exportation.  
# We create or open a database, we use the cursor to input command and to get output. 

# In[1]:


#
# Final
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import sqlite3
import csv
import pandas as pd

NODES_PATH = "csv_test/nodes.csv"
NODE_TAGS_PATH = "csv_test/nodes_tags.csv"
WAYS_PATH = "csv_test/ways.csv"
WAY_NODES_PATH = "csv_test/ways_nodes.csv"
WAY_TAGS_PATH = "csv_test/ways_tags.csv"

"""
NODES_PATH = "csv/nodes.csv"
NODE_TAGS_PATH = "csv/nodes_tags.csv"
WAYS_PATH = "csv/ways.csv"
WAY_NODES_PATH = "csv/ways_nodes.csv"
WAY_TAGS_PATH = "csv/ways_tags.csv"
"""

#Reminder TABLES
"""
nodes
nodes_tags
ways
ways_tags
ways_nodes
"""

def main():

    #con = sqlite3.connect("database") # change to 'sqlite:///your_filename.db'
    con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()
    
    
    data_wrangling_schemaScript = open("data_wrangling_schema.sql", 'r')
    scripts = data_wrangling_schemaScript.read()
    data_wrangling_schemaScript.close()

    # all SQL commands (split on ';')
    tableCreations = scripts.split(';')

    # Execute every command from the input file
    for table in tableCreations:
        #print(table)
        cur.execute(table)
    
    con.commit()
    
    #Import CSV to sqlite database in two line !
    df = pd.read_csv("csv/nodes.csv")
    df.to_sql("nodes", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv/nodes_tags.csv")
    df.to_sql("nodes_tags", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv/ways.csv")
    df.to_sql("ways", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv/ways_tags.csv")
    df.to_sql("ways_tags", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv/ways_nodes.csv")
    df.to_sql("ways_nodes", con, if_exists='append', index=False)

#queries to do
#-size of the file
#-number of unique users
#-number of nodes and ways
#-number of chosen type of nodes, like cafes, shops etc.
#Request with a jointure

    
    print("Database Size")
    query = "SELECT page_count * page_size as size             FROM pragma_page_count(), pragma_page_size();"
    cur.execute(query)
    rows=cur.fetchone()
    print(round(rows[0]/1024/1024)," Mo")

    print("\n")
    
    print("Unique USERS")
    query = "SELECT COUNT(distinct(uid))             FROM                 (SELECT uid                 FROM nodes                     UNION ALL                 SELECT uid                 FROM ways);"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)
    

    print("\n")   
    
    print("Number of WAYS")
    query = "SELECT COUNT(*)             FROM ways;"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)
    
    
    print("\n")   
    
    print("Number of NODES")
    query = "SELECT COUNT(*)             FROM nodes;"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

    
    print("\n")   
    
    print("Count types of nodes")
    query = "SELECT type,count(*)             FROM nodes_tags             group by type;"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

   
    print("\n")   
    
    print("Count keys of nodes")
    query = "SELECT key,count(*)             FROM nodes_tags             group by key;"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)



    print("\n")   
    
    print("School and jointure, get who added schools and the postcode of schools")
    query = "SELECT nodes.user, nodes.id, nodes_tags.value             FROM nodes, nodes_tags             WHERE nodes.id = nodes_tags.id             AND nodes_tags.type ='school'"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

    
    print("\n")   
    
    print("Postcode analysis")
    query = "SELECT value, count(*)             FROM nodes_tags             WHERE key = 'postcode'             group by value;"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)
    


    print("\n")   
    
    print("Top 10 amenity")
    query = "SELECT value, COUNT(*) as num             FROM nodes_tags             WHERE key='amenity'             GROUP BY value             ORDER BY num DESC             LIMIT 10;"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

  
    
    print("\n")   
    
    print("Restaurant type")
    query = "SELECT value,count(*) as num             FROM                 (SELECT key,value                 FROM nodes_tags                     UNION ALL                 SELECT key,value                 FROM ways_tags) as allTags                 WHERE allTags.key like 'cuisine'             GROUP BY value             ORDER BY num desc limit 20;"
  
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)
    
    
    con.close() 


           
      
    
if __name__ == "__main__":
    main()


# 

# # For test purpose only 

# In[119]:


#
# TEst !
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import sqlite3
import csv
import pandas as pd

NODES_PATH = "csv_test/nodes.csv"
NODE_TAGS_PATH = "csv_test/nodes_tags.csv"
WAYS_PATH = "csv_test/ways.csv"
WAY_NODES_PATH = "csv_test/ways_nodes.csv"
WAY_TAGS_PATH = "csv_test/ways_tags.csv"

"""
NODES_PATH = "csv/nodes.csv"
NODE_TAGS_PATH = "csv/nodes_tags.csv"
WAYS_PATH = "csv/ways.csv"
WAY_NODES_PATH = "csv/ways_nodes.csv"
WAY_TAGS_PATH = "csv/ways_tags.csv"
"""

#Reminder TABLES
"""
nodes
nodes_tags
ways
ways_tags
ways_nodes
"""

def main():

    con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()
   
    data_wrangling_schemaScript = open("data_wrangling_schema.sql", 'r')
    scripts = data_wrangling_schemaScript.read()
    data_wrangling_schemaScript.close()

    # all SQL commands (split on ';')
    tableCreations = scripts.split(';')

    # Execute every command from the input file
    for table in tableCreations:
        #print(table)
        cur.execute(table)
    
    con.commit()
    
    df = pd.read_csv("csv_test/nodes.csv")
    df.to_sql("nodes", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv_test/nodes_tags.csv")
    df.to_sql("nodes_tags", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv_test/ways.csv")
    df.to_sql("ways", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv_test/ways_tags.csv")
    df.to_sql("ways_tags", con, if_exists='append', index=False)
    
    df = pd.read_csv("csv_test/ways_nodes.csv")
    df.to_sql("ways_nodes", con, if_exists='append', index=False)

    print("NODES")
    query = "SELECT *  FROM nodes LIMIT 3"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

    print("NODES TAGS")
    query = "SELECT *  FROM nodes_tags LIMIT 3"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

    print("WAYS")
    query = "SELECT *  FROM ways LIMIT 3"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)
    
    print("WAYS TAGS")
    query = "SELECT *  FROM ways_tags LIMIT 3"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

    print("WAYS NODES")
    query = "SELECT *  FROM ways_nodes LIMIT 3"
    cur.execute(query)
    rows=cur.fetchall()
    pprint(rows)

    
    
    """
    query = "SELECT *  FROM t"
    cur.execute(query)
    rows=cur.fetchall()

    pprint(rows)
    """
    
    
    
    
    con.close()
    
if __name__ == "__main__":
    main()


# In[3]:


#For test purpose only
con = sqlite3.connect("DB") # change to 'sqlite:///your_filename.db'
con.close()


# In[94]:


#
# Test !
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import pandas as pd
import sqlite3
import csv
import logging

"""
OSM_PATH = 'data/small_sample_map.osm'

NODES_PATH = "csv_test/nodes.csv"
NODE_TAGS_PATH = "csv_test/nodes_tags.csv"
WAYS_PATH = "csv_test/ways.csv"
WAY_NODES_PATH = "csv_test/ways_nodes.csv"
WAY_TAGS_PATH = "csv_test/ways_tags.csv"
"""

OSM_PATH = 'data/map.osm'

NODES_PATH = "csv/nodes.csv"
NODE_TAGS_PATH = "csv/nodes_tags.csv"
WAYS_PATH = "csv/ways.csv"
WAY_NODES_PATH = "csv/ways_nodes.csv"
WAY_TAGS_PATH = "csv/ways_tags.csv"



def main():

    con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()
    cur.execute("CREATE TABLE t (col1, col2);")
    
    
    #with open('data.csv','r') as fin: # `with` statement available in 2.5+
    ## csv.DictReader uses first line in file for column headings by default
    #dr = csv.DictReader(fin) # comma is default delimiter
    #to_db = [(i['col1'], i['col2']) for i in dr]

    #cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
    cur.execute("INSERT INTO t (col1, col2) VALUES ('Aaaaaaaaaaaaaaaaaaaaaaaaaaaaa', '1');")
    cur.execute("INSERT INTO t (col1, col2) VALUES ('Bbbbbbbbbbbbbbbbbbbbbbbbbbbbb', '2');")
    cur.execute("INSERT INTO t (col1, col2) VALUES ('Ccccccccccccccccccccccccccccc', '3');")
    con.commit()
    
    
    query = "SELECT *  FROM t"
    cur.execute(query)
    rows=cur.fetchall()

    pprint(rows)
    
    
    
    
    
    con.close()
    
if __name__ == "__main__":
    main()


# In[ ]:


#Reminder of project 
"""

CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

"""

