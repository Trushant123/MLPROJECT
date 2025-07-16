import sys
from dataclasses import dataclass
import os
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

@dataclass
class data_transformationconfig:
    preprocessor_filepath=os.path.join('artifacts','preprocessor.pkl')
class data_transformation:
    def __init__(self):
        self.data_transformation_config=data_transformationconfig()
    def get_data_transformer_object(self):
        try:
            num_col=["reading_score","writing_score"]
            cat_col=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder(sparse_output=False)),
                    ("scaler",StandardScaler())
                ]
            )
            preproccesor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_col),
                    ("cat_pipeline",cat_pipeline,cat_col)
                ]
            )
            return preproccesor
        
        except Exception as e:
               raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):
         try:
              train_df=pd.read_csv(train_path)
              test_df=pd.read_csv(test_path)
              logging.info("READ Train And Test Data")
              logging.info("obtaining preproccessor")
              preproccessing_obj=self.get_data_transformer_object()
              target_column_name="math_score"
              num_col=["reading_score","writing_score"]
              cat_col=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
              input_df_train_df=train_df.drop(columns=target_column_name,axis=True)
              target_feat_train_df=train_df[target_column_name]
              input_df_test_df=test_df.drop(columns=target_column_name,axis=True)
              target_feat_test_df=test_df[target_column_name]
              logging.info("applying preproccessor on training and testing data")
              input_feat_train_arr=preproccessing_obj.fit_transform(input_df_train_df)
              input_feat_test_arr=preproccessing_obj.transform(input_df_test_df)
              train_arr=np.c_[
                   input_feat_train_arr,np.array(target_feat_train_df)
                              ]
              test_arr=np.c_[
                   input_feat_test_arr,np.array(target_feat_test_df)
              ]
              save_obj(
                   file_path=self.data_transformation_config.preprocessor_filepath,
                   obj=preproccessing_obj
              )
              logging.info("Data Transformation Done")
              return(
                   train_arr,test_arr,self.data_transformation_config.preprocessor_filepath
              )
              
         except Exception as e:
              raise CustomException(e,sys)
         

    