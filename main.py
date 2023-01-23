from jamals_stats_api import app, db
from jamals_stats_api.api.drivers import driver_blueprint
from jamals_stats_api.model.drivers import init_drivers

app.register_blueprint(driver_blueprint)

@app.before_first_request
def activate_job():
    db.create_all() # Added <--- Must add
    init_drivers()

if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8086")
