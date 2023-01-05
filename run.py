from app import create_app, User, db

app = create_app()


@app.before_first_request
def create_user():
    # Check if the user exists in the database
    user = User.query.filter_by(username=app.config['USER']).first()

    if not user:
        # Add the user to the database
        user = User()
        user.username = app.config['USER']
        user.password = app.config['PASSWORD']

        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    app.run()
