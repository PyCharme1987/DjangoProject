
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")

import django
django.setup()

from django.db import connection

curser = connection.cursor()

#cursor.execute("SELET name FROM sqlite_master WHERE type='table';" # get all table names
curser.execute("SELECT email FROM account_user;") # get all emails
users = curser.fetchall()

for i in users:
    print(i)

for i in range (len(users)):
    curser.execute(f"UPDATE account_user SET id = {i} WHERE email = '{users[i][0]}';") # updating id
    results = curser.fetchall()
    print(results)

curser.close()

