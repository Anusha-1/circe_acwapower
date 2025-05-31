"""
acwa.log.format

Format logging
"""

import logging

def format_basic_logging(config: dict):
    """
    Formats basic logging

    Args:
        config (dict): Configuration of log (under 'log' section)
    """

    handlers=[
        logging.StreamHandler()
    ]

    if config.get('file', None) is not None:
        handlers.append(logging.FileHandler(config['file']))

    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        level=getattr(logging, config.get('level', 'INFO')),
        handlers=handlers
    )