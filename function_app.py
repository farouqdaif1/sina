import azure.functions as func
import logging
import json
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="define_words")
def define_words(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        return func.HttpResponse(
            json.dumps({
                "error_message": "Please provide a query parameter",
                "status": "error"
            }),
            status_code=400,
            mimetype="application/json"
        )

    query = query.split(" ")

    definitions = []

    for word in query:
        api_url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"

        response = requests.get(api_url, headers={\
            "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
            "x-rapidapi-key" : "Y3PZ2XdXqHmshgbfl2LK5rVYqI3gp1ewQXijsnWMKNjUX86NtO",
        })

        if response.status_code == 200:
            word_data = response.json()
            if word_data:
                definitions.append(word_data)
        else:
            definitions.append({
                "word": word,
                "definitions": []
            })

    return func.HttpResponse(
        json.dumps(definitions),
        mimetype="application/json"
    )