# import asyncio
# from websockets.server import serve
from requests import Session
from flask import Flask
from flask_restful import Api, Resource, reqparse, request

session = Session()

class symbolSuggestion(Resource):

    def __init__(self) -> None:

        self.name_mappings = {}
        self.names = []

        import csv
        file = open('MCAP31032023_0.csv')
        csvreader = csv.reader(file)

        for row in csvreader:
            self.name_mappings[row[1].lower()] = {"name": row[2], "symb": row[1]}
            self.names.append(row[1].lower())
            self.name_mappings[row[2].lower()] = {"name": row[2], "symb": row[1]}
            self.names.append(row[2].lower())
        file.close()

    def get(self):
        query = request.args.get('q')
        filtered_list = list(set([self.name_mappings[string]['symb'] for string in self.names if string.startswith(query)]))
        print(filtered_list)
        return_list = [self.name_mappings[symbol_name.lower()] for symbol_name in filtered_list]
        return {"suggestions":return_list}



page_url = "https://www.nseindia.com/"
base_url = "https://www.nseindia.com/api"

h = {
    "Host": "www.nseindia.com",
    "Referer": "https://www.nseindia.com/",
    "X-Requested-With": "XMLHttpRequest",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}
session.headers.update(h)
session.get(page_url)
    


app = Flask(__name__)
api = Api(app)


api.add_resource(symbolSuggestion, '/')
app.run(debug=True, host='0.0.0.0')