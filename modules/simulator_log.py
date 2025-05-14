# modules/simulator_log.py

import logging
import os

# Ensure the logs folder exists
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Set up logging configuration to save logs in the logs folder
logging.basicConfig(
    filename=os.path.join(log_folder, 'simulator.log'),  # Logs saved in the 'logs/simulator.log' file
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_simulation(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
