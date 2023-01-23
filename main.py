from jamals_stats_api import app, db
from jamals_stats_api.api.drivers import driver_blueprint
from jamals_stats_api.model.drivers import init_drivers
from __init__ import app  # Definitions initialization
from model.tokens import initTeams
from api.cardAPI import card_api # Blueprint import api definition
from api.formulaone import f1_api # Blueprint import api definition

from projects.projects import app_projects # Blueprint directory import projects definition

app.register_blueprint(driver_blueprint)

@app.before_first_request
def init_db():
    with app.app_context():
        init_drivers()
        db.create_all()
        initTeams()

if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8086")
