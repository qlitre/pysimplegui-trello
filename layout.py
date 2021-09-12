import PySimpleGUI as sg


def trello_gui_layout(trello_board_names):
    """トレロアプリのレイアウト"""

    column_choice = sg.Column([
        [sg.T('Choice Board')],
        [sg.Combo(values=trello_board_names, size=(35, 1), key='BOARD_NAME', enable_events=True)],
        [sg.T('Choice List')],
        [sg.Combo(values=[''], size=(35, 1), key='LIST_NAME', enable_events=True)]
    ])

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

    frame_excel = sg.Frame('Excel', [
        [sg.B('export', key='EXPORT'), sg.B('import')],
    ], pad=((15, 0), (20, 20)))

    return [
        [sg.T('Trello GUI',
              size=(30, 1),
              justification='center',
              font=("Helvetica", 20),
              relief=sg.RELIEF_RIDGE)],
        [column_choice, frame_excel],
        [frame_add_card, frame_print_card]
    ]
