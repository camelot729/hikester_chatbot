from modules.chatbot import Chatbot
from e.state import State
from http.server import  HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from facts.facr_generator import FactGenerator
from firebase.firebase import FirebaseService

from geopy.geocoders import Nominatim

class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed_path = urlparse(self.path)
        if parsed_path.query == '':
            return

        params = parsed_path.query

        arr_param = params.split('&')

        #user request
        text_param = arr_param[0].split('=')[1]
        text_param = text_param.split('_')

        chat_id_param = arr_param[1].split('=')[1]

        user_id_param = arr_param[2].split('=')[1]

        #firebase init

        params = ''
        for par in text_param:
            params += par + ' '

        #write user message to firebase
        FirebaseService.send_message_by_user(chat_id_param, user_id_param, params)



        # print('1', type(params))
        # print('2',par_array)
        # print('3',params)
        result = start(params)
        message = result.value
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(message))
        self.wfile.write(str.encode(' ' + params))
        if message == 'fact':
            model = FactGenerator()
            print( model.best_fact(params)[0])
            self.wfile.write(str.encode(' ' + model.best_fact(params)[0]))
            answer = 'Take some facts about it, dude. ' + str(model.best_fact(params)[0])
            FirebaseService.send_message_by_bot(chat_id_param, user_id_param, answer)
        # take id
        #KyDmJ0Rt6HtoimcmVup
        # if not FirebaseService.apps.length:

        if message == 'cost':
            cost = FirebaseService.get_cost_by_id(chat_id_param)
            print('4' , type(cost))
            answer = 'Event cost: ' + cost
            self.wfile.write(str.encode(answer))
            FirebaseService.send_message_by_bot(chat_id_param, user_id_param, answer)

        if message == 'place':
            se = FirebaseService.get_place_by_id(chat_id_param)
            geolocator = Nominatim(scheme='http')
            print(str(se[0]) , str(se[1]))
            location = geolocator.reverse((str(se[0]),str(se[1])))
            answer = 'Event place are : ' + location.address
            self.wfile.write(str.encode(answer))
            FirebaseService.send_message_by_bot(chat_id_param, user_id_param, answer)

        if message == 'time':
            time = FirebaseService.get_time_by_id(chat_id_param)
            print(str(time))
            time_date = '' + str(time.date())
            print(type(time_date))
            answer = 'Event time at ' + str(time.hour + 3) + ' ' + str(time.minute)
            self.wfile.write(str.encode(answer))
            FirebaseService.send_message_by_bot(chat_id_param, user_id_param, answer)
        return


def start(string):
    print("Let's go")
    qwe = Chatbot(State.EMPTY_SECTION, string)
    q = qwe.proccess_request(string)
    print(q)
    return q

def main(port):
    try:
        server = HTTPServer(('', int(port)), MainHandler)
        print('started httpserver...')
        FirebaseService.init()
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

main(8005)