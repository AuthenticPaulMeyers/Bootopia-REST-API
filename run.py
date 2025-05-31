from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    print("database created!")
    app.run(debug=True)
