import argparse
import os
from dotenv import load_dotenv
from utils.diagram import DiagramHandler
from utils.chatgpt import OpenAIHandler

def handle_arguments():
    parser = argparse.ArgumentParser(description=
        "Dragon-GPT is a CLI program that makes an automatic threat analysis "
        "using Chat-GPT on a given scenario produced using OWASP Threat Dragon.")
    parser.add_argument("filename", help="Path to the diagram (json format expected)")
    parser.add_argument("--api_key", "-k", help="Pass the key as a parameter or set it in .env file")
    parser.add_argument("--model", "-m", default="gpt-3.5-turbo", help="AI Model to be used by OpenAI API (default: gpt-3.5-turbo)")
    parser.add_argument("--output", "-o", default="output.txt", help="Export the response from OpenAI to a txt file")
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

    for comp in diagram.components:
        if comp["type"] == DiagramHandler.flow_type:
            for flow in comp["flow"]:
                if "preventive_measures" in flow:
                    response += f"\nPreventive measures for {flow['name']}: {flow['preventive_measures']}"

    print(response)
