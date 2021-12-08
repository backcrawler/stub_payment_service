import logging

logging.config.fileConfig('./stub_payment_service/loggers/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('root')
