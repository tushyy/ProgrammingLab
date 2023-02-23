class ExamException(Exception):
    pass

class CSVFile():
    pass

class CSVTimeSeriesFile(CSVFile):

  def __init__(self, name):
    self.name = name
  
  def get_data(self):
    try: # controllo l'apertra del file
      my_file = open(self.name, 'r')
    except:
      raise ExamException('Errore: il file non può essere aperto o inesistente')
      
    try:
      my_file.readline()
      my_file.close() # reset conto righe
    except:
      raise ExamException('Errore: file non leggibile o vuoto')

    my_file = open(self.name, 'r')
    
    list_of_lists = []
    for line in my_file:
      nested_list = line.strip('\n').split(',') # tolgo il carattere \n e divido la lista in base alle virgole
      if nested_list[0] != 'data': # salto l'intestazione
        try:
          nested_list[1] = int(nested_list[1])
        except:
          continue # salta le righe non valide, che quindi non è possibile rendere interi
        list_of_lists.append(nested_list)

    for i in range(len(list_of_lists)-1): # controllo ordine in modo crescente
        if list_of_lists[i+1][0] <= list_of_lists[i][0]:
            raise ExamException('Errore: lista non ordinata o duplicato')
    my_file.close()
    return list_of_lists

def from_list_to_dict(time_series): # trasformo i la lista di dati di un anno in un dizionario di dizionari strutturato in questo modo: {anno :{mese1 :valore_mese1, mese2: valore_mese2}}
  
  years = [date[0][:4] for date in time_series]
  year_dicts = {}
  for year in years:
    year_dicts[year] = {}
  
  # riempio i dizionari con i dati disponibili
  for date in time_series:
    year = date[0][:4]
    month = int(date[0][5:])
    value = date[1]
    year_dicts[year][month] = value
  
  # aggiungo le chiavi mancanti con valore None
  for year in year_dicts:
    for month in range(1, 13):
      if month not in year_dicts[year]:
        year_dicts[year][month] = None
  
  return year_dicts

def detect_similar_monthly_variations(time_series, years):
  
  if type(time_series) is not list:
    raise ExamException('Errore: l\'argomento deve essere una lista')
  if type(years) is not list:
    raise ExamException('Errore: gli anni inseriti devono essere inseriti come lista')
  if len(years) != 2:
    raise ExamException('Errore: inserire esattamente due anni da comparare')
    
  year1 = years[0]
  year2 = years[1]
  
  if abs(int(year1)-int(year2)) != 1:
    raise ExamException('Errore: gli anni devono essere consecutivi')

  # crea una lista di dati da time series che comprendono solo i dati di un anno
  year_data1 = [item for item in time_series if item[0].startswith(str(year1))]
  year_data2 = [item for item in time_series if item[0].startswith(str(year2))]

  dict_year1 = from_list_to_dict(year_data1)
  dict_year2 = from_list_to_dict(year_data2)
    
  variation = []
  for i in range(1, 12):
    try:
      if dict_year1[str(year1)][i] is None or dict_year1[str(year1)][i+1] is None or dict_year2[str(year2)][i] is None or dict_year2[str(year2)][i+1] is None: # verifica che se un valore è None appenda False
        variation.append(False)
      elif abs((dict_year1[str(year1)][i] - dict_year1[str(year1)][i+1]) - (dict_year2[str(year2)][i] - dict_year2[str(year2)][i+1])) <= 2:
        variation.append(True)
      else:
        variation.append(False)
    except:
      raise ExamException('Errore: years non è compreso nel file CSV') # comprende anche l'eccezione di valori negativi o nulli, supponendo che nessun CSV valido abbia anni negativi
  return variation 

'''time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
variation = detect_similar_monthly_variations(time_series, [1949, 1950])
print(variation)'''
