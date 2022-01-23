from website import create_app
import os

port = int(os.environ.get('PORT'))

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

