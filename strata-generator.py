from xml.etree.ElementTree import ElementTree

from file_utils import FileUtils

def get_keywords(fileTree: ElementTree) -> dict:
  rosterSchema = '{http://www.battlescribe.net/schema/rosterSchema}'
  keyword_dict = {
    'names': [],
    'keywords': []
  }

  # TODO: FIURE OUT HOW TO EXTRACT FACTION

  for selection in fileTree.iter(f'{rosterSchema}selection'):
    if selection.get('type') == 'model' or selection.get('type') == 'unit':
      keyword_dict['names'].append(selection.get('name'))

      for category in selection.iter(f'{rosterSchema}categories'):
        keyword_dict['keywords'].extend([category.get('name') for category in category])

  keyword_dict = {key: list(set(value)) for key, value in keyword_dict.items()}
  return keyword_dict

if __name__ == '__main__':
  # get filename from arguments

  filename = '2k Undivided'
  # filename = 'Test_Custodes'

  fileTree = FileUtils.extract_roster(filename)
  keywords_dict = get_keywords(fileTree)

  # FileUtils.sync_csv_files()

  data = FileUtils.load_datasheets_csv()
  print(data.columns)
