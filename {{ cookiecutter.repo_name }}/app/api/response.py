from typing import List
import json
from constants import constants as const
from http import HTTPStatus


class PredictionSuccess:
    def __init__(self, pred):
        self.prediction = pred

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class NestedError(object):
    def __init__(self, error_code):
        self.errorCode = error_code if error_code is not None else ''

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class ErrorDetail(object):
    def __init__(self, message, nested_errors: List[NestedError], message_local=None):
        self.message = message
        self.messageLocal = message_local if message_local else ''
        self.nestedErrors = nested_errors

    @classmethod
    def from_json(cls, data):
        nestedErrors = list(map(NestedError.from_json, data["nestedErrors"]))
        return cls(nestedErrors)


class InvalidField:
    def __init__(self, field, msg):
        self.field = field
        self.msg = msg

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class Error:
    def __init__(self, error_code, error_detail):
        self.errorCode = error_code
        self.errorDetail = error_detail

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class BadRequestError(object):
    def __init__(self, error_code, error_detail, invalid_fields: List[InvalidField]):
        self.errorCode = error_code
        self.errorDetail = error_detail
        self.invalidFields = invalid_fields

    @classmethod
    def from_json(cls, data):
        print(data)
        invalidFields = list(map(InvalidField.from_json, data["invalidFields"]))
        return cls(invalidFields)


def set_error(err_code, err_msg, nested_errs=None, err_msg_local=None, invalid_field=None, invalid_field_msg=None):
    n_error = []
    if nested_errs is not None:
        for nested_err in nested_errs:
            n_error.append(NestedError(error_code=nested_err))
    else:
        n_error.append(NestedError(error_code=None))

    if invalid_field is not None:
        error = BadRequestError(error_code=err_code,
                                error_detail=ErrorDetail(nested_errors=n_error,
                                                         message=err_msg,
                                                         message_local=err_msg_local),
                                invalid_fields=[InvalidField(field=invalid_field, msg=invalid_field_msg)])
    else:
        error = Error(error_code=err_code,
                      error_detail=ErrorDetail(nested_errors=n_error,
                                               message=err_msg,
                                               message_local=err_msg_local))

    return json.dumps(error, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def set_ok(pred):
    prediction = PredictionSuccess(pred)
    return json.dumps(prediction, default=lambda o: o.__dict__, indent=4)


def __400_failed_field_validation(field, field_msg, error=None):
    err_res = set_error(err_code=const.REQ_FAILED_VALIDATION,
                        err_msg=const.REQ_FAILED_VALIDATION_MSG,
                        nested_errs=[error],
                        invalid_field=field,
                        invalid_field_msg=field_msg)
    res_stat = RequestStatus(status_code=HTTPStatus.BAD_REQUEST, status_reason='Bad request')
    return err_res, res_stat


def __400_invalid_format(error):
    err_res = set_error(err_code=const.REQ_INVALID_FORMAT,
                        err_msg=const.REQ_INVALID_FORMAT_MSG,
                        nested_errs=[error])
    res_stat = RequestStatus(status_code=HTTPStatus.BAD_REQUEST, status_reason='Bad request')
    return err_res, res_stat


def __200_ok(res):
    res_stat = RequestStatus(status_code=HTTPStatus.OK, status_reason='Success')
    ok_res = set_ok(res)
    return ok_res, res_stat


def __500_error(error):
    err_res = set_error(err_code=const.REQ_SERVER_UNAVAILABLE,
                        err_msg=const.REQ_SERVER_UNAVAILABLE_MSG,
                        nested_errs=[error])
    res_stat = RequestStatus(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, status_reason='Internal server error')

    return err_res, res_stat


class RequestStatus:
    def __init__(self, status_code: int, status_reason: str):
        self.code = status_code
        self.reason = status_reason

