

class DataHandler:
  def saveToFile(wools):
      # Save in json lines format, each line is a valid json object
      with open('./data.jsonl', 'w', encoding='utf-8') as dataFile:
          dataFile.writelines([x.toJSON() + '\n' for x in wools])
