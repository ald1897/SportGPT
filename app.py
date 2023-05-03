import logging
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
db = SQLAlchemy(app)
app.logger.setLevel(logging.DEBUG)

app.logger.debug("Define Team Data Model")


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rushing_offense_grade = db.Column(db.Integer, nullable=False)
    passing_offense_grade = db.Column(db.Integer, nullable=False)
    rushing_defense_grade = db.Column(db.Integer, nullable=False)
    passing_defense_grade = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<{self.name}>'


app.logger.debug("Push App Context")
app.app_context().push()

app.logger.debug("Get rid of old Data")
db.drop_all()

app.logger.debug("Create Team Data Model in DB")
db.create_all()

app.logger.debug("Add Data for Team 1")

# Create a pandas dataframe that holds the data for the two teams
df = pd.DataFrame({'name': ['Team 1', 'Team 2'],
                   'rushing_offense_grade': [80, 85],
                   'passing_offense_grade': [70, 75],
                   'rushing_defense_grade': [75, 80],
                   'passing_defense_grade': [85, 70],
                   'winner': [False, False]})
# Create a variable called team1s that holds the data for team 1 in a Team object
team1s = Team(name=df['name'][0], rushing_offense_grade=df['rushing_offense_grade'][0],
              passing_offense_grade=df['passing_offense_grade'][0],
              rushing_defense_grade=df['rushing_defense_grade'][0],
              passing_defense_grade=df['passing_defense_grade'][0],
              winner=df['winner'][0])
# Create a variable called team2s that holds the data for team 2 in a Team object
team2s = Team(name=df['name'][1], rushing_offense_grade=df['rushing_offense_grade'][1],
              passing_offense_grade=df['passing_offense_grade'][1],
              rushing_defense_grade=df['rushing_defense_grade'][1],
              passing_defense_grade=df['passing_defense_grade'][1],
              winner=df['winner'][1])
# Add the data for team 1 to the database
print(df)
print(team1s)
print(team2s)

db.session.add(team1s)
# Add the data for team 2 to the database
db.session.add(team2s)
#
#
# team1d = Team(name='Team 1', rushing_offense_grade=80, passing_offense_grade=70, rushing_defense_grade=75,
#               passing_defense_grade=85, winner=False)
# db.session.add(team1d)
#
# app.logger.debug("Add Data for Team 2")
# team2d = Team(name='Team 2', rushing_offense_grade=85, passing_offense_grade=75, rushing_defense_grade=80,
#               passing_defense_grade=70, winner=False)
# db.session.add(team2d)

app.logger.debug("Commit DB Changes")
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    app.logger.debug("Hitting Base Route / ")
    if request.method == 'POST':
        team1 = Team.query.filter_by(name=team1s.name).first()
        team2 = Team.query.filter_by(name=team2s.name).first()
        if team1s.passing_defense_grade > team2s.passing_defense_grade:
            team1.winner = True
        else:
            team2.winner = True
        return render_template('results.html', team1=team1, team2=team2, teams=Team.query.all())
    return render_template('compare.html', teams=Team.query.all())


if __name__ == '__main__':
    app.run(debug=True)
