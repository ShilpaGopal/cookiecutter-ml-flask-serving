import string

MODEL_NAME: str = '<MODEL-NAME>'


SVC_NAME: str = '<SERVICE-NAME>'  # e.g: CRNN-inference-service
SVC_SHORT_NAME: str = '<SERVICE-SHORT-NAME>'  # e.g: CIS

REQ_INVALID_FORMAT = SVC_SHORT_NAME+'-VAL-101'
REQ_INVALID_FORMAT_MSG = 'invalid format'
REQ_FAILED_VALIDATION = SVC_SHORT_NAME+'-VAL-102'
REQ_FAILED_VALIDATION_MSG = 'failed field validation'
REQ_SERVER_UNAVAILABLE = 'SystemUnavailable'
REQ_SERVER_UNAVAILABLE_MSG = 'the server encountered an error'

PREDICT_ERROR_EVENT = SVC_SHORT_NAME + 'PredictErrorEvent'
PREDICT_SUCCESS_EVENT = SVC_SHORT_NAME + 'PredictSuccessEvent'
PREDICT_WARNING_EVENT = SVC_SHORT_NAME + 'PredictWarningEvent'
