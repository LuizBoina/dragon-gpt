import openai

class OpenAIHandler():
  def __init__(self, api_key, ai_model):
    openai.api_key = api_key
    self.model = ai_model

  def do_threat_modeling(self, sentence):
    print("Processing your request, please wait...")
    context = "Generate Threats and their Preventive Measures"
    try:
      response = openai.ChatCompletion.create(model=self.model,
        messages=[
          {"role": "system", "content": context},
          {"role": "user", "content": sentence}
        ]
      )
      response = response["choices"][0]["message  "]["content"]
      return response
    except (openai.error.RateLimitError, openai.error.InvalidRequestError) as error:
      print("You exceeded your current quota or used an invalid model.")