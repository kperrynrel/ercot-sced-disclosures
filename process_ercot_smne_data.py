"""
Unzip all of the SCED files (located in a folder called /ercot_15_min_data),
and build a master dataframe of all of the data.
"""

import zipfile,fnmatch,os
import glob
import pandas as pd
import os

if __name__ == "__main__":
    rootPath = r"./ercot_15_min_data"
    downloadPath = r"./Downloads"
    # Unzip all of the SCED folders
    pattern = '*.zip'
    zip_files = glob.glob(os.path.join(downloadPath, "*.zip"))
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(rootPath + "/" +  
                                os.path.basename(zip_file).replace(".zip", ""))
        files = glob.glob(rootPath + "/" +  os.path.basename(zip_file).replace(".zip", "")+ 
                          "/*")
        for file in files:
            if "SMNE" not in file:
                os.remove(file)
        # Move the file to S3 and then delete it
        
    # Open up all of the SMNE files in the zipped folders.
    files = glob.glob(os.path.join(rootPath, "*/*SMNE*.csv"))
    master_df_list = list()
    for file in files:
        try:
            df = pd.read_csv(file,
                             on_bad_lines='skip',
                             engine='python')
            df.columns = ["Interval Time",
                          "Interval Number",
                          "Resource Code",
                          "Interval Value"]
            master_df_list.append(df)
            print("data added!")
            print(len(master_df_list))
        except Exception as e:
            print(e)
                    
    master_df = pd.concat(master_df_list, axis=0)
    # Clean up the data set, get all of the plants, etc
    # Interval Time cleanup
    master_df['Interval Time'] = master_df['Interval Time'].str.replace('"', "")
    master_df['Interval Time'] = pd.to_datetime(master_df['Interval Time'],
                                                format='mixed')
    # Get the names of all of the plants
    plants = list(master_df['Resource Code'].drop_duplicates())
    missing_dates_list = list()
    already_inserted = glob.glob(os.path.join(rootPath, "plant_data/*.csv"))
    already_inserted = [os.path.basename(x) for x in already_inserted]
    for plant in plants:
        file_name = os.path.join(rootPath, "plant_data/" + plant.replace("\x00", "").replace('"', "") +".csv")
        if os.path.basename(file_name) in already_inserted:
            print("Already processed!")
            continue
        else:
            try:
                df_subset = master_df[master_df['Resource Code'] == plant]
                df_subset = df_subset.sort_values(by="Interval Time")
                # Check for any missing dates in the middle of the sequence
                full_range = pd.date_range(df_subset['Interval Time'].min().date(), 
                                           df_subset['Interval Time'].max().date()).date
                time_series_dates = list(df_subset['Interval Time'].dt.date.drop_duplicates())
                missing_dates = list(set(full_range) - set(time_series_dates))
                missing_dates_list = missing_dates_list + missing_dates
                df_subset.to_csv(file_name,
                                 index=False)
            except Exception as e:
                print(e)
                print(plant)
                break
