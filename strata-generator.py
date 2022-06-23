import pathlib
import zipfile
from typing import List
from xml.etree.ElementTree import ElementTree
from lxml import etree
import requests
import urllib.request

def get_data_path() -> pathlib.PurePath:
  data_path = pathlib.PurePath.joinpath(pathlib.Path.cwd(), 'data')
  return data_path

def extract_and_get_file(filename: str = '2k_Undivided.rosz') -> ElementTree:
  filename = '2k Undivided'
  # filename = 'Test_Custodes'
  ext = '.rosz'

  dataPath = get_data_path()
  with zipfile.ZipFile(dataPath.joinpath(filename + ext), 'r') as file:
    file.extractall(path=dataPath)

  return etree.parse(dataPath.joinpath(filename + '.ros'))

def get_keywords(fileTree: ElementTree) -> List[str]:
  keywords: List[str] = []
  rosterSchema = '{http://www.battlescribe.net/schema/rosterSchema}'

  for selection in fileTree.iter(f'{rosterSchema}selection'):
    if selection.get('type') == 'model' or selection.get('type') == 'unit':
      for category in selection.iter(f'{rosterSchema}categories'):
        keywords.extend([category.get('name') for category in category])

  return list(set(keywords))

def get_strat_csv():
  url = 'https://wahapedia.ru/wh40k9ed/Stratagems.csv'
  headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.125 Safari/537.36'}
  response = requests.get(url, headers=headers)

  with open(get_data_path().joinpath('stratagems.csv'), 'wb') as outfile:
    outfile.write(response.content)

if __name__ == '__main__':
  # get filename from arguments
  allCsvUrl = 'https://wahapedia.ru/wh40k9ed/Export%20Data%20Specs.xlsx'
  factionsUrl = 'https://wahapedia.ru/wh40k9ed/Factions.csv'
  datasheetsUrl = 'https://wahapedia.ru/wh40k9ed/Datasheets.csv'
  keyswordsUrl = 'http://wahapedia.ru/wh40k9ed/Datasheets_keywords.csv'
  stratagemsId = 'http://wahapedia.ru/wh40k9ed/Datasheets_stratagems.csv'

  # from roster, get name for models/units/factions
  # find factionIDs from factions.csv with faction names
  # find datasheetIDs from datasheets.csv with model/unit names
  # find keywords from datasheets_keywords.csv with datasheetIDs

  fileTree = extract_and_get_file()
  keywordSet = get_keywords(fileTree)

  get_strat_csv()

  print(*keywordSet, sep='\n')
