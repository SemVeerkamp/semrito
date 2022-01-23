from website import create_app
import os

PORT=4000
os.environ.get('PORT', 5000)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

