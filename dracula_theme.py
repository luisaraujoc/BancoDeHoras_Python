import PySimpleGUI as sg

# Defina um tema inspirado no Dracula
dracula_theme = {
    'BACKGROUND': '#282a36',
    'TEXT': '#f8f8f2',
    'INPUT': '#44475a',
    'TEXT_INPUT': '#f8f8f2',
    'SCROLL': '#50fa7b',
    'BUTTON': ('#bd93f9', '#44475a'),
    'PROGRESS': ('#bd93f9', '#50fa7b'),
    'BORDER': 0,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

sg.theme_add_new('Dracula', dracula_theme)