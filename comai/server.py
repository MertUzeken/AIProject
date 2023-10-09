#!/usr/bin/env python3

import os
import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
#from setupGUI import *


import argparse


class ServerApp:
    def __init__(self, instance_choice=1):
        self.app = Flask(__name__)
        self.answer_history = []
        self.setup_routes()

        print("Choose a model by entering the number")

        if instance_choice == '1':
            import LChainTest
            self.instance = LChainTest.comai()
            print("Choice 1")
        elif instance_choice == '2':
            import privateGPT
            self.instance = privateGPT.privateGPT()
            print("choice 2")
        else:
            print("Choose a model by entering the number")

            while True:
                print("1. ComAI")
                print("2. GPT4all (privateGPT)")
                choice = input()

                if choice == '1':
                    import LChainTest
                    self.instance = LChainTest.comai()
                    break
                elif choice == '2':
                    import privateGPT
                    self.instance = privateGPT.privateGPT()
                    break
                else:
                    print("Wrong choice")


    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', answer_history=self.answer_history)

        @self.app.route('/getQuestions')
        def getList():
             return self.readQuestionList()

        @self.app.route('/sendRequest', methods=['POST'])
        def send_request():
            received_string = request.json['message']
            response = self.instance.sendToGPT(received_string)
            question = response['question']
            answer = response['answer']
            return jsonify(response=answer)
        
        #For user feedback, experimental.
        @self.app.route('/sentToSupport', methods=['POST'])
        def sent_to_support():
            message = request.json['message']
            try:
                df = pd.read_excel('SupportMessages.xlsx')
            except FileNotFoundError:
                df = pd.DataFrame(columns=['Message', 'Bearbeitet?'])
                df = df.append({'Message': message}, ignore_index=True)
                df.to_excel('SupportMessages.xlsx', index=False)
                return 'Message saved to Excel file', 200
            
    #Read questions for the navbar from a excel file.
    def readQuestionList(self) -> list:
        json = ''
        try:
            df = pd.read_excel('PDFStore/questions.xlsx')
            json = df.to_json(orient="records")
            return json
            
        except FileNotFoundError:
            print("The questions.xlsx file could not been found.")
        
    

    def run(self):
        port = int(os.environ.get("PORT", 9000))
        host = '127.0.0.1' #config['ip']
        # Change debug to True for hot reloading
        CORS(self.app, origins=["http://localhost:8080"])
        self.app.run(host=host, port=port, debug=False)
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start the server with a model choice.")
    parser.add_argument('-m', '--model', type=str, help='Model choice: 1 for ComAI, 2 for GPT4all. If not provided, will ask interactively.')

    args = parser.parse_args()
    server = ServerApp(args.model)
    server.run()
