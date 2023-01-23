from __init__ import app  # Definitions initialization
from model.tokens import initTeams


# setup APIs
from api.cardAPI import card_api # Blueprint import api definition
# from api.driver import joke_api # Blueprint import api definition
from api.formulaone import f1_api # Blueprint import api definition

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        initTeams()
        

if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8086")
