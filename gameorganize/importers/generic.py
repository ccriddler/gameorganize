from gameorganize.db import db
from gameorganize.model.platform import Platform
from gameorganize.model.game import GameEntry, Completion, Priority
from flask import flash

def parse_csv_line(line, user):
  platform_name = line.get("Platform")
  platform = find_or_create_platform(user, platform_name)

  try:
    new_game = GameEntry(
      name = line.get("Name"),
      platform = platform,
      completion = Completion[line.get("Completion")],
      priority = Priority[line.get("Priority")],
      notes = line.get("Notes"),
      user = user,
    )

    db.session.add(new_game)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    flash(f"DB Error: {e}")
    print(e)
    return None

  return new_game


def import_csv(csv_data, user):
  if(not csv_data):
    flash("Missing CSV data")
    return []

  csv_parsed = csv_data.read().decode("utf-8").split("\n")

  csv_reader = csv.DictReader(csv_parsed)

  new_games = []

  for line in csv_reader:
    new_game = parse_csv_line(line, user)
    if(new_game):
      new_games.append(new_game)
  return new_games
