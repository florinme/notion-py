import datetime
from notion.client import *

client = NotionClient(token_v2="fcbde2a33d8d564986e867ea99872ec082b6581f523bb8433eadf3d954256a6cd1bf84da5da8db62c1333ce74b7b4b33841dc4c75d6a5c5af45ff7ae25ce34d1bf042e05417caa7a6610b3e04413")

cv = client.get_collection_view("https://www.notion.so/mdnt/c413404538d44a68af2b024e8b6767aa?v=0277131d489743a492fd9ab91a89d3d5")

for row in cv.collection.get_rows():
  # print(row.name)
  if (row.status != 'Done') and (row.scheduled and row.scheduled.start):
    # Is this task scheduled for today?
    if (type(row.scheduled.start) is datetime.datetime):
      today = datetime.datetime.today()
    else:
      today = datetime.datetime.today().date()
    if (row.scheduled.start < today):
      # Handle old scheduled tasks
      print("Moving " + row.name + " to No Status")
      row.scheduled = None
      row.status = None
    else:
      if (row.scheduled.start == today) and (row.status != 'Today' and row.status != 'Now'):
        # Handle scheduled for Today
        print("Moving: " + row.name + " to Today")
        row.status = "Today"
      else:
        if (row.scheduled.start > today) and (row.status != 'Upcoming' and row.status != 'Backlog'):
          # Handle future scheduled tasks
          print("Moving: " + row.name + " to Upcoming")
          row.status = "Upcoming"
  if (row.status == 'Today' or row.status == 'Now') and (row.scheduled == None):
    print("Scheduling: " + row.name + " for Today ")
    row.scheduled = datetime.datetime.today().date()
  if (row.status == 'Upcoming') and (row.scheduled == None):
    print("Scheduling: " + row.name + " for Tomorrow ")
    row.scheduled = datetime.datetime.today().date() + datetime.timedelta(days=1)
