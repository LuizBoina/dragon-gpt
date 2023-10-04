import argparse
import os
from dotenv import load_dotenv
from utils.diagram import *
from utils.chatgpt import *

def handle_arguments():
  parser = argparse.ArgumentParser(description=
    "Dragon-GPT is a CLI program that makes an automatic threat analysis \
    using Chat-GPT on a given scenario produced using OWASP Threat Dragon.")
  parser.add_argument("filename", help="Path to the diagram (json format excepted)")
  parser.add_argument("--api_key", "-k", help="Pass the key as parameter or set it on .env file")
  parser.add_argument("--model", "-m", default="gpt-3.5-turbo", help="AI Model to be used by OpenAI API (default: gpt-3.5-turbo)")
  parser.add_argument("--output", "-o", help="Export the response from openai to a txt file")
  args = parser.parse_args()
  return args

if __name__ == "__main__":
  args = handle_arguments()
  diagram = DiagramHandler(args.filename)
  sentence = diagram.make_sentence()
  print(sentence)
  load_dotenv()
  openai_key = os.getenv("OPENAI_KEY")
  if openai_key == "":
    if args.api_key:
      openai_key = args.api_key
    else:
      print("OpenAI KEY needs to be informed. You can get yours from this link: ")
      print("https://platform.openai.com/account/api-keys")
      exit()
  chatgpt = OpenAIHandler(openai_key, args.model, args.output)
  response = chatgpt.do_threat_modeling(sentence)