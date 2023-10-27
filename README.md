<p align="center">
  <img src="./img/logo.png">
  <p align="center">An automatic OpenAI-powered threat modeling analysis based on OWASP Threat Dragon diagram</p>
  <p align="center">
    <a href="/LICENSE.md">
      <img src="https://img.shields.io/badge/license-MIT-blue.svg">
    </a>
  </p>
</p>

---

## General Updates

- [Update on 27/10/23] Add Support to Local LLM, the Llama 2, so you don't need to have a OpenAI account and even credits on that. The results using Llama may be inferior and slower then to ChatGPT but at least it's free. :grin:

### Summary

Dragon-GPT is an AI-powered tool that automatically does the threat modeling analysis on the diagram made using the OWASP Threat Dragon modeling software. It uses the OpenAI API, so you need to have a valid account for their tokens to use on each program call, and the JSON file generated when you save/export an OWASP Threat Dragon project (generally saved in td.vue folder).

The program itself is pretty simple, it extracts every relevant information on the JSON file, like the diagram model and components used on the modeling, and transforms it into a human-readable sentence. After that, the sentence is send via OpenAI API, and the result of the analysis is printed. By default, it uses `chatgpt-3.5-turbo` but you can change that via parameter to another model like the `chatgpt-4`.

---

### Download and install

```bash
  # Download the project
  $ git clone https://github.com/LuizBoina/dragon-gpt.git && cd dragon-gpt
    
  # Install deps (Developed using Python 3.10)
  $ pip install -r requirements.txt

  # Set OPENAI_KEY variable on .env file (Required only when using chatgpt)
  OPENAI_KEY=<your_openai_key>

  # Run using ChatGPT
  $ python main.py diagram/basic_scenario.json

  # To run using local LLM (Llama 2) you need to install python3-dev:
  $ apt install python3-dev

  # You will also need a model that can be find on https://huggingface.co/TheBloke/Llama-2-7B-GGUF/tree/main
  # or just skip this step to install automatically the default used in this project, the llama-2-7b.Q8_0.gguf.
  # This recommended model uses 7Gb or disk and 10GB of RAM when running.
  # Model should be placed on /utils/local_llm/model

  # Run using Llama 2
  $ python main.py -l diagram/basic_scenario.json
```
---

### Usage:
```
usage: main.py [-h] [--api_key API_KEY] [--model MODEL] [--output OUTPUT] [--use_local_llm] [--n_ctx N_CTX] filename

Dragon-GPT is a CLI program that makes an automatic threat analysis using Chat-GPT on a given scenario produced using OWASP Threat Dragon.

positional arguments:
  filename              Path to the diagram (json format expected)

options:
  -h, --help            show this help message and exit
  --api_key API_KEY, -k API_KEY
                        Pass the key as a parameter or set it in .env file
  --model MODEL, -m MODEL
                        AI Model to be used by OpenAI API (default: gpt-3.5-turbo)
  --output OUTPUT, -o OUTPUT
                        Export the response from OpenAI to a txt file
  --use_local_llm, -l   Set to true if you want to use a local LLM
  --n_ctx N_CTX, -c N_CTX
                        (Recommended when using local LLM) Number of tokens the LLM uses for context, generally high numbers (>2048) gives longer
                        responses but takes more time.
```

---

### Contribution

As an open-source project, feel welcome to open a pull request to improve this project or ask a question and I'll help you as soon as possible.

---

### License

This work is licensed under [MIT License.](/LICENSE.md)
