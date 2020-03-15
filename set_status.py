import datetime
import pytz
from notion.client import NotionClient

client = NotionClient(
    token_v2="fcbde2a33d8d564986e867ea99872ec082b6581f523bb8433eadf3d954256a6cd1bf84da5da8db62c1333ce74b7b4b33841dc4c75d6a5c5af45ff7ae25ce34d1bf042e05417caa7a6610b3e04413")
pst = pytz.timezone('US/Pacific')
today = pst.localize(datetime.datetime.today()).date()
cv = client.get_collection_view(
    "https://www.notion.so/mdnt/c413404538d44a68af2b024e8b6767aa?v=0277131d489743a492fd9ab91a89d3d5")
rows = cv.collection.get_rows()

for row in rows:
    # print(row.name)
    if (row.status != 'Done'):
        if (row.scheduled and row.scheduled.start):
            if (type(row.scheduled.start) is datetime.datetime):
                # Has time data, set timezone and convert to date
                scheduled = pst.localize(row.scheduled.start).date()
            else:
                # No time data, convert to time, set timezone, and convert back to date
                scheduled = pst.localize(datetime.datetime(
                    year=row.scheduled.start.year, month=row.scheduled.start.month, day=row.scheduled.start.day)).date()

            if (scheduled < today):
                # Handle old scheduled tasks
                print("Moving " + row.name + " to Overdue")
                row.status = "Overdue"
            else:
                if (scheduled == today) and (row.status != 'Today' and row.status != 'Now'):
                    # Handle scheduled for Today
                    print("Moving: " + row.name + " to Today")
                    row.status = "Today"
                else:
                    if (scheduled > today) and (row.status != 'Upcoming'):
                        # Handle future scheduled tasks
                        print("Moving: " + row.name + " to Upcoming")
                        row.status = "Upcoming"
        elif (row.status != "Backlog"):
            # It's not done and doesn't have a scheduled date move to backlog
            row.status = "Backlog"
