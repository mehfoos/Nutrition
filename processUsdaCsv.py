'''
Main program for generating Nutrition Spreadsheet from USDA csv data download
Tested with foundation foods + supporting data from 2022
'''

__author__ = "Mehfoos"
__version__ = "0.1.0" # major.minor.patch
__license__ = "MIT"   

""" Imports """
import pandas as pd
import os

""" Main entry point of the app """
def main():
    """ All user configuration changes are applied here """
    
    # Folder path including all csv files from USDA
    usda_download_folder = r"C:\Users\mly509\Downloads\USDA Food"
    
    """ Import relevant csv files """
    food_category = pd.read_csv(os.path.join(usda_download_folder,"food_category.csv"))
    nutrient = pd.read_csv(os.path.join(usda_download_folder,"nutrient.csv"))
    food = pd.read_csv(os.path.join(usda_download_folder,"food.csv"))
    food_nutrient = pd.read_csv(os.path.join(usda_download_folder,"food_nutrient.csv"))
    nutrient = pd.read_csv(os.path.join(usda_download_folder,"nutrient.csv"))

    """ Create new Dataframe and fill with food information """

    # Create new dataframe/table, starting with "food" table, filtered to only include "foundation foods"
    df_main = food[food.data_type=='foundation_food']

    # Only keep the columns we desire
    df_main = df_main[['fdc_id','description','food_category_id']]

    # Rename food description as such
    df_main.rename(columns={'description': 'Food Description'}, inplace=True)

    # Replace food_category_id with description
    df_main = pd.merge(df_main, food_category[['id','description']], how='left', left_on='food_category_id', right_on='id')

    # Rename food category as such
    df_main.rename(columns={'description': 'Food Category'}, inplace=True)

    # Only keep the columns we desire
    df_main = df_main[['fdc_id','Food Description','Food Category']]

    # Reorder
    df_main = df_main[['fdc_id', 'Food Category','Food Description']]

    """ Pivot the Food nutrition data to have nutrition as separate columns """

    # Pivot by food id, on nutrient id, by amount values
    df_food_nutrient = food_nutrient.pivot(index='fdc_id', columns='nutrient_id', values='amount')

    # remove column name
    df_food_nutrient.reset_index(inplace=True)
    # df_food_nutrient = df_food_nutrient.rename_axis(None, axis=1)

    # Concatenate units to nutrient name
    nutrient['Nutrient'] = nutrient['name'] + ' [' + nutrient['unit_name'] + ']'

    # Rename Nutrient id in df_food_nutrient to name of nutrient
    df_food_nutrient.rename(columns=nutrient.set_index('id')['Nutrient'], inplace=True)

    """ Merge Main table with nutrition data """
    df_main = pd.merge(df_main, df_food_nutrient, how='left', on='fdc_id')

    ''' Export '''
    df_main.to_csv('NutritionDatabase.csv')

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()