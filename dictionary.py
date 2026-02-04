#!/usr/bin/env python3
import json
import os
from dataclasses import dataclass, asdict 
from nicegui import ui
from deep_translator import GoogleTranslator

FILE_PATH = 'dictionary.json'


@dataclass
class WordPair:
    english: str
    russian: str

DICTIONARY_DB = {'cat': 'кот', 'dog': 'собака'}


def save_data(words):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump([asdict(w) for w in words], f, ensure_ascii=False, indent=4)

def load_data():  
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [WordPair(**item) for item in data]
        except:
            return []
    return []

@ui.page('/')
def main_page():
    
    words_list = load_data()

    @ui.refreshable
    def render_list():
        with ui.column().classes('w-full gap-2 mt-4 bg-zinc-700'):
            for item in words_list:
                with ui.row().classes('w-full items-center justify-between bg-zinc-700 rounded p-2'):
                    with ui.row().classes('gap-4'):
                        ui.label(item.english).classes('w-16 text-sm font-bold text-bg-red-200')
                        ui.label('–').classes('mx-2 text-bg-stone-600')
                        ui.label(item.russian).classes('italic text-sm text-bg-red-100')
                    ui.button(icon='delete', on_click=lambda i=item: remove_word(i)) \
                        .props('flat fab-mini color=bg-stone-300')

    async def add_word():
        text = input_field.value.strip().lower()
        if not text:
            return
        
        # search through the API
        if text in DICTIONARY_DB:
            translation = DICTIONARY_DB[text]
        try:
            
            translation = GoogleTranslator(source='en', target='ru').translate(text)
        except Exception as e:
            translation = 'ошибка'
            ui.notify(f'Ошибка: {e}', color='red')

        # Добавляем, Сохраняем и Обновляем
        words_list.append(WordPair(text, translation))
        save_data(words_list)
        input_field.value = ''
        render_list.refresh()

    def remove_word(item):
        words_list.remove(item)
        save_data(words_list) 
        render_list.refresh()

    # ui
    with ui.card().classes('w-96 mx-auto mt-10 p-6 bg-zinc-800'):
        ui.label('My dictionary').classes('text-2xl text-bg-gray-200 font-bold mx-auto')
        input_field = ui.input(label='English word').classes('w-full').props('bg-gray-500') \
            .on('keydown.enter', add_word)
        ui.button('Add', on_click=add_word).props('color=bg-red-950').classes('w-full mt-2')
        ui.separator().classes('my-4')
        render_list()


ui.run(native=True, dark=True, title="Dictionary App")

