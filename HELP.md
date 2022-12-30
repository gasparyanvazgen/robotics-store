## MEM task 755

##### Before running
Open CLI and to do these commands for you (examples for Linux/MacOS)
```shell
pip install -r requirements.txt

export MYSQL_USER=root
export MYSQL_PASSWORD=password
export MYSQL_HOST=localhost:3306
export DATABASE=mysql
```
<br/>

#### Run program with one of these example:
```shell
export FLASK_APP=run.py

# you can run this in debug mode with this:
export FLASK_DEBUG=1

flask run
```

```shell
python3 run.py
```

In program default enabled DEBUG mode. You can change this in `create_app()` function at `app/__init__.py` file.
```python
# Load the default configuration
app.config.from_object('config.DevelopmentConfig')
```
Change above code attribute value to `'config.ProductionConfig'`. That you can see in `config.py` file.
