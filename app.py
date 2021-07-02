import os
import logging
import uuid
import asyncio
from flask import Flask
from flask import request
from rasa.core.agent import Agent
#from waitress import serve


logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')

def __create_agent(game):
    model_path = './models/model-{}.tar.gz'.format(game)
    return Agent.load(model_path=model_path)

agents = {
    "en": __create_agent("en"),
    "es": __create_agent("es"),
    "kushal": __create_agent("kushal"),
    "vishnu": __create_agent("vishnu"),
    "mayank": __create_agent("mayank")
}

loop = asyncio.get_event_loop()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def user_uttered():
    print(request.json)
    sid = str(request.json.get('sid'))
    message = str(request.json.get('message'))
    game = str(request.json.get('game'))
    agent = agents.get(game)
    bot_response = loop.run_until_complete(
        agent.parse_message_using_nlu_interpreter(message_data=message)
        #agent.handle_text(text_message=message, sender_id=sid)
    )
    print(bot_response)
    #return ', '.join(map(str, bot_response))
    return bot_response

if __name__ == '__main__':
	#serve(app, host = "0.0.0.0", port = 8080)
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host, port, debug=False, use_reloader=False)
    
    
    
    
    
##
