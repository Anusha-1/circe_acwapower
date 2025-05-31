import azure.functions as func
import logging

import acwa.scripts as scripts

def main(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info("Collect 10 min data")
    scripts.collect_10min()

    logging.info("Collect alarms")
    scripts.collect_alarms()
    