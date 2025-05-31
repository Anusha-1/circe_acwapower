import logging
import azure.functions as func

import acwa.scripts as scripts

logging.basicConfig(level=logging.INFO)

def main(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    scripts.fit_quantiles(
        n_samples=200000)
