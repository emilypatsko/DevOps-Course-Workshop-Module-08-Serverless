import logging
import uuid
import time
import json
import typing
import azure.functions as func


def main(request: func.HttpRequest, translation: func.Out[str], queuemsgs: func.Out[typing.List[str]]) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')
    start = time.time()

    rowKey = str(uuid.uuid4())    

    request_body = request.get_json()
    subtitle = request_body.get("subtitle")
    languages = request_body.get("languages")

    data = {
        "Name": subtitle,
        "PartitionKey": "translation",
        "RowKey": rowKey
    }

    translation.set(json.dumps(data))

    msgs = []
    for l in languages:
        msg = json.dumps({
            "rowKey": rowKey,
            "languageCode": l
        })
        msgs.append(msg)

    queuemsgs.set(msgs)    

    end = time.time()
    processingTime = end - start

    return func.HttpResponse(
        f"Processing took {str(processingTime)} seconds. Translation is: {subtitle}. Translation created with rowKey {rowKey}",
        status_code=200
    )
