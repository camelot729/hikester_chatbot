#pip install yandex.translate

from yandex_translate import YandexTranslate

key = YandexTranslate('trnsl.1.1.20180216T133517Z.9eb599729cc6f038.adb96ddcd04c34e7cae27de0693a36930d6b1c08')

class Translate:

    def __init__(self):
        self.translator = key
#en-ru or ru-en

    def translate(self, text, source_lang, dest_lang):
        json = self.translator.translate(text, source_lang + "-" + dest_lang)
        text = json["text"][0]
        return text

    def define(self, query):
        lang = self.translator.detect(query)
        return lang
