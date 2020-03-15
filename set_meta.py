import datetime
import pytz
from notion.client import NotionClient

client = NotionClient(
    token_v2="ef1861814ee0cec302083947747eedcf568865ac519fd7f7e492c184062fec934bf610a73fc2fd2e24c9c0901169ad4646db6a1fee7d21c9102cdadacf364b8ee59fa3ad52cf1eb99037e1527b5e")


def set_meta(parent_page_url_or_id):
    cv = client.get_collection_view(parent_page_url_or_id)
    for row in cv.collection.get_rows():
        goalsArray = []
        tagsArray = []
        if row.milestones:
            duration = datetime.datetime.now(
                tz=pytz.utc) - row.updated.replace(tzinfo=pytz.utc)
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
