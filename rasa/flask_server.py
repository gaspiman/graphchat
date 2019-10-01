from flask import Flask, request
app = Flask(__name__)

@app.route('/<type>/', methods=["POST"])
def dummy(type):
    print(request.data)
    if type == "backend":
        print("backend")
        return "url_of_graph"
    else:
        print("app")
        return "app_response"