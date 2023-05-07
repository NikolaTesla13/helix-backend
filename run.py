from src.app import app

is_debug = True
port = 4000

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=is_debug)
