from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
import gameorganize.importers

importer = Blueprint('importer', __name__, template_folder='templates')

def import_steam(id, key):
    backend = ImporterBackend(current_user)
    importer = ImporterSteam(
        backend=backend, 
        steam_id=id, 
        api_key=key
    )

    meta_games = importer.get_owned_games()
    app_ids = [game.get("appid",0) for game in meta_games.get("response", {}).get("games", [])]
    meta_cheev = importer.get_player_achievements_bulk(app_ids)

    return importer.add_all(meta_games, meta_cheev)

def import_ra(id, key):
    backend = ImporterBackend(current_user)
    importer = importers.retroachievemnts.ImporterRA(
        backend=backend, 
        username=id, 
        api_key=key
    )

    meta = importer.get_user_completion_progress()
    return importer.add_all(meta)

@importer.route("/", methods=['POST'])
@login_required
def import_post():
    site = request.form.get("website")
    api_id = request.form.get("id")
    apiKey = request.form.get("key")

    new_games = []

    if(site == "Steam"):
        new_games = import_steam(api_id, apiKey)

    elif(site == "RetroAchievements"):
        new_games = import_ra(api_id, apiKey)

    try:
        db.session.commit()
    except Exception as e:
        flash(f"Import error: {e}")
    finally:
        flash(f"Imported {len(new_games)} games from {site}")

    return redirect(url_for('importer.detail'))

@importer.route("/", methods=['GET'])
@login_required
def detail():
    return render_template(
        'importer/detail.html'
    )
