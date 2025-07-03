from gameorganize.db import db
from flask_wtf import FlaskForm
from gameorganize.model.game import GameEntry, Completion, Priority
from gameorganize.model.platform import Platform
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import NumberInput, TextArea

class GameEntryForm(FlaskForm):
    def from_user(self, user):
        self.platform.choices += [platform.name for platform in user.platforms]

    def from_game(self, game):
        self.name.data = game.name
        if(game.platform):
            self.platform.data = game.platform.name
        self.platform.choices += [platform.name for platform in game.user.platforms]
        self.completion.data = game.completion.name
        self.priority.data = game.priority.name
        self.notes.data = game.notes

    def to_game(self, game_entry):
        platform_select = db.session.query(Platform).where(Platform.name==self.platform.data).first()
        game_entry.name = self.name.data
        game_entry.platform = platform_select
        game_entry.completion = Completion[self.completion.data]
        game_entry.priority = Priority[self.priority.data]
        game_entry.cheev = self.cheev.data
        game_entry.cheev_total = self.cheev_total.data
        game_entry.notes = self.notes.data

    name = StringField(
        'Name', 
        validators=[DataRequired()]
    )

    platform = SelectField(
        'Platform',
       choices=[""], #validators=[DataRequired()]
    )

    completion = SelectField(
        'Completion', 
        default=Completion.Started, choices=Completion.choices(), validators=[DataRequired()]
    )

    priority = SelectField(
        'Priority', 
        default=Priority.Low, choices=Priority.choices(), validators=[DataRequired()]
    )

    cheev = IntegerField(
        'Achievement Count', 
        default=0, widget=NumberInput(min = 0)
    )

    cheev_total = IntegerField(
        'Achievement Total', 
        default=0, widget=NumberInput(min = 0)
    )

    notes = StringField(
        'Notes', 
        widget=TextArea(), validators=[Optional()]
    )
