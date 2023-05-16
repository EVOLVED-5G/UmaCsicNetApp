from src import create_app
from waitress import serve

# Main class
app = create_app()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=10001)