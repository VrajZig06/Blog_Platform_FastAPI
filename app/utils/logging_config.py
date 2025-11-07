import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Define log file paths
main_log_file = os.path.join(logs_dir, "braintrain.log")
error_log_file = os.path.join(logs_dir, "errors.log")
debug_log_file = os.path.join(logs_dir, "debug.log")  # New file for debug logs


def configure_logger(name=None):
    """
    Configure and return a logger with the given name.
    
    Args:
        name: The logger name, typically __name__ from the calling module
        
    Returns:
        A configured logger instance
    """
    # Get logger with the given name, or root logger if None
    logger = logging.getLogger(name)
    
    # Only configure if logger doesn't already have handlers
    if not logger.handlers:
        # Set level and propagation
        logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logging
        logger.propagate = False
        
        # Create formatters
        standard_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        verbose_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
        )
        
        # Console handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(standard_formatter) 
        
        # File handler for all logs (rotating, max 10MB per file, 5 backup files)
        file_handler = RotatingFileHandler(
            main_log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG) 
        file_handler.setFormatter(standard_formatter)
        
        # Debug file handler for detailed logs
        debug_handler = RotatingFileHandler(
            debug_log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(standard_formatter)
        
        # File handler for errors only
        error_handler = RotatingFileHandler(
            error_log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(verbose_formatter)
        
        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(debug_handler)  # Add the debug handler
        logger.addHandler(error_handler)
        
        # Configure third-party loggers to reduce noise
        # Keep most third-party loggers at INFO level
        for module in [
            'urllib3.connectionpool',
            'httpx',
            'msal',
            'PIL'
        ]:
            logging.getLogger(module).setLevel(logging.INFO)
            
        # Set Azure SDK loggers to ERROR level to prevent detailed HTTP logging
        azure_loggers = [
            'azure.storage.blob',
            'azure.core.pipeline.policies.http_logging_policy',
            'azure.storage.blob._shared',
            'azure.identity',
            'azure'  # Parent logger for all Azure modules
        ]
        for module in azure_loggers:
            logging.getLogger(module).setLevel(logging.ERROR)
    
    return logger 