from tensorflow.keras.models import load_model
from config.config import MODEL_CONFIG
import constants.constants as const

import sys
import os

model_filepath = MODEL_CONFIG['model_path']
MODEL_INIT_SUCCESS_EVENT = const.MODEL_NAME+'InitSuccessEvent'
MODEL_INIT_ERROR_EVENT = const.MODEL_NAME+'InitErrorEvent'


def load(logger):
    try:
        model = load_model(model_filepath, compile=False)
        logger.info(msg="model loaded successfully: worker pid " + str(os.getpid()), event=MODEL_INIT_SUCCESS_EVENT)
        return model
    except OSError:
        logger.error(msg="unable to load the model", event=MODEL_INIT_ERROR_EVENT, error='saved model file does not exist')
        sys.exit()
    except Exception:
        logger.error(msg="unable to load the model", event=MODEL_INIT_ERROR_EVENT, error="model initialisation failed")
        sys.exit()