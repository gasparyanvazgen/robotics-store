## MEM task 755

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
