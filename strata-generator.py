from typing import List
from xml.etree.ElementTree import ElementTree

from file_utils import FileUtils

def get_keywords(fileTree: ElementTree) -> List[str]:
  rosterSchema = '{http://www.battlescribe.net/schema/rosterSchema}'
  keywords: List[str] = []
  names: List[str] = []

  for selection in fileTree.iter(f'{rosterSchema}selection'):
    if selection.get('type') == 'model' or selection.get('type') == 'unit':
      names.append(selection.get('name'))

      for category in selection.iter(f'{rosterSchema}categories'):
        keywords.extend([category.get('name') for category in category])

  print(*list(set(names)), sep='\n')
  return list(set(keywords))

if __name__ == '__main__':
  # get filename from arguments

  filename = '2k Undivided'
  # filename = 'Test_Custodes'

  fileTree = FileUtils.extract_roster(filename)
  keywordSet = get_keywords(fileTree)

  FileUtils.sync_csv_files()
