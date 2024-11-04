from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FileLogger:
    def __init__(self, file, disabled=False):
        self.file = file
        self.disabled = disabled
        if self.disabled:
            logger.debug("FileLogger disabled.")

    def append(self, data, timestamp=False):
        if self.disabled:
            return
        with open(self.file, "a") as f:
            dt = ""
            if timestamp:
                dt = f"{datetime.now()}\t"
            f.write(f"{dt}{data}\n")
