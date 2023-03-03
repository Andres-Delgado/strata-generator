from xml.etree.ElementTree import ElementTree

from fileutils import FileUtils
from exporter import Exporter

class StrataGenerator:
  @staticmethod
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

  @classmethod
  def process(cls) -> str:
    filename = 'New_Roster'

    fileTree = FileUtils.extract_roster(filename)
    keyword_dict = cls.get_keywords(fileTree)

    # TODO: sync flag
    # FileUtils.sync_csv_files()

    ##################################
    # TODO: STRING DISTANCE CHECKING #
    #    to get faction/unit names   #
    ##################################

    data = FileUtils.load_csv_to_dataframe('datasheets.csv')
    datasheetRows = data.loc[data['name'].isin(keyword_dict['names'])]
    datasheetIds = list(set(datasheetRows['id'].array))
    print('datasheet ids: ', datasheetIds)

    dataStratagems = FileUtils.load_csv_to_dataframe('datasheets_stratagems.csv')
    dataStratagemRows = dataStratagems.loc[dataStratagems['datasheet_id'].isin(datasheetIds)]
    stratagemIds = list(set(dataStratagemRows['stratagem_id'].array))
    print('stratagem ids: ', stratagemIds)

    stratagems = FileUtils.load_csv_to_dataframe('stratagems.csv')
    stratagemRows = stratagems.loc[stratagems['id'].isin(stratagemIds)]
    print(stratagemRows.columns.tolist())

    Exporter.to_json(stratagemRows)
    return filename
