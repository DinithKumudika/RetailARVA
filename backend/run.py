from src.app import create_app

if __name__ == '__main__':
    # mongodb://[mongo_username]:[mongo_password]@mongo:27017/
    app = create_app()
    app.run(host='0.0.0.0', debug=True)