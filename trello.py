import requests
from datetime import datetime
from datetime import timedelta


class TrelloClient:

    def __init__(self, user_id: str, key: str, secret: str, token: str):
        self.user_id = user_id
        self.key = key
        self.secret = secret
        self.token = token
        self.URL = 'https://trello.com/1/'

    def get_board_id(self, board_name: str):
        """
        ボード名からボードidを特定する
        """
        end_point = f"members/{self.user_id}/boards?key={self.key}&token={self.token}&fields=name"
        json_data = requests.get(self.URL + end_point).json()
        for json in json_data:
            if json['name'] == board_name:
                return json['id']

    def get_board_names(self):
        """
        ボード名のリストを返す
        """
        end_point = f"members/{self.user_id}/boards?key={self.key}&token={self.token}&fields=name"
        json_data = requests.get(self.URL + end_point).json()
        return [json['name'] for json in json_data]

    def get_list_id(self, board_id: str, list_name: str):
        """
        ボードidとTrelloリスト名からTrelloリストidを特定して返す
        """
        end_point = f"boards/{board_id}/lists?key={self.key}&token={self.token}&fields=name"
        json_data = requests.get(self.URL + end_point).json()
        for json in json_data:
            if json['name'] == list_name:
                return json['id']

    def get_list_ids_and_names(self, board_id: str):
        """
        idとnameがタプルになったリストを返す
        """
        end_point = f"boards/{board_id}/lists?key={self.key}&token={self.token}&fields=name"
        json_data = requests.get(self.URL + end_point).json()
        return [(json['id'], json['name']) for json in json_data]

    def add_task(self, list_id: str, card_name: str, due_date: str = None, due_time: str = None, desc: str = None):
        """
        カードを特定のリストに追加する
        """
        end_point = "cards"
        if due_date and due_time:
            due = datetime.strptime(due_date + ' ' + due_time, '%Y/%m/%d %H:%M')
            # そのまま登録すると13時間後になる仕様のため
            due = due - timedelta(hours=13)
            due = due.isoformat()
        else:
            due = ""

        query = {
            'key': self.key,
            'token': self.token,
            'idList': list_id,
            'name': card_name,
            'desc': desc,
            'due': due}

        requests.request("POST", self.URL + end_point, params=query)

    def get_cards_in_list(self, list_id):
        """
        Trelloリストの中のカードをjson形式で返す
        """
        end_point = f"lists/{list_id}/cards"
        query = {
            'key': self.key,
            'token': self.token
        }

        response = requests.request(
            "GET",
            self.URL + end_point,
            params=query
        )

        return response.json()

    def create_new_trello_list(self, board_id: str, list_name: str):
        """
        ボードidとリスト名を指定して、新しいリストを作ります。
        """
        end_point = "lists"

        query = {
            'key': self.key,
            'token': self.token,
            'name': list_name,
            'idBoard': board_id
        }

        response = requests.request(
            "POST",
            self.URL + end_point,
            params=query
        )

        return response.text

    def create_new_trello_board(self, board_name: str):
        end_point = "boards/"

        query = {
            'key': self.key,
            'token': self.token,
            'name': board_name
        }

        response = requests.request(
            "POST",
            self.URL + end_point,
            params=query
        )

        return response.text
