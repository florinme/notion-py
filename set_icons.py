from notion.client import NotionClient

client = NotionClient(token_v2="fcbde2a33d8d564986e867ea99872ec082b6581f523bb8433eadf3d954256a6cd1bf84da5da8db62c1333ce74b7b4b33841dc4c75d6a5c5af45ff7ae25ce34d1bf042e05417caa7a6610b3e04413")

def set_icons(icon, parent_page_url_or_id):
  cv = client.get_collection_view(parent_page_url_or_id)
  if icon is None or icon == '':
    if cv.parent.icon is None or cv.parent.icon == '':
      print('There is no parent icon, you must provide one')
    else:
      icon = cv.parent.icon
  else:
    if cv.parent.icon is None or cv.parent.icon == '':
      cv.parent.icon = icon
  for row in cv.collection.get_rows():
    if (row.icon is None) or (row.icon == '') or (row.icon != icon):
      row.icon = icon

set_icons('🏃', 'https://www.notion.so/mdnt/c413404538d44a68af2b024e8b6767aa?v=0277131d489743a492fd9ab91a89d3d5')
set_icons('🏁', 'https://www.notion.so/mdnt/2b4384ac910847248555ccc4ae4d8209?v=1cee8558b4fd42179d5223ff8ac52c55')
