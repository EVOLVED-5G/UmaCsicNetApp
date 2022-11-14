from src import create_app
from waitress import serve


app = create_app()

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=80)
    serve(app, host='0.0.0.0', port=10001)