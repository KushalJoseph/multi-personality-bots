import os
import logging
import uuid
import asyncio
from flask import Flask
from flask import request
from rasa.core.agent import Agent

logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')

def __create_agent(lang):
    model_path = './models/model-{}.tar.gz'.format(lang)
    return Agent.load(model_path=model_path)
    
agents = {
    "hindi": __create_agent("hindi"),
    "en": __create_agent("en"),
    "es": __create_agent("es")
}

loop = asyncio.get_event_loop()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def user_uttered():
    print(request.json)
    sid = str(request.json.get('sid'))
    message = str(request.json.get('message'))
    lang = str(request.json.get('lang', 'en'))
    agent = agents.get(lang, 'Language {} is not supported'.format(lang))
    bot_response = loop.run_until_complete(
        agent.parse_message_using_nlu_interpreter(message_data = message)
    )
    #return ', '.join(map(str, bot_response))
    return bot_response

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host, port, debug=False, use_reloader=False)
