from flask import Flask, render_template, request, abort, send_from_directory
import json
import requests
import redis
import uuid

RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

datasets = {
    "employees": {
        "url": "https://cs269155827a4fdx4087x964.z13.web.core.windows.net/"
    },
    "chatbot": {
        "url": "https://cs269155827a4fdx4087x964.z13.web.core.windows.net/PowerBIEmbedAzureFunction_Chatbot.html"
    },
    "dsa applications": {
        "data_url": "https://graphchat.westeurope.cloudapp.azure.com/data/dataset.csv"
    }
}
base_template = "https://graphchat.westeurope.cloudapp.azure.com/template/graph.html"

app = Flask(__name__, static_folder="../html",
            static_url_path='/', template_folder="./templates")

POOL = redis.ConnectionPool(
    host='localhost', decode_responses=True, port=6379, db=0)
redis_conn = redis.StrictRedis(connection_pool=POOL)


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('/', path)


@app.route('/data/<path:path>')
def data_process(path):
    print("HERE", path)
    return send_from_directory('data/', path)


@app.route('/process', )
def process():
    user_message = request.args.get('message')
    print(user_message)
    if user_message is None or user_message == "":
        response = {
            "url": "",
            "message": "I couldn't understand your query. Could you please repeat?"
        }
        return json.dumps(response)
    processor = Processor(user_message)

    response = {
        "url": processor.graph_url,
        "message": processor.hint
    }
    return json.dumps(response)


@app.route('/template/<path:path>')
def index(path):
    if path == "graph.html":
        code = request.args.get('code')
        d = redis_conn.hgetall(code)
        print(d)
        params = d.get("params")
        """
        params = params.replace("\"", "")
        params = params.replace(": ", ": \"")
        params = params.replace(",", "\",")
        params = params.replace("}", "\"}")
        params = params.replace('"null"', '[]')
        params = params.replace('"[\\', '["')
        params = params.replace('\\]"', '"]')
        """
        params = params.replace('null', '[]')
        params = params.replace('aggregation_list', 'aggregation')
        params = params.replace('filter_list', 'filter')
        params = params.replace('chart_type', 'graph_type')

        return render_template(path, data_url=d.get("data_url"), params=params)

    return render_template(path)


class Processor():
    def __init__(self, msg: str):
        self.msg = msg.strip()
        self.hint = ""
        self.graph_url = ""
        self.mapping()
        self.call()

    def mapping(self):
        m = {
            "dsa applications": ["tsa", "gsa", "dsa", "csa", "usa", "essay"],
            "employees": ["employee", "employer", "employees"],
            "filter_name": ["filter_name", "filter_name"],
            "plots": ["clocks"],
            "application": ["multiplication"],
            "chatbot": ["chabot", "chad boat", "chuck"],
        }
        for key, values in m.items():
            for value in values:
                msg = self.msg.replace(value, key)
                if self.msg != msg:
                    self.msg = msg
                    break

    def call(self):
        # sending get request and saving the response as response object
        print({"message": self.msg})
        headers = {'content-type': 'application/json'}
        r = requests.post(url=RASA_ENDPOINT,  headers=headers,
                          json={"message": self.msg})
        # extracting data in json format

        responses = r.json()
        if len(responses) == 0:
            self.msg = "Could you please repeat your query"
            return
        print("RASA RESPONSE:", responses)
        text = responses[0].get("text")
        response_json = json.loads(text)
        self.hint = response_json.get("message", "")

        graph_data = response_json.get("graph_data")
        if graph_data is None:
            return
        dataset_name = graph_data.get("dataset", "")
        dataset_meta = datasets.get(dataset_name.lower().strip())
        if dataset_meta is None:
            print("\nmissed the dataset name {}\n".format(dataset_name))
            return
        if dataset_meta.get("url"):
            self.graph_url = dataset_meta.get("url")
            return

        code = uuid.uuid1()
        code_url = base_template+"?code="+str(code)
        redis_conn.hmset(str(code), {
            "data_url": dataset_meta.get("data_url"),
            "params": json.dumps(graph_data)
        })
        self.graph_url = code_url


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
