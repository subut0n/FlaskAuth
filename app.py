from pip import main
from project import create_app
from project import app

if __name__ == "__main__" :
    app.run(debug=True)