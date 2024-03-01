from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . models import Note
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required # cannot accesc home page until u login
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash(" Note is short", category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id: # check if current user is own this note
            db.session.delete()
            db.session.commit()
        
    return jsonify({})