import pandas as pd
import numpy as np
from regex import D
import sys

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# importing scripts
sys.path.insert(1, '..')
sys.path.append("..")
sys.path.append(".")

from scripts import data_viz

class DataCleaner:
    """
    class that handles data cleaning.
    """
    def __init__(self, filehandler) -> None:
        self.summar = data_viz.Data_Viz("logs/data_clean_script.log") 
        file_handler = logging.FileHandler(filehandler)
        formatter = logging.Formatter("time: %(asctime)s, function: %(funcName)s, module: %(name)s, message: %(message)s \n")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def convert_to_datetime(self, df, columns):
        """
        convert to datetime.
        """
        for col in columns:
            df[col] = pd.to_datetime(df[col])

        logger.info("string successfully converted to datetime")
        return df

    def rename(self, df, col, old, new):
        """
        functions that renames specified list of old values with new ones
        in a column
        """
        for i in range(len(old)):
            df[col] = df[col].replace([old[i]], new[i])
            
        logger.info("values successfully renamed")

        return df
        


    def fill_outliers_mean(self, df, cols):
        df_temp = df.copy(deep=True)
        for col in cols:
            ''' Detection '''
            # IQR
            Q1 = df_temp[col].quantile(0.25)

            Q3 = df_temp[col].quantile(0.75)
            IQR = Q3 - Q1

            length=df_temp.shape[0]
            for index in range(length):
                if(df_temp.loc[index,col] >= (Q3+1.5*IQR)):
                    df_temp.loc[index,col] = np.nan

            ''' filling the Outliers '''
            df_temp = self.fill_missing_by_median(df_temp, cols)

        logger.info("outliers successfully filled with the mean value")

        return df_temp


    def removeOutliers(self, df,cols):
        df_temp = df.copy(deep=True)
        for col in cols:
            ''' Detection '''
            # IQR
            Q1 = df_temp[col].quantile(0.25)

            Q3 = df_temp[col].quantile(0.75)
            IQR = Q3 - Q1
            rm_lis = []
            length=df_temp.shape[0]
            for index in range(length):
                if(df_temp.loc[index,col] >= (Q3+1.5*IQR)):
                    rm_lis.append(index)

            ''' Removing the Outliers '''
            df_temp.drop(rm_lis, inplace = True)

        logger.info("outliers successfully removed")

        return df_temp
    
    def remove_cols(self, df, cols, keep=False):
        """
        a functions that removes specified columns from dataframe
        """
        if(keep):
            r_df = df.loc[:,cols]
        else:
            r_df = df.drop(cols, axis=1)

        logger.info("columns successfully removed")

        return r_df

    def reduce_dim_missing(self, df,limit):
        """
        removes columns with number of missing values greater than the provided limit
        """
        temp = self.summar.summ_columns(df)
        rem_lis = []
        for i in range(temp.shape[0]):
            if(temp.iloc[i,2] > limit):
                rem_lis.append(temp.iloc[i,0])
        r_df = df.drop(rem_lis, axis=1) 

        logger.info("columns with missing values removed successfully")
        
        return r_df

    
    def fill_missing_by_mode(self, df, cols=None):
        """
        fills missing values by mode
        """
        mod_fill_list = []
        if(cols == None):
            temp = self.summar.summ_columns(df)
            for i in range(temp.shape[0]):
                if(temp.iloc[i,3] == "object"):
                    mod_fill_list.append(temp.iloc[i,0])
        else:
            for col in cols:
                mod_fill_list.append(col)
        
        for col in mod_fill_list:
            df[col] = df[col].fillna(df[col].mode()[0])
        
        logger.info("missing values filled with mode")

        return df


    def fill_missing_by_mean(self, df, cols=None):
        """
        fills missing values by mean
        """
        temp = self.summar.summ_columns(df)
        mean_fill_list = []
        
        if cols is None:
            for i in range(temp.shape[0]):
                if(temp.iloc[i,3] == "float64"):
                    mean_fill_list.append(temp.iloc[i,0])
        else:
            for col in cols:
                mean_fill_list.append(col)
        
        for col in mean_fill_list:
            df[col] = df[col].fillna(df[col].median())
        
        logger.info("missing value successfully filled with the mean")

        return df

    def fill_missing_by_median(self, df, cols=None):
        """
        fills missing values by median.
        """
        temp = self.summar.summ_columns(df)
        median_fill_list = []

        if cols is None:
            for i in range(temp.shape[0]):
                if(temp.iloc[i,3] == "float64" or temp.iloc[i,3] == "int64"):
                    median_fill_list.append(temp.iloc[i,0])
        else:
            for col in cols:
                median_fill_list.append(col)

        for col in median_fill_list:
            df[col] = df[col].fillna(df[col].median())

        logger.info("missing values successfully filled with the median value")

        return df


    


    


    

    

    