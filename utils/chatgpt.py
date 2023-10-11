import openai

class OpenAIHandler():
  def __init__(self, api_key, ai_model, output_file):
    openai.api_key = api_key
    self.model = ai_model
    self.output_file = output_file

  def do_threat_modeling(self, sentence):
    print("Processing your request, please wait...")
    context = "Generate Threats and their Preventive Measures"
    response = openai.ChatCompletion.create(model=self.model,
      messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": sentence}
      ]
    )
    result = response["choices"][0]["message"]["content"]
    print(result)
    if self.output_file:
      with open(self.output_file, "w") as f:
        f.write(result)