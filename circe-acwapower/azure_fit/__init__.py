import logging
import azure.functions as func

import acwa.scripts as scripts

logging.basicConfig(level=logging.INFO)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    try:
        # Intentamos capturar el parámetro "name" de la query string
        n_samples = req.params.get('n_samples')
        if not n_samples:
            try:
                req_body = req.get_json()
                n_samples = req_body.get('n_samples')
            except ValueError:
                logging.warning("No value for n_samples found")
                n_samples = None

        scripts.fit_quantiles(n_samples=n_samples)

        return func.HttpResponse("Models fitted")       

    
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        return func.HttpResponse(
            "An error occurred",
            status_code=500
        )
