import azure.functions as func
import logging
import openai
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="chat")
def HttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    default_credential = DefaultAzureCredential()
    token = default_credential.get_token(
        "https://cognitiveservices.azure.com/.default")

    api_subscption_key = "your api subscription key"

    openai.api_type = "azure"
    # APIM Endpoint
    openai.api_version = "2023-07-01-preview"

    # DO NOT USE ACTUAL AZURE OPENAI SERVICE KEY
    openai.api_key = api_subscption_key
    openai.api_base = "https://apim-emt-aip-dev-01.azure-api.net/"
    response = openai.ChatCompletion.create(deployment_id="gpt-35-16",
                                            messages=[
                                                {"role": "system",
                                                    "content": "You are a helpful assistant."},
                                                {"role": "user",
                                                    "content": "Knock knock."},
                                                {"role": "assistant",
                                                    "content": "Who's there?"},
                                                {"role": "user",
                                                    "content": "Orange."},
                                            ],
                                            temperature=0,
                                            headers={
                                                'Authorization': f'{token}',
                                                'ocp-apim-subscription-key': f'{api_subscption_key}'
                                            }
                                            )
    return func.HttpResponse(f"{response.choices[0].message.role}: {response.choices[0].message.content}")
