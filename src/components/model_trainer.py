import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor # type: ignore
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor # type: ignore
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.metrics import r2_score # type: ignore
from sklearn.neighbors import KNeighborsRegressor # type: ignore
from sklearn.tree import DecisionTreeRegressor # type: ignore
from xgboost import XGBRegressor # type: ignore

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array,test_array,preprocessor_path):
        try:
            logging.info('Splitting training and test input data.') # Coming from data transformation
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            models = {
                'Random Forest' : RandomForestRegressor(),
                'Decision Tree' : DecisionTreeRegressor(),
                'Gradient Boosting' : GradientBoostingRegressor(),
                'Linear Regression' : LinearRegression(),
                'K-Neighbors Regressor' : KNeighborsRegressor(),
                'XGBoost Regressor' : XGBRegressor(),
                'CatBoostRegressor' : CatBoostRegressor(verbose = False),
                'AdaBoostRegressor' : AdaBoostRegressor()
            }
            
            model_report:dict = evaluate_models(X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test, models = models)
            
            # To get best model score from dict
            best_model_score = max(sorted(model_report.values()))
            
            # To gest best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            
            if(best_model_score < 0.6):
                raise CustomException('No best model found.')
            
            logging.info(f'Best model found on both training and test datasets')
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            predicted = best_model.predict(X_test)
            
            r2_square = r2_score(y_test, predicted)
            
            return r2_square
            
        except Exception as e:
            raise CustomException(e,sys)

