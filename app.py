import logging
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
db = SQLAlchemy(app)
app.logger.setLevel(logging.DEBUG)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TEAM = db.Column(db.String(50), nullable=False)
    OVR = db.Column(db.Float, nullable=False)
    OFF = db.Column(db.Float, nullable=False)
    PASS = db.Column(db.Float, nullable=False)
    RUN = db.Column(db.Float, nullable=False)
    RECV = db.Column(db.Float, nullable=False)
    PBLK = db.Column(db.Float, nullable=False)
    RBLK = db.Column(db.Float, nullable=False)
    DEF = db.Column(db.Float, nullable=False)
    RDEF = db.Column(db.Float, nullable=False)
    TACK = db.Column(db.Float, nullable=False)
    PRSH = db.Column(db.Float, nullable=False)
    COV = db.Column(db.Float, nullable=False)
    winner = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'{self.TEAM}'


class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    GAME_DATE = db.Column(db.String(50), nullable=False)
    HOME_TEAM = db.Column(db.String(50), nullable=False)
    OVR = db.Column(db.Float, nullable=False)
    OFF = db.Column(db.Float, nullable=False)
    PASS = db.Column(db.Float, nullable=False)
    RUN = db.Column(db.Float, nullable=False)
    RECV = db.Column(db.Float, nullable=False)
    PBLK = db.Column(db.Float, nullable=False)
    RBLK = db.Column(db.Float, nullable=False)
    DEF = db.Column(db.Float, nullable=False)
    RDEF = db.Column(db.Float, nullable=False)
    TACK = db.Column(db.Float, nullable=False)
    PRSH = db.Column(db.Float, nullable=False)
    COV = db.Column(db.Float, nullable=False)
    AWAY_TEAM = db.Column(db.String(50), nullable=False)
    AWAY_OVR = db.Column(db.Float, nullable=False)
    AWAY_OFF = db.Column(db.Float, nullable=False)
    AWAY_PASS = db.Column(db.Float, nullable=False)
    AWAY_RUN = db.Column(db.Float, nullable=False)
    AWAY_RECV = db.Column(db.Float, nullable=False)
    AWAY_PBLK = db.Column(db.Float, nullable=False)
    AWAY_RBLK = db.Column(db.Float, nullable=False)
    AWAY_DEF = db.Column(db.Float, nullable=False)
    AWAY_RDEF = db.Column(db.Float, nullable=False)
    AWAY_TACK = db.Column(db.Float, nullable=False)
    AWAY_PRSH = db.Column(db.Float, nullable=False)
    AWAY_COV = db.Column(db.Float, nullable=False)
    winner = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'{self.HOME_TEAM} vs {self.AWAY_TEAM}'


app.app_context().push()
db.drop_all()
db.create_all()


# @app.before_first_request
def setup_db():
    if Team.query.count() == 0:
        app.logger.info("Loading teams into database")
        df1 = pd.read_csv(r"Data/Grades/TeamGrades.csv")
        teams = [Team(TEAM=row['TEAM'],
                      OVR=row['OVR'],
                      OFF=row['OFF'],
                      PASS=row['PASS'],
                      RUN=row['RUN'],
                      RECV=row['RECV'],
                      PBLK=row['PBLK'],
                      RBLK=row['RBLK'],
                      DEF=row['DEF'],
                      RDEF=row['RDEF'],
                      TACK=row['TACK'],
                      PRSH=row['PRSH'],
                      COV=row['COV'],
                      winner="None") for index, row in df1.iterrows()]
        db.session.bulk_save_objects(teams)
        db.session.commit()

    if Matchup.query.count() == 0:
        app.logger.info("Loading matchups into database")
        matchups = []
        for ii in range(1, 19):
            df = pd.read_csv(f"Data/Matchups/grades_matchups_WEEK{ii}.csv")
            for index, row in df.iterrows():
                matchup = Matchup(
                    GAME_DATE=row['Game Date'],
                    HOME_TEAM=row['Home Team'],
                    OVR=row['OVR'],
                    OFF=row['OFF'],
                    PASS=row['PASS'],
                    RUN=row['RUN'],
                    RECV=row['RECV'],
                    PBLK=row['PBLK'],
                    RBLK=row['RBLK'],
                    DEF=row['DEF'],
                    RDEF=row['RDEF'],
                    TACK=row['TACK'],
                    PRSH=row['PRSH'],
                    COV=row['COV'],
                    AWAY_TEAM=row['Away Team'],
                    AWAY_OVR=row['OPP OVR'],
                    AWAY_OFF=row['OPP OFF'],
                    AWAY_PASS=row['OPP PASS'],
                    AWAY_RUN=row['OPP RUN'],
                    AWAY_RECV=row['OPP RECV'],
                    AWAY_PBLK=row['OPP PBLK'],
                    AWAY_RBLK=row['OPP RBLK'],
                    AWAY_DEF=row['OPP DEF'],
                    AWAY_RDEF=row['OPP RDEF'],
                    AWAY_TACK=row['OPP TACK'],
                    AWAY_PRSH=row['OPP PRSH'],
                    AWAY_COV=row['OPP COV'],
                    winner="None"
                )
                matchups.append(matchup)
        db.session.bulk_save_objects(matchups)
        db.session.commit()


def get_all_weeks():
    # Retrieve a distinct list of all weeks in GAME_DATE column
    return Matchup.query.with_entities(Matchup.GAME_DATE).distinct()


setup_db()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the team names from the form
        team1_name = request.form.get('team1')
        team2_name = request.form.get('team2')
        # Get the Team objects from the database based on the team names
        team1s = Team.query.filter_by(TEAM=team1_name).first()
        team2s = Team.query.filter_by(TEAM=team2_name).first()
        # Pass the teams and their statistics to the results page
        return render_template('results.html', team1s=team1s, team2s=team2s)
    # If the request method is GET, show the compare page
    return render_template('compare.html', teams=Team.query.all())


@app.route('/matchups', methods=['GET', 'POST'])
def matchup_data():
    weeks = get_all_weeks()  # Your function to retrieve all matchups
    if request.method == 'POST' and 'GAME_DATE' in request.form:
        week = request.form['GAME_DATE']
        selected_matchups = Matchup.query.filter_by(GAME_DATE=week)
        return render_template('weeks.html', weeks=weeks, selected_matchups=selected_matchups)
    if request.method == 'GET':
        return render_template('weeks.html', weeks=weeks)


if __name__ == '__main__':
    app.run(debug=True)
