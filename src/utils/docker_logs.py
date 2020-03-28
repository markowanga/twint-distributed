import logging

loggers = dict()


def get_logger(mod_name):
    if mod_name in loggers:
        return loggers[mod_name]
    else:
        logger = logging.getLogger(mod_name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(name)-30s] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        for it in logger.handlers:
            logger.removeHandler(it)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        loggers[mod_name] = mod_name
        return logger
