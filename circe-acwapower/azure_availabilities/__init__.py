import azure.functions as func
import logging

import acwa.scripts as scripts

def main(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info("Running inner function")
    scripts.update_availabilities()