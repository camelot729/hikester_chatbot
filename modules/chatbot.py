from modules.translate import Translate
import pickle
from facts.facts import Model
from e.state import State


class Chatbot:

    def __init__(self, State, input_message):
        self.state = State.EMPTY_SECTION
        self.input_message = input_message
        self.language = 'en'
        self.translate_module = Translate()

    def proccess_request(self, user_request_str):
        try:
            with open('model.pkl'.format(20), 'rb') as input:
                model = pickle.load(input)
        except:
            with open('model.pkl'.format(20), 'wb') as output:
                model = Model()
                pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)
        self.state = model.check_section(user_request_str)
        return self.state
