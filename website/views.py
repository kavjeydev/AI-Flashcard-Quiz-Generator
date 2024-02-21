# takes care of URL stuff for website
from openai import OpenAI

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Flashcard
from . import db
import json


# means we have a bunch of URLs defined in here (this is what a blueprint is)
def process_output(flashcards):
    front = []
    back = []

    split_flashcards = flashcards.split(' ')
    print("split_flashcards", split_flashcards)

    front_string = ""
    back_string = ""
    front_bool = True
    for i in range(len(split_flashcards)):
        if split_flashcards[i] == "Front:":
            if i > 0:

                back.append(back_string)
                back_string = ""
            front_bool = True
            continue
        if split_flashcards[i] == "Back:":

            front.append(front_string)
            front_string = ""
            front_bool = False
            continue
        if front_bool:
            front_string += split_flashcards[i] + " "
        if not front_bool:
            back_string += split_flashcards[i] + " "
    
    back.append(back_string)

    print("front", front)
    print("back", back)
    return front, back
        

client = OpenAI(api_key="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")
views = Blueprint('views', __name__) # setup blueprint for our flask app

@views.route('/', methods=['GET', 'POST']) # takes us to our main page, whenever we hit this route, the function below will run
@login_required # cannot get to home page unless we're logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if(len(note) < 1):
            flash('Note is too short.', category='error')
        else:

            stream = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": f"Make flashcards with this content, don't number flashcards and label the front and back: {note}"}],
                stream=True,
            )


            data_string = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    data_string += (chunk.choices[0].delta.content) 


            new_data_string = ""
            for i in range(len(data_string)):
                if data_string[i] == '\n':
                    new_data_string += ' '
                else:
                    new_data_string += data_string[i]

            front_of_flashcard, back_of_flashcard = process_output(new_data_string)


            print("here", back_of_flashcard)
            new_note = Note(data=data_string, user_id=current_user.id)
            for i in range(len(front_of_flashcard)):
                print("here")
                new_flashcard = Flashcard(front=front_of_flashcard[i], back=back_of_flashcard[i], user_id=current_user.id)
                db.session.add(new_flashcard)
            db.session.add(new_note)
            db.session.commit()
            flash('Note processed.', category='success')
            return redirect(url_for('views.flashcards'))
    return render_template("home.html", user=current_user) # just returns some HTML code

@views.route('/flashcards', methods=['GET', 'POST']) # takes us to our main page, whenever we hit this route, the function below will run
@login_required
def flashcards():
    return render_template("flashcards.html", user=current_user)
        

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if(note.user_id == current_user.id):
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/delete-card', methods=['POST'])
def delete_card():
    card = json.loads(request.data)
    cardID = card['flashID']
    card = Flashcard.query.get(cardID)

    if card:
        if(card.user_id == current_user.id):
            db.session.delete(card)
            db.session.commit()
    
    return jsonify({})

