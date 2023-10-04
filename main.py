import argparse
from utils.diagram import *

def handle_arguments():
    parser = argparse.ArgumentParser(description=
        "Dragon-GPT is a CLI program that makes an automatic threat analysis \
        using Chat-GPT based on a given scenario construted using OWASP Threat Dragon.")
    parser.add_argument("filename", help="Path to the diagram (json format excepted)")
    args = parser.parse_args()
    return args.filename

if __name__ == "__main__":
    filename = handle_arguments()
    diagram = DiagramHandler(filename)
    sentence = diagram.make_sentence()
    print(sentence)
    