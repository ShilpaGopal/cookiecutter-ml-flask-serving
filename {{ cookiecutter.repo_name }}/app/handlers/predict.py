import binascii
from provider import preprocess
from provider import postprocess
from provider.predict import predict
from config.config import MODEL_CONFIG
from api.response import __200_ok, __500_error, __400_failed_field_validation
from constants import constants as const


PREPROCESS_ERROR_EVENT = const.SVC_SHORT_NAME+'PreprocessErrorEvent'
POSTPROCESS_ERROR_EVENT = const.SVC_SHORT_NAME+'PostprocessErrorEvent'
PREPROCESS_SUCCESS_EVENT = const.SVC_SHORT_NAME+'PreprocessSuccessEvent'
POSTPROCESS_SUCCESS_EVENT = const.SVC_SHORT_NAME+'PostprocessSuccessEvent'


class ModelPredict:
    def __init__(self, model, roi):
        self.model = model
        self.roi = roi

    def run(self, req_id, logger):
        ok_res = None

        image, err, res_stat = transform_image(self.roi, req_id, logger)
        if err is not None:
            return ok_res, err, res_stat

        temp_pred, err, res_stat = get_prediction(image, self.model, req_id, logger)
        if err is not None:
            return ok_res, err, res_stat

        ok_res, err, res_stat = decode_prediction(temp_pred, req_id, logger)

        return ok_res, err, res_stat


def transform_image(roi, req_id, logger):
    processed_img = None
    err = None
    res_stat = None
    if roi is not None:
        try:
            processed_img = preprocess.run(roi)
            logger.debug(msg='roi preprocessed successfully', event=PREPROCESS_SUCCESS_EVENT, req_id=req_id)
            return processed_img, err, res_stat
        except binascii.Error:
            error_msg = 'invalid base64-encoded string for roi'
            err_res, res_stat = __400_failed_field_validation(error=error_msg, field='roi', field_msg='the field of '
                                                                                                      'the '
                                                                                                      'request is '
                                                                                                      'not valid')
            logger.error(msg=error_msg, event=PREPROCESS_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                         status_code=res_stat.code)
            return processed_img, err_res, res_stat
        except preprocess.InputFormatException:
            error_msg = 'invalid format string for roi'
            err_res, res_stat = __400_failed_field_validation(error=error_msg, field='roi',
                                                              field_msg='the field of the '
                                                                        'request is '
                                                                        'not valid')
            logger.error(msg=error_msg, event=PREPROCESS_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                         status_code=res_stat.code)
            return processed_img, err_res, res_stat
        except Exception:
            error_msg = 'error occurred while preprocessing the image'
            err_res, res_stat = __500_error(error_msg)
            logger.error(msg=error_msg, event=PREPROCESS_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                         status_code=res_stat.code)
            return processed_img, err_res, res_stat
    else:
        error_msg = 'error occurred while preprocessing the image, roi is null'
        err_res, res_stat = __500_error(error_msg)
        logger.error(msg=error_msg, event=PREPROCESS_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                     status_code=res_stat.code)
        return processed_img, err_res, res_stat


def get_prediction(image, model, req_id, logger):
    pred = None
    err_res = None
    res_stat = None
    if image is not None:
        try:
            pred = predict(model, image)
            logger.debug(msg='prediction successful', event=const.PREDICT_SUCCESS_EVENT, req_id=req_id)
            return pred, err_res, res_stat
        except Exception:
            error_msg = 'error occurred while prediction'
            err_res, res_stat = __500_error(error_msg)
            logger.error(msg=error_msg, event=const.PREDICT_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                         status_code=res_stat.code)
            return pred, err_res, res_stat
    else:
        error_msg = 'error occurred while prediction, preprocessed image is null'
        err_res, res_stat = __500_error(error_msg)
        logger.error(msg=error_msg, event=const.PREDICT_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                     status_code=res_stat.code)
        return pred, err_res, res_stat


def decode_prediction(pred, req_id, logger):
    ok_res = None
    err_res = None
    try:
        if pred.size != 0:
            decoded_pred = postprocess.run(pred, MODEL_CONFIG['crnn_threshold'], MODEL_CONFIG['crnn_max_pred'],
                                           MODEL_CONFIG['crnn_top_path'])
            if any([ele for ele in decoded_pred]):
                ok_res, res_stat = __200_ok(decoded_pred)
                logger.info(msg="prediction successful", event=const.PREDICT_SUCCESS_EVENT,
                            status_code=res_stat.code, req_id=req_id, res=ok_res)
                return ok_res, err_res, res_stat
            else:
                ok_res, res_stat = __200_ok(decoded_pred)
                logger.warning(msg="prediction successful, prediction returned no value", event=const.PREDICT_WARNING_EVENT,
                               status_code=res_stat.code, req_id=req_id)
                return ok_res, err_res, res_stat
        else:
            ok_res, res_stat = __200_ok(pred)
            logger.warning(msg='prediction successful, prediction returned no value', event=const.PREDICT_WARNING_EVENT, req_id=req_id,
                           status_code=res_stat.code)
            return ok_res, err_res, res_stat
    except Exception:
        error_msg = 'error occurred while processing the prediction'
        err_res, res_stat = __500_error(error_msg)
        logger.error(msg=error_msg, event=POSTPROCESS_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                     status_code=res_stat.code)
        return ok_res, err_res, res_stat
