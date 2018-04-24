from facts.facts import Model
from modules.chatbot import Chatbot


def start():
    print("Let's go")
    qwe = Chatbot

    q = Chatbot.proccess_request("How much it costs?")
    return qwe


if __name__ == "__main__":
    start()
