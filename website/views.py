from flask import Blueprint, Response, render_template, request, session, url_for, send_file
from website.connections.openai_connection import OpenAIConnection
from website.connections.azure_conection import AzureConnection
import os
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/newconversation', methods=['GET', 'POST'])
def new_conversation():
    if 'conversation' not in session:
        session['conversation'] = {}
        session['json'], session['final_json'] = OpenAIConnection.initialize()
        session['question'] = "What's your name?"

    conversation = session['conversation']
    json = session['json']
    final_json = session['final_json']
    question = session['question']

    if request.method == 'POST':
        answer = request.form['answer']

        conversation, json, final_json, question = OpenAIConnection.conversation(conversation, json, final_json, question, answer)

        session['conversation'] = conversation
        session['json'] = json
        session['final_json'] = final_json
        session['question'] = question
        
        flag = False
        if question == "Thanks for your time." and not flag:
            flag = True
            print(conversation)
            print(json)
            paragraph = OpenAIConnection.create_paragraph(final_json)
            audio_data = AzureConnection.text_to_speech(paragraph)
            if audio_data:
                audio_path = os.path.join('static', 'audio', 'output.wav')
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)
                with open(audio_path, 'wb') as audio_file:
                    audio_file.write(audio_data)
                return render_template('conversation/newconversation.html', user=current_user,   conversation=conversation, question=question, audio_url=url_for('static', filename='audio/output.wav'))

        return render_template('conversation/newconversation.html', user=current_user, conversation=conversation, question=question)
    
    else:
        session.pop('conversation', None)
        session.pop('json', None)
        session.pop('final_json', None)
        session.pop('question', None)
        question = "What's your name?"
        '''question = "Thanks for your time."
        flag = False
        if question == "Thanks for your time." and not flag:
            flag = True
            paragraph = "sergio prueba"
            audio_data = AzureConnection.text_to_speech(paragraph)
            if audio_data:
                audio_path = os.path.join('static', 'audio', 'output.wav')
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)
                with open(audio_path, 'wb') as audio_file:
                    audio_file.write(audio_data)
                return render_template('conversation/newconversation.html', conversation=conversation, question=question, audio_url=url_for('static', filename='audio/output.wav'))
        '''
        return render_template('conversation/newconversation.html', user=current_user, conversation={}, question=question)
