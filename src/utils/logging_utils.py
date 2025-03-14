# src/utils/logging_utils.py
import logging
import sys
from datetime import datetime
import os

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Set up a logger with a specific name, log file, and level
    
    Args:
        name (str): Logger name
        log_file (str, optional): File to save logs to. Defaults to None.
        level (int, optional): Logging level. Defaults to logging.INFO.
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if not exists and log_file is specified
    if log_file and not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers = []
    
    # Create console handler and set level
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # If log file is specified, add file handler
    if log_file:
        if not log_file.startswith('logs/'):
            log_file = f'logs/{log_file}'
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_timestamped_logger(name, prefix='log', level=logging.INFO):
    """
    Get a logger with a timestamped log file
    
    Args:
        name (str): Logger name
        prefix (str, optional): Log file prefix. Defaults to 'log'.
        level (int, optional): Logging level. Defaults to logging.INFO.
        
    Returns:
        logging.Logger: Configured logger with timestamped log file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"{prefix}_{timestamp}.log"
    return setup_logger(name, log_file, level)