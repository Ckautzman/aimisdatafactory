import azure.functions as func
import logging
import json
import datetime
from fogo_scraper import get_all_locations

def main(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the Fogo de Chao locations
        locations = get_all_locations()
        
        if not locations:
            return func.HttpResponse(
                "No locations were found",
                status_code=404
            )

        # Create output data with timestamp
        output_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "locations": locations
        }

        # Convert to JSON string
        json_data = json.dumps(output_data, indent=2)
        
        # Write to blob storage
        outputblob.set(json_data)

        return func.HttpResponse(
            f"Successfully processed {len(locations)} locations. Data written to blob storage.",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        ) 