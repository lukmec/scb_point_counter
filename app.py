#importing "app" --> Flask Container for the application, that is referenced by procfile or vercel.json
from counter_app import counter_app as app

#for running locally for testing
if __name__ == "__main__":

    app.run()
