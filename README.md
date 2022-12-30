## MEM task 755

Notice the code below which is in `app/__init__.py` file.
```python
# add default admin to the database - this is draft
user = User()
user.username = 'admin'
user.password = 'password'

db.session.add(user)
db.session.commit()
```
The above code runs every time the program is run, it adds the default admin user to the database. I'll fix this.
