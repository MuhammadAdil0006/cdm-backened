"""Settings module for white_label."""

import logging

from AiMapper.settings.base import *

logger = logging.getLogger(__name__)

try:
    from AiMapper.settings.local import *
except ModuleNotFoundError:
    logger.warning('Local settings file not initialized yet.')
