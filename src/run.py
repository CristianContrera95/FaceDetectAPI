from app import app
from config import ENVIRONMENT, PORT


if __name__ == '__main__':
    if ENVIRONMENT == 'dev':
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        app.run(host='0.0.0.0', port=PORT, debug=False)
