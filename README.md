# ercot-sced-disclosures
Scripts for pulling down ERCOT SCED disclosures.

#1: Run the ercot_historic_pull.py file

This file is run by a Selenium driver, and downloads all historic data back to 2011 for all sites in ERCOT. This script will likely take 8-10 hours to run as it is simulating a full web session. To pull back a few months (approx. 6 months), use the ERCOT API specifically. The API does NOT contain all data from the dataset, but rather a subset.

#2: Run the process_ercot_smne_data.py file

This script unzips and processes all of the historic ERCOT download from step 1. You will need to specific input/output folder for the data set in this script. 

# Run the ercot_mora_data.py file
This script pulls all of the metadata associated with the ERCOT data set. It will be used subsequently for matching with the EIA data set via system/site name.

# Run the eia_860_pulls.py file
This pulls down all of the historic EIA systems from the API. It also takes several hours to run and requires and EIA API key.
