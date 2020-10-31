from api.response import __400_failed_field_validation, __500_error, __400_invalid_format
from constants import constants as const


class HTTPHandler:
    def __init__(self, req_body, req_id):
        self.body = req_body
        self.req_id = req_id

    def validate(self, logger):
        req_id = self.req_id
        roi = None
        body = self.body
        valid, err, res_stat = is_header_valid(req_id, logger)
        if not valid:
            return req_id, roi, err, res_stat

        roi, err_res, res_stat = get_roi(body, req_id.strip(), logger)
        return req_id.strip(), roi, err_res, res_stat


def is_header_valid(req_id, logger):
    err_res = None
    res_stat = None
    try:
        if not req_id:
            err_res, res_stat = __400_failed_field_validation(field='X-Request-ID',
                                                              field_msg='the field of the request '
                                                                        'missing in the header')
            logger.error(msg='X-Request-ID missing in the header', event=const.PREDICT_ERROR_EVENT,
                         error=res_stat.reason, status_code=res_stat.code)
            return False, err_res, res_stat

        elif len(req_id.strip()) == 0:
            err_res, res_stat = __400_failed_field_validation(field='X-Request-ID', field_msg='the field value of the '
                                                                                              'request is null in the '
                                                                                              'header')
            logger.error(msg='X-Request-ID value is null', event=const.PREDICT_ERROR_EVENT, error=res_stat.reason,
                         status_code=res_stat.code)
            return False, err_res, res_stat
        else:
            return True, err_res, res_stat
    except Exception:
        error_msg = 'error occurred while validating header'
        err_res, res_stat = __500_error(error_msg)
        logger.error(msg=error_msg, event=const.PREDICT_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                     status_code=res_stat.code)
        return False, err_res, res_stat


def get_roi(req_body, req_id, logger):
    roi = None
    err_res = None
    res_stat = None
    try:
        if req_body is not None:
            if req_body['roi'] is not None and len(req_body['roi'].strip()) != 0:
                roi = req_body['roi']
                return roi, err_res, res_stat
            else:
                err_res, res_stat = __400_failed_field_validation(field='roi',
                                                                  field_msg='the field value of the request is null in '
                                                                            'the body')
                logger.error(msg='roi value is null in the request body', event=const.PREDICT_ERROR_EVENT,
                             error=res_stat.reason, req_id=req_id,
                             status_code=res_stat.code)
                return roi, err_res, res_stat
        else:
            error_msg = 'empty request body'
            err_res, res_stat = __400_invalid_format(error_msg)
            logger.error(msg='empty request body', event=const.PREDICT_ERROR_EVENT,
                         error=res_stat.reason, req_id=req_id,
                         status_code=res_stat.code)
            return roi, err_res, res_stat
    except KeyError:
        err_res, res_stat = __400_failed_field_validation(field='roi',
                                                          field_msg='the field of the request is missing in the body')
        logger.error(msg='roi field is missing in the request body', event=const.PREDICT_ERROR_EVENT,
                     error=res_stat.reason,
                     req_id=req_id,
                     status_code=res_stat.code)
        return roi, err_res, res_stat
    except TypeError:
        error_msg = 'the request body is not a valid JSON'
        err_res, res_stat = __400_invalid_format(error_msg)
        logger.error(msg=error_msg, event=const.PREDICT_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                     status_code=res_stat.code)
        return roi, err_res, res_stat
    except Exception:
        error_msg = 'error occurred while validating request body'
        err_res, res_stat = __500_error(error_msg)
        logger.error(msg=error_msg, event=const.PREDICT_ERROR_EVENT, error=res_stat.reason, req_id=req_id,
                     status_code=res_stat.code)
        return roi, err_res, res_stat
