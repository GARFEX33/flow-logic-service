import structlog
import logging
from src.config.settings import LOG_LEVEL

def configure_structlog():
    logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    logger = structlog.get_logger()
    logger.info("Structlog configured successfully")