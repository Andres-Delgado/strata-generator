from xml.etree.ElementTree import ElementTree

from file_utils import FileUtils

def get_keywords(fileTree: ElementTree) -> dict:
  rosterSchema = '{http://www.battlescribe.net/schema/rosterSchema}'
  keyword_dict = {
    'names': [],
    'keywords': []
  }

  # TODO: FIGURE OUT HOW TO EXTRACT FACTION

  for selection in fileTree.iter(f'{rosterSchema}selection'):
    if selection.get('type') == 'model' or selection.get('type') == 'unit':
      keyword_dict['names'].append(selection.get('name'))

      for category in selection.iter(f'{rosterSchema}category'):
        keyword_dict['keywords'].append(category.get('name'))

  keyword_dict = {key: list(set(value)) for key, value in keyword_dict.items()}
  return keyword_dict

if __name__ == '__main__':
  # get filename from arguments

  filename = '2k Undivided'
  # filename = 'Test_Custodes'

  fileTree = FileUtils.extract_roster(filename)
  keyword_dict = get_keywords(fileTree)

  # FileUtils.sync_csv_files()

  ##################################
  # TODO: STRING DISTANCE CHECKING #
  #  to go get faction/unit names  #
  ##################################

  data = FileUtils.load_csv_to_dataframe('datasheets.csv')
  datasheetRows = data.loc[data['name'].isin(keyword_dict['names'])]
  datasheetIds = list(set(datasheetRows['id'].array))

  dataStratagems = FileUtils.load_csv_to_dataframe('datasheets_stratagems.csv')
  dataStratagemRows = dataStratagems.loc[dataStratagems['datasheet_id'].isin(datasheetIds)]
  stratagemIds = list(set(dataStratagemRows['stratagem_id'].array))

  stratagems = FileUtils.load_csv_to_dataframe('stratagems.csv')
  stratagemRows = stratagems.loc[stratagems['id'].isin(stratagemIds)]
