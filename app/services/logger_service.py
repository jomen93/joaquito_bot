import os
import logging
from datetime import datetime
from typing import Optional


class LoggerService:
    _instance = None

    def __new__(cls, log_dir="logs", log_file=None):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance._initialize(log_dir, log_file)
        return cls._instance

    def _initialize(self, log_dir: str, log_file: str):
        """
        Init the logging service 

        Args:
        -----
            log_dir (str): Directory to save the logs
            log_file (str): Name of log file. If is None, is automatically generated
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if log_file is None:
            log_file = f"log_{datetime.now().strftime('%Y%m%s_%H%M%S')}.log"

        log_path = os.path.join(log_dir, log_file)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger("LoggerService")
        self.default_context = {
            "session": "N/A",
            "symbol": "N/A",
            "risk": "N/A",
            "event": "N/A"
        }

    def set_context(
        self, session: Optional[str] = None,
        symbol: Optional[str] = None,
        risk: Optional[str] = None,
        event: Optional[str] = None):
        """
        Set default context for the logger.

        Args:
        -----
            session (str): Identifier for the session.
            symbol (str): Symbol being analyzed.
            risk (str): Risk level (if applicable).
            event (str): Event description.
        """
        if session:
            self.default_context["session"] = session
        if symbol:
            self.default_context["symbol"] = symbol
        if risk:
            self.default_context["risk"] = risk
        if event:
            self.default_context["event"] = event

    def log(self, level: str, message: str):
        """
        Add a record in the log.

        Args:
        -----
            level (str): Level log ('INFO', 'WARNING', 'ERROR', ...)
            message (str): Log message
        """
        if level.upper() == "INFO":
            self.logger.info(message)
        elif level.upper() == "WARNING":
            self.logger.warning(message)
        elif level.upper() == "ERROR":
            self.logger.error(message)
        elif level.upper() == "DEBUG":
            self.logger.debug(message)
        else:
            self.logger.info(f"UNKNOWN LEVEL: {message}")
