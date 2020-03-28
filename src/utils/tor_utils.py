import time

import requests

import utils.command_utils as command_utils
import utils.docker_logs as docker_logs

logger = docker_logs.get_logger('tor_utils')


def _start_tor():
    logger.info('start tor proxy')
    command_utils.run_bash_command('tor &')
    return


def _wait_until_tor_works():
    logger.info('wait until tor works')
    code = ''
    while code != '200':
        try:
            logger.info('tor check request')
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            r = requests.get('http://jsonip.com/', proxies=proxies)
            code = str(r.status_code)
            logger.info('response_code: ' + code)
        except Exception as err:
            logger.error(err)
            logger.info('not works yet, waiting..')
            time.sleep(2)
    logger.info('tor works')
    return


def prepare_tor():
    _start_tor()
    _wait_until_tor_works()
    return
