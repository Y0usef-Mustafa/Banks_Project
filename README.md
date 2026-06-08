# Banks_Project
# ETL Pipeline: Top 10 Largest Banks by Market Capitalization

## Project Overview
This project involves building an end-to-end Extract, Transform, Load (ETL) pipeline. The core objective is to extract data regarding the **top 10 largest banks in the world, ranked by market capitalization in billion USD**. 

The pipeline extracts this data, transforms the market capitalization values into other currencies (GBP, EUR, and INR) using current exchange rates, and loads the final processed data for further use.

## Files and Outputs
* **Output File:** The final output of this ETL process is the `Banks_Project.csv` file, which contains the processed and transformed data.
* **Exchange Rate Data:** For the transformation script to run successfully, the `exchange_rate.csv` file **must** be located in the same directory as the Python script.
* **code_log:** for tracking how the project works  

## Important Note on File Paths
Please note that the output path used in this script is configured to a specific local directory on the `F:` drive:
`F:\Data Topics\Data Engineering\Python project for Data Engineering\Banks_Project.csv`

*(If you are cloning or running this repository on a different machine, ensure you update the `csv_path` variable in the script to match your local environment).*
