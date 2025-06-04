import os
import requests

class LlamaHandler:
  def __init__(self, n_ctx=None, backend="ollama", model=None, base_url=None):
    self.backend = backend
    self.n_ctx = n_ctx

    if backend == "ollama":
      from langchain.chat_models import init_chat_model
      self.config = {
        "model": model,
        "base_url": base_url,
      }
      if n_ctx:
        self.config["context_window"] = int(n_ctx)
      self.llm = init_chat_model(**self.config)

    elif backend == "llama_cpp":
      from llama_cpp import Llama
      self.model_path = "./utils/local_llm/model/"
      self.n_ctx = n_ctx
      if not os.listdir:
        self.__download_model()
      else:
        self.model_path = self.model_path + os.listdir(self.model_path)[0]
      if n_ctx:
        self.llm = Llama(model_path=self.model_path, n_ctx=int(n_ctx))
      else:
        self.llm = Llama(model_path=self.model_path)
    else:
        raise ValueError("Unsupported backend: choose 'ollama' or 'llama_cpp'.")

  def __download_model(self):
    print("---=== * * * ===---")
    print("Downloading llama-2-7b-chat.ggmlv3.q8_0.bin model, it may take a while (size: 7Gb)")
    url = "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/blob/main/llama-2-7b.Q8_0.gguf"
    file_name = os.path.basename(url)
    file_path = os.path.join(self.model_path, file_name)
    # Rename from folder to model filename + path
    self.model_path = file_path
    try:
      response = requests.get(url)
      if response.status_code == 200:
        with open(file_path, 'wb') as file:
          file.write(response.content)
          print(f"Model '{file_name}' downloaded.")
      else:
        print(f"Failed to download the model. Status code: {response.status_code}")
        print("You may prefer downloading it manually and then putting it in ./utils/local_llm/model folder")
        exit()
    except Exception as e:
      print(f"Error downloading the model: {e}")
      print("You may prefer downloading it manually and then putting it in ./utils/local_llm/model folder")
      exit()

  def do_threat_modeling(self, sentence):
    prompt = "Q: " + sentence
    print("Processing your request, please wait...")
    if self.backend == "ollama":
      response = self.llm.invoke(prompt)
      return response.content if hasattr(response, "content") else str(response)
    elif self.backend == "llama_cpp":
      if self.n_ctx:
        response = self.llm(prompt, max_tokens=0)
      else:
        response = self.llm(prompt)
        return response["choices"][0]["text"]
