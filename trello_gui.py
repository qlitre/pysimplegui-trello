import PySimpleGUI as sg
from trello import TrelloClient
import settings


class TrelloGui(TrelloClient):

    def __init__(self, user_id, key, secret, token):

        super().__init__(user_id=user_id,
                         key=key,
                         secret=secret,
                         token=token)
        # ボード名をインスタンス変数に格納
        self.board_names = super().get_board_names()
        # windowのインスタンス化
        self.window = sg.Window('for Trello...', size=(560, 560), finalize=True).Layout(self.layout())
        # GUI操作に応じてセットされる変数
        self._trello_board_id = None
        self._trello_list_id = None
        self._trello_list_names = None
        self._trello_list_ids = None

    def set_trello_board_id(self, board_id):
        self._trello_board_id = board_id

    def set_trello_list_id(self, list_id):
        self._trello_list_id = list_id

    def set_trello_list_names(self, ids_and_names):
        self._trello_list_names = [name for list_id, name in ids_and_names]

    def set_trello_list_ids(self, ids_and_names):
        self._trello_list_ids = [list_id for list_id, name in ids_and_names]

    def layout(self):
        """レイアウトを定義します"""

        # カード追加のフレーム
        col1 = [[sg.T('due date', size=(10, 1))],
                [sg.InputText('', size=(10, 1), key="DUE_DATE")]]
        col2 = [[sg.T('time', size=(5, 1))],
                [sg.InputText('', size=(5, 1), key="DUE_TIME")]]

        frame_add_card = sg.Frame('Add Card', [
            [sg.T('Card Name')],
            [sg.MLine('', size=(35, 2), key="CARD_NAME")],
            [sg.T('Description')],
            [sg.MLine('', size=(35, 2), key="DESC")],
            [sg.Column(col1), sg.Column(col2)],
            [sg.Submit('ADD', key="ADD_CARD")]
        ])

        # カード出力のフレーム
        frame_print_card = sg.Frame('Print Card', [
            [sg.Button('All Card in Board', key='ALL_LIST_PRINT'),
             sg.Button('Just Selected List', key='SELECTED_LIST_PRINT')],
            [sg.MLine('', size=(35, 20), key='PREVIEW', enable_events=True)]
        ])

        return [
            [sg.T('Trello GUI',
                  size=(30, 1),
                  justification='center',
                  font=("Helvetica", 20),
                  relief=sg.RELIEF_RIDGE)],
            [sg.T('Choice Board')],
            [sg.Combo(values=self.board_names, size=(20, 1), key='BOARD_NAME', enable_events=True)],
            [sg.T('Choice List')],
            [sg.Combo(values=[''], size=(20, 1), key='LIST_NAME', enable_events=True)],
            [frame_add_card, frame_print_card]
        ]

    def event_loop(self):

        while True:
            event, values = self.window.read()
            if event is None:
                print('exit')
                break
            # 選択されたボード名に応じて、Trelloリスト名コンボボックスの更新、
            # インスタンス変数にTrelloリスト情報をセットします。
            if event == 'BOARD_NAME':
                board_name = values['BOARD_NAME']
                board_id = super().get_board_id(board_name)
                self.set_trello_board_id(board_id)
                id_and_name_of_trello_list = super().get_list_ids_and_names(board_id)
                self.set_trello_list_names(id_and_name_of_trello_list)
                self.set_trello_list_ids(id_and_name_of_trello_list)
                self.window['LIST_NAME'].Update(values=self._trello_list_names)

            # Trelloリスト名が選択されたら、Trelloリストidをセットします
            if event == 'LIST_NAME':
                list_name = values['LIST_NAME']
                list_id = super().get_list_id(self._trello_board_id, list_name)
                self.set_trello_list_id(list_id)

            # カードを追加します
            if event == 'ADD_CARD':
                card_name = values['CARD_NAME']
                desc = values['DESC']
                due_date = values['DUE_DATE']
                due_time = values['DUE_TIME']
                super().add_task(self._trello_list_id, card_name, due_date, due_time, desc)

            # 選択されているボードの全カードを出力します
            if event == 'ALL_LIST_PRINT':
                preview_text = ''
                for list_id, list_name in zip(self._trello_list_ids, self._trello_list_names):
                    json_data = super().get_cards_in_list(list_id)
                    preview_text += f'=====\n{list_name}\n=====\n'
                    for json in json_data:
                        card_name = json['name']
                        preview_text += f'{card_name}\n---\n'
                self.window['PREVIEW'].Update(preview_text)

            # 選択されているTrelloリストのカードを出力します
            if event == 'SELECTED_LIST_PRINT':
                preview_text = ''
                list_name = values['LIST_NAME']
                preview_text += f'=====\n{list_name}\n=====\n'
                json_data = super().get_cards_in_list(self._trello_list_id)
                for json in json_data:
                    card_name = json['name']
                    preview_text += f'{card_name}\n---\n'
                self.window['PREVIEW'].Update(preview_text)


def job():
    user_id = settings.TRELLO_USER_ID
    key = settings.TRELLO_API_KEY
    secret = settings.TRELLO_API_SECRET
    token = settings.TRELLO_API_TOKEN
    gui = TrelloGui(user_id=user_id, key=key, secret=secret, token=token)
    gui.event_loop()


if __name__ == '__main__':
    job()
