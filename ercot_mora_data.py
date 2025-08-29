from bs4 import BeautifulSoup as bs
import requests
import re
import glob
import pandas as pd
import os

def get_soup(URL):
    return bs(requests.get(URL, verify=False).text, 'html.parser')

URL = "https://www.ercot.com/gridinfo/resource"
if __name__ == "__main__":
    mora_df = pd.DataFrame()
    for link in get_soup(URL).findAll("a", attrs={'href': re.compile(".xlsx")}):
        file_link = link.get('href')
        if 'MORA' in file_link:
            df = pd.read_excel(file_link, 
                               engine='openpyxl',
                               header=1,
                               sheet_name='Resource Details')
            df = df.iloc[:, : 10]
            df.columns =['Unnamed: 0', 'UNIT NAME', 
                   'INR', 'UNIT CODE', 'COUNTY',
                   'FUEL', 'ZONE',
                   'IN SERVICE',
                   'INSTALLED CAPACITY RATING (MW)',
                   'WINTER CAPACITY (MW)']
            df['file_link'] = file_link
            mora_df = pd.concat([mora_df, df])
    
    mora_df = mora_df[~mora_df['Unnamed: 0'].isna()] 
    mora_df = mora_df[mora_df['FUEL'] == "SOLAR"]
    # Subset MORA based on the actual ERCOT 15-minute data sets
    ercot_systems = [os.path.basename(x).replace(".csv", "") for x in glob.glob(
        "./ercot_15_min_data/plant_data/*.csv")]
    mora_df = mora_df[mora_df['UNIT CODE'].isin(ercot_systems)]
    mora_df.to_csv("./metadata/ercot_mora_data.csv", index=False)