import pathlib
import zipfile
from typing import List
from xml.etree.ElementTree import ElementTree
from lxml import etree

def get_path() -> pathlib.PurePath:
  data_path = pathlib.PurePath.joinpath(pathlib.Path.cwd(), 'data')
  return data_path

def extract_and_get_file(filename: str = '2k_Undivided.rosz') -> ElementTree:
  filename = '2k Undivided'
  # filename = 'Test_Custodes'
  ext = '.rosz'

  dataPath = get_path()
  with zipfile.ZipFile(dataPath.joinpath(filename + ext), 'r') as file:
    file.extractall(path=dataPath)

  return etree.parse(dataPath.joinpath(filename + '.ros'))

def get_keywords(fileTree: ElementTree) -> List[str]:
  keywords: List[str] = []

  for selection in fileTree.iter('{http://www.battlescribe.net/schema/rosterSchema}selection'):
    if selection.get('type') == 'model' or selection.get('type') == 'unit':
      for category in selection.iter('{http://www.battlescribe.net/schema/rosterSchema}categories'):
        keywords.extend([category.get('name') for category in category])

  return list(set(keywords))

if __name__ == '__main__':
  # get filename from arguments

  fileTree = extract_and_get_file()
  keywordSet = get_keywords(fileTree)

  print(*keywordSet, sep='\n')
