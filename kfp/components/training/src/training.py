import numpy as np
import xgboost as xgb

from helpers import gcs


def train_model(gcs_input_path,
                gcs_output_path,
                n_estimators, learning_rate, scale_pos_weight):
    if type(scale_pos_weight) == str and scale_pos_weight in ('TRUE', 'True', 'true'):
            hparams['scale_pos_weight'] = n_neg / n_pos
    elif type(scale_pos_weight) == str:
        scale_pos_weight = 1
            
    # Load training data
    gcs.download_file(f'{gcs_input_path}/X_train.npy', 'X_train.npy')
    X_train = np.load('X_train.npy', allow_pickle=True)
    gcs.download_file(f'{gcs_input_path}/y_train.npy', 'y_train.npy')
    y_train = np.load('y_train.npy', allow_pickle=True)
    
    # Train model
    xgb_model = xgb.XGBClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        scale_pos_weight=scale_pos_weight
    )
    xgb_model.fit(X_train, y_train)
    
    # Save trained model
    xgb_model.save_model('xgb_model.bin')
    gcs.upload_file('xgb_model.bin', f'{gcs_output_path}/xgb_model.bin')
