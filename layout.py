import PySimpleGUI as sg


def trello_gui_layout(trello_board_names):
    """トレロアプリのレイアウト"""

    # 選択エリア
    col_choice = sg.Column([

        [sg.T('Board', size=(5, 1)),
         sg.Combo(values=trello_board_names, size=(25, 1), key='BOARD_NAME', enable_events=True)],
        [sg.T('List', size=(5, 1)), sg.Combo(values=[''], size=(25, 1), key='LIST_NAME', enable_events=True)]
    ], size=(280, 50))

    # インポートエクスポート
    col_excel = sg.Column([
        [sg.B('export to excel', key='EXPORT', enable_events=True)], [
            sg.B('import from excel')],
    ], pad=((0, 0), (0, 0)), vertical_alignment='center'
    )

    column_top = sg.Column([[col_choice, col_excel]], vertical_alignment='top', justification='l')

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
    ], vertical_alignment='top', size=(300, 280))

    # デバッグ出力エリア
    frame_debug_print = sg.Frame('Debug', [
        [sg.Button('Clear', key='CLEAR_DEBUG')],
        [sg.MLine('', size=(35, 4), key='DEBUG_PRINT')]
    ], size=(300, 120))

    # カード出力のフレーム
    frame_print_card = sg.Frame('Print Card', [
        [sg.Button('All Card in Board', key='ALL_LIST_PRINT'),
         sg.Button('Just Selected List', key='SELECTED_LIST_PRINT')],
        [sg.MLine('', size=(30, 20), key='PREVIEW', enable_events=True)]
    ])

    column_bottom_left = sg.Column([[frame_add_card], [frame_debug_print]], size=(300, 400))
    column_bottom_right = sg.Column([[frame_print_card]], size=(300, 400))

    return [
        [sg.T('Trello GUI',
              size=(30, 1),
              justification='center',
              font=("Helvetica", 20),
              relief=sg.RELIEF_RIDGE)],
        [column_top],
        [column_bottom_left, column_bottom_right],
    ]
