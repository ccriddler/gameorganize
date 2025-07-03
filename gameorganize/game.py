from .db import db
from .forms.game import GameEntryForm
from .model.game import GameEntry
from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user

game = Blueprint('game', __name__, template_folder='templates')

@game.route("/<id>", methods=['GET'])
def detail(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    abort(404)

  _game_form = GameEntryForm()
  _game_form.from_game(game=_game)

  return render_template(
    'game/detail.html',
    game=_game,
    form=_game_form,
  )

@game.route("/<id>", methods=['POST'])
@login_required
def update(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    abort(404)

  if(_game.user_id != current_user.id):
    abort(403)

  form = GameEntryForm(request.form)
  form.from_user(user=_game.user)

  try:
    if(not form.validate()):
      raise ValueError(f"Form validation failed! {form.errors}")

    form.to_game(_game)

    db.session.commit()
  except Exception as e:
    flash(f"DB Error: {e}")
    return redirect(url_for('game.detail', id=id))

  flash(f"Updated game: '{_game.name}'")
  return redirect(url_for('game.detail', id=id))

@game.route("/<id>/delete", methods=['POST'])
@login_required
def delete(id):
  _game = db.session.get(GameEntry, id)

  if(not _game):
    abort(404)

  if(_game.user_id != current_user.id):
    abort(403)

  db.session.delete(_game)
  db.session.commit()

  flash(f"Deleted game '{_game.name}'")
  return redirect(url_for("user.detail", username=current_user.username))

@game.route("/add", methods=['GET'])
@login_required
def add():
  _game_form = GameEntryForm(user=current_user)

  return render_template(
    'game/add.html',
    form=_game_form,
  )

@game.route("/add", methods=['POST'])
@login_required
def add_post():
  form = GameEntryForm(form=request.form)
  
  try:
    if(not form.validate()):
      raise ValueError(f"Form validation failed! {form.errors}")

    new_game = GameEntry()

    form.to_game(new_game)

    db.session.add(new_game)
    db.session.commit()
  except Exception as e:
    flash(f"DB Error: {e}")
    return redirect(url_for('game.add'))

  flash(f"Added new game {new_game.name}")
  return redirect(url_for('user.detail', username=current_user.username))
