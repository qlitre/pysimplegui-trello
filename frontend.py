import PySimpleGUI as sg


class Widget:
    """ウィジェットを定義"""

    @staticmethod
    def relief():
        """リリーフ"""

        return sg.T(text='Trello GUI',
                    size=(30, 1),
                    justification='center',
                    font=("Helvetica", 20),
                    relief=sg.RELIEF_RIDGE)

    @staticmethod
    def label(text: str, width: int = None):
        """ラベル的なテキストボックス"""
        if not width:
            width = len(text) + 1
        return sg.T(text, (width, 1))

    @staticmethod
    def combo(key, values=None, enable_events=True):
        """コンボボックス"""
        if not values:
            values = []
        return sg.Combo(values=values,
                        size=(25, 1),
                        key=key,
                        enable_events=enable_events)

    @staticmethod
    def input(key: str, width: int, height: int = 1):
        """インプットテキスト"""
        return sg.InputText('', size=(width, height), key=key)

    @staticmethod
    def textarea(key: str, height: int, width: int = 35):
        """mline"""
        return sg.MLine('', size=(width, height), key=key)

    @staticmethod
    def button(text: str, key: str):
        """ボタン"""
        return sg.Button(text, key=key)


class Frontend(Widget):
    """GUIの見た目を定義"""

    def column_choice(self):
        """ボードとリストの選択エリア"""

        left = sg.Column(layout=[[self.label('Board')],
                                 [self.label('List')]])
        right = sg.Column(layout=[[self.combo(key='BOARD_NAME')],
                                  [self.combo(key='LIST_NAME')]])

        return sg.Column([
            [left, right]
        ], size=(280, 70))

    def frame_import(self):
        """インポートボタンフレーム"""
        return sg.Frame('Import', layout=[[self.button(text='Excel', key='IMPORT_EXCEL')]])

    def frame_export(self):
        """エクスポートボタンフレーム"""
        return sg.Frame('Export', layout=[[self.button('Excel', key='EXPORT_EXCEL')]])

    def frame_add_card(self):
        """カード追加フレーム"""
        col1 = [[self.label(text='due date', width=10)],
                [self.input(width=10, key="DUE_DATE")]]
        col2 = [[self.label(text='time', width=10)],
                [self.input(width=10, key="DUE_TIME")]]

        return sg.Frame('Add Card', [
            [self.label('Card Name')],
            [self.textarea(key="CARD_NAME", height=2)],
            [self.label('Description')],
            [self.textarea(key="DESC", height=2)],
            [sg.Column(col1), sg.Column(col2)],
            [self.button(text='ADD', key="ADD_CARD")]
        ], vertical_alignment='top', size=(300, 280))

    def frame_debug_print(self):
        """デバッグ出力フレーム"""
        return sg.Frame('Debug', [
            [self.button(text='Clear', key='CLEAR_DEBUG')],
            [self.textarea(height=4, key='DEBUG_PRINT')]
        ], size=(300, 120))

    def frame_card_print(self):
        """カード内容プリントフレーム"""
        return sg.Frame('Print Card', [
            [self.button(text='All Card in Board', key='ALL_LIST_PRINT'),
             self.button(text='Just Selected List', key='SELECTED_LIST_PRINT')],
            [self.textarea(key='PREVIEW', width=30, height=20)]
        ])

    def layout(self):
        left = sg.Column(layout=[
            [self.column_choice()],
            [self.frame_add_card()],
            [self.frame_debug_print()]
        ])
        right = sg.Column(layout=[
            [self.frame_export(), self.frame_import()],
            [self.frame_card_print()]], vertical_alignment='t')

        layout = [[self.relief()],
                  [left, right]]

        return layout

    def window(self):
        return sg.Window(title='for Trello...',
                         size=(600, 600),
                         finalize=True,
                         layout=self.layout())
