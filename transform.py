import pandas as pd
from pandasql import sqldf
import json

class transform_process():
    def formatPriceMinor(self, Price):
        minorPrice = ''
        for i in range(len(Price)):
            if Price[i] == ' ':
                return minorPrice
                break
            elif Price[i].isdigit():
                minorPrice = minorPrice  + Price[i]
            else:
                continue
        return '0'

    def formatPriceMajor(self, Price):
        majorPrice = '0'
        start = 0
        for i in range(len(Price)):
            if Price[i] == ' ':
                majorPrice = ''
                start = 1
            elif start == 1 and Price[i].isdigit():
                majorPrice = majorPrice  + Price[i]
            else:
                continue
        return majorPrice

    def formatPrice(self, dataPandas):
        dataPandas['MinorPrice'] = 'NaN'
        dataPandas['MajorPrice'] = 'NaN'
        for i in range(len(dataPandas['Price'])):
                dataPandas['MinorPrice'][i] = int(self.formatPriceMinor(dataPandas.loc[:, 'Price'].values[i])) #Return column values using loc
                dataPandas['MajorPrice'][i] = int(self.formatPriceMajor(dataPandas['Price'][i])) #Return column values accessing directily the position

    def averagePrice(self, dataPandas):
        avgPrice = [(dataPandas['MinorPrice'][i] + dataPandas['MajorPrice'][i]) / 2 for i in range(len(dataPandas))]
        dataPandas['AveragePrice'] = avgPrice

    def priceAvaliation(self, AveragePrice):
        avaliation = ''
        if AveragePrice == 0:
            avaliation = 'Uninformed'
        elif AveragePrice <= 50:
            avaliation = 'Cheap'
        elif AveragePrice > 50 and AveragePrice <= 150:
            avaliation = 'Average'
        else:
            avaliation = 'Expensive'
        return avaliation

    def changeUniformed(self, dataPandas):
        pos = 0
        for data_uniformed in dataPandas['Position_Restaurants']:
            if data_uniformed == 'Uninformed':
                dataPandas.loc[dataPandas.index[pos], 'Position_Restaurants'] = str(pos+1) + ' of 17,631'
            pos = pos + 1
        return dataPandas

    def replace_text(self, dataPandas):
        dataPandas["Rating"] = dataPandas["Rating"].apply(lambda x: x.replace('\u00a0', ""))
        dataPandas["Position1"] = dataPandas["Position1"].apply(lambda x: x.replace('#', "").replace(' in Sao Paulo', ''))
        dataPandas["Position2"] = dataPandas["Position2"].apply(lambda x: x.replace('#', "").replace(' Restaurants in Sao Paulo', "").replace('none', 'Uninformed'))
        dataPandas["Reviews"] = dataPandas["Reviews"].apply(lambda x: x.replace(' reviews', ""))
        dataPandas["Phone"] = dataPandas["Phone"].apply(lambda x: x.replace('(', '').replace(')', '').replace('+55', '').replace('-', '').replace(' ', '').replace('none', '000000000').replace('.', ''))
        return dataPandas

    def transform(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        data = pd.read_json('extracted_data.json') 
        data = data.T #reverse rows and columns
        self.formatPrice(data)
        self.averagePrice(data)
        data['Avaliation'] = data['AveragePrice'].map(self.priceAvaliation)
        del data['Link']
        del data['Price']
        data = self.replace_text(data)
        data.rename(columns={'Position2': 'Position_Restaurants', 'Position1': 'Position_perCuisine'},inplace=True)
        data = self.changeUniformed(data)

        with open("transformed_data.json", "w") as write_file:
            json.dump(data.to_dict(orient='index'), write_file, indent=8)
        write_file.close()