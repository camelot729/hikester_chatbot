import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import calendar

import datetime

import numpy as np


class FirebaseService:

    MAX_DISTANCE = 4000

    @staticmethod
    def init():
        # Use a service account
        cred = credentials.Certificate('../data/serviceAccount.json')
        firebase_admin.initialize_app(cred)

        FirebaseService.db = firestore.client()

    @staticmethod
    def get_by_id(id = ''):
        events_ref = FirebaseService.db.collection('events').document(id)
        docs = events_ref.get().to_dict()
        result = [{
            'lat': docs["lat"],
            'lng': docs["lng"],
            'time': docs["start_date"],
            'cost': docs["cost"]
        }]
        return result

    @staticmethod
    def get_time_by_id(id = ''):
        events_ref = FirebaseService.db.collection('events').document(id)
        docs = events_ref.get().to_dict()
        result = [{
            'time': docs["start_date"]
        }]
        return result[0]['time']

    @staticmethod
    def get_place_by_id(id = ''):
        events_ref = FirebaseService.db.collection('events').document(id)
        docs = events_ref.get().to_dict()
        result = [{
            'lat': docs["lat"],
            'lng': docs["lng"]
        }]
        return [result[0]['lat'],result[0]['lng']]

    @staticmethod
    def get_cost_by_id(id = ''):
        events_ref = FirebaseService.db.collection('events').document(id)
        docs = events_ref.get().to_dict()
        result = [{
            'cost': docs["cost"]
        }]
        return result[0]['cost']


        #/events/-KyDmJ0Rt6HtoimcmVup/users/2jUGSMPgAodGxN4lZ8fh/chat_bot_messages/B7OLPVXLJ0MWHewxPXQl/message/n954GKDP9XLcxU7gSNUd
    @staticmethod
    def send_message_by_user(event_id, user_id, mess):
        result = []
        events_ref = FirebaseService.db.collection('events').document(event_id).collection('users').document(user_id).collection('chat_bot_messages').get()
        chat_bot_id = ''
        for doc in events_ref:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
            print(doc.id)
            chat_bot_id = doc.id

        message_text = {
            'from': '1',
            'message': mess,
            'date' : datetime.datetime.now()
        }
        events_ref = FirebaseService.db.collection('events').document(event_id).collection('users').document(
            user_id).collection('chat_bot_messages').document().set(message_text)

        return
    @staticmethod
    def send_message_by_bot(event_id, user_id, mess):
        result = []
        events_ref = FirebaseService.db.collection('events').document(event_id).collection('users').document(user_id).collection('chat_bot_messages').get()
        chat_bot_id = ''
        for doc in events_ref:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
            print(doc.id)
            chat_bot_id = doc.id

        message_text = {
            'from': '2',
            'message': mess,
            'date' : datetime.datetime.now()
        }
        events_ref = FirebaseService.db.collection('events').document(event_id).collection('users').document(
            user_id).collection('chat_bot_messages').document().set(message_text)


        return



# if __name__ == '__main__':
#     FirebaseService.init()
#     FirebaseService.send_message_by_user('-KyDmJ0Rt6HtoimcmVup' , '2jUGSMPgAodGxN4lZ8fh')
