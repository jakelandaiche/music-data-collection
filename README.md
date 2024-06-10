# https://www.drexel-musicbox.com/index.html

## Running

Install the packages in `requirements.txt` first

```
pip3 install -r requirements.txt
```

Then create the database with 

```
python3 create_sqlite.py
```

Run the server with

```
python3 server.py [--host HOST] [--port PORT]
```

Default value for `HOST:PORT` is `localhost:8080`

