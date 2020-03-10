import datetime
import pytz
from notion.client import NotionClient

client = NotionClient(token_v2="fcbde2a33d8d564986e867ea99872ec082b6581f523bb8433eadf3d954256a6cd1bf84da5da8db62c1333ce74b7b4b33841dc4c75d6a5c5af45ff7ae25ce34d1bf042e05417caa7a6610b3e04413")

def set_meta(parent_page_url_or_id):
  cv = client.get_collection_view(parent_page_url_or_id)
  for row in cv.collection.get_rows():
    goalsArray = []
    tagsArray = []
    if row.milestones:
      duration = datetime.datetime.now(tz=pytz.utc) - row.updated.replace(tzinfo=pytz.utc)
      if (not row.goals or not row.tags):
      # if (duration.total_seconds() <= 120) and (not row.goals or not row.tags):
        print('Updating: ' + row.name)

        goalsIdArray = []
        tagsIdArray = []
        for milestone in row.milestones:
          if milestone:
            if milestone.goals:
              for goal in milestone.goals:
                if (not goalsIdArray or goal.id not in goalsIdArray):
                  goalsArray.append(goal)
                  goalsIdArray.append(goal.id)
                if goal.tags:
                  for goalTag in goal.tags:
                    if (not tagsIdArray or goalTag.id not in tagsIdArray):
                      tagsArray.append(goalTag)
                      tagsIdArray.append(goalTag.id)
            if milestone.tags:
              for milestoneTag in milestone.tags:
                if (not tagsIdArray or milestoneTag.id not in tagsIdArray):
                  tagsArray.append(milestoneTag)
                  tagsIdArray.append(goalTag.id)
        row.goals = goalsArray
        row.tags = tagsArray

set_meta('https://www.notion.so/mdnt/c413404538d44a68af2b024e8b6767aa?v=0277131d489743a492fd9ab91a89d3d5')
