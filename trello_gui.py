import PySimpleGUI as sg
from trello import TrelloClient
import settings
import layout
import excel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class TrelloGui:

    def __init__(self, user_id, key, secret, token):

        # トレロクライアントのインスタンス化
        self.client = TrelloClient(user_id, key, secret, token)
        # ボード名をインスタンス変数に格納
        self.board_names = self.client.get_board_names()

        # windowのインスタンス化
        self.window = sg.Window('for Trello...',
                                size=(600, 600),
                                finalize=True
                                ).Layout(layout.trello_gui_layout(self.board_names))

        # GUI操作に応じてセットされる変数
        self._trello_borad_name = None
        self._trello_board_id = None
        self._trello_list_id = None
        self._trello_list_names = None
        self._trello_list_ids = None

    def set_trello_board_name(self, board_name):
        self._trello_borad_name = board_name

    def set_trello_board_id(self, board_id):
        self._trello_board_id = board_id

    def set_trello_list_id(self, list_id):
        self._trello_list_id = list_id

    def set_trello_list_names(self, ids_and_names):
        self._trello_list_names = [name for list_id, name in ids_and_names]

    def set_trello_list_ids(self, ids_and_names):
        self._trello_list_ids = [list_id for list_id, name in ids_and_names]

    def debug_print(self, msg):
        """
        debug print エリアにメッセージを出力
        """
        self.window['DEBUG_PRINT'].print(msg)

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
                self.set_trello_board_name(board_name)
                board_id = self.client.get_board_id(board_name)
                self.set_trello_board_id(board_id)
                id_and_name_of_trello_list = self.client.get_list_ids_and_names(board_id)
                self.set_trello_list_names(id_and_name_of_trello_list)
                self.set_trello_list_ids(id_and_name_of_trello_list)
                self.window['LIST_NAME'].Update(values=self._trello_list_names)

            # Trelloリスト名が選択されたら、Trelloリストidをセットします
            if event == 'LIST_NAME':
                list_name = values['LIST_NAME']
                list_id = self.client.get_list_id(self._trello_board_id, list_name)
                self.set_trello_list_id(list_id)

            # カードを追加します
            if event == 'ADD_CARD':
                if not self._trello_list_id:
                    sg.Popup('', '追加するリストを選択してください')
                elif not values['CARD_NAME']:
                    sg.Popup('', 'カード名は必須です')
                else:
                    card_name = values['CARD_NAME']
                    desc = values['DESC']
                    due_date = values['DUE_DATE']
                    due_time = values['DUE_TIME']
                    self.client.add_task(self._trello_list_id, card_name, due_date, due_time, desc)

                    self.debug_print(f'カードの追加に成功しました。')

            # 選択されているボードの全カードを出力します
            if event == 'ALL_LIST_PRINT':
                if self._trello_borad_name:
                    preview_text = ''
                    for list_id, list_name in zip(self._trello_list_ids, self._trello_list_names):
                        json_data = self.client.get_cards_in_list(list_id)
                        preview_text += f'=====\n{list_name}\n=====\n'
                        for json in json_data:
                            card_name = json['name']
                            preview_text += f'{card_name}\n---\n'
                    self.window['PREVIEW'].Update(preview_text)
                else:
                    sg.Popup('', 'ボードを選択してください')

            # 選択されているTrelloリストのカードを出力します
            if event == 'SELECTED_LIST_PRINT':
                if values['LIST_NAME']:
                    preview_text = ''
                    list_name = values['LIST_NAME']
                    preview_text += f'=====\n{list_name}\n=====\n'
                    json_data = self.client.get_cards_in_list(self._trello_list_id)
                    for json in json_data:
                        card_name = json['name']
                        preview_text += f'{card_name}\n---\n'
                    self.window['PREVIEW'].Update(preview_text)
                else:
                    sg.Popup('', 'リストを選択してください')

            # 選択されているボードをExcelにエクスポートします
            if event == 'EXPORT':
                if self._trello_borad_name:
                    excel.export_excel(trello_client=self.client,
                                       board_name=self._trello_borad_name,
                                       list_ids=self._trello_list_ids,
                                       list_names=self._trello_list_names,
                                       save_dir=BASE_DIR)

                    self.debug_print(f'exportに成功しました。')

                else:
                    sg.Popup('', 'ボードを選択してください')

            if event == 'CLEAR_DEBUG':
                self.window['DEBUG_PRINT'].update(value='')

def job():
    user_id = settings.TRELLO_USER_ID
    key = settings.TRELLO_API_KEY
    secret = settings.TRELLO_API_SECRET
    token = settings.TRELLO_API_TOKEN
    gui = TrelloGui(user_id=user_id, key=key, secret=secret, token=token)
    gui.event_loop()


if __name__ == '__main__':
    job()
