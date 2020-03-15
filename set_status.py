import datetime
import pytz
from notion.client import NotionClient

client = NotionClient(
    token_v2="ef1861814ee0cec302083947747eedcf568865ac519fd7f7e492c184062fec934bf610a73fc2fd2e24c9c0901169ad4646db6a1fee7d21c9102cdadacf364b8ee59fa3ad52cf1eb99037e1527b5e")
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
