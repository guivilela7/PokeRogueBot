import time
import pyautogui
import keyboard
import pytesseract
import win32api, win32con
import pokebase as pb
from pytesseract import *
from PIL import Image
import difflib
import requests
import re

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

url = "https://pokeapi.co/api/v2/move?offset=0&limit=2000/"
poke_request = requests.get(url)
moves = poke_request.json()

# Lista com todos os moves de pokemon
pokemoves = [mov["name"] for mov in moves["results"]]

urlp = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=3000/"
poke_requestp = requests.get(urlp)
pokemons = poke_requestp.json()

# Lista com todos os nomes de pokemon
pokenames = [pok["name"] for pok in pokemons["results"]]

# Dicionario de efetividade
tipo_efetividade = {
    "normal": {
        "rock": 0.5, "ghost": 0, "steel": 0.5
    },
    "fire": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2
    },
    "water": {
        "fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5
    },
    "electric": {
        "water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5
    },
    "grass": {
        "fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5
    },
    "ice": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5
    },
    "fighting": {
        "normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5
    },
    "poison": {
        "grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2
    },
    "ground": {
        "fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2
    },
    "flying": {
        "electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5
    },
    "psychic": {
        "fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5
    },
    "bug": {
        "fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "steel": 0.5, "fairy": 0.5
    },
    "rock": {
        "fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5
    },
    "ghost": {
        "normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5
    },
    "dragon": {
        "dragon": 2, "steel": 0.5, "fairy": 0
    },
    "dark": {
        "fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5
    },
    "steel": {
        "fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2
    },
    "fairy": {
        "fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5
    }
}


# Descobrir qual o pokemon inimigo
def get_inimigo():
    # mudar região de acordo com o tamanho do monitor Grande = 220, 250, 200, 46 ; Pequeno = 270, 270, 220, 46
    img = pyautogui.screenshot(region=[230, 250, 200, 46])
    # img.show()
    saida = pytesseract.image_to_string(img, lang="pkmngba_en", config="--psm 7 -c tessedit_char_whitelist=' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'")
    if difflib.get_close_matches(saida, pokenames, n=1):
        return difflib.get_close_matches(saida, pokenames, n=1)
    else:
        return None


# Retorna uma lista com os tipos do pokemon
def get_types_inimigo():
    tipos = []

    nome = get_inimigo()
    aproxima = nome.pop()
    poke = pb.pokemon(aproxima.lower()).types

    for i in poke:
        tipos.append(str(i.type))

    return tipos


# Reconhecer estado do menu
# 0 = estado fight / 1 = estado ball / 2 = estado pokemon / 3 = estado run / None = nada encontrado
def menu_status():
    # img = pyautogui.screenshot(region=[1220, 840, 440, 170])
    # img.show()
    try:
        pyautogui.locateOnScreen("./Prints/fight.png", grayscale=True)
        return 0
    except pyautogui.ImageNotFoundException:
        try:
            pyautogui.locateOnScreen("./Prints/ball.png", grayscale=True)
            return 1
        except pyautogui.ImageNotFoundException:
            try:
                pyautogui.locateOnScreen("./Prints/pokemon.png", grayscale=True)
                return 2
            except pyautogui.ImageNotFoundException:
                try:
                    pyautogui.locateOnScreen("./Prints/run.png", grayscale=True)
                    return 3
                except pyautogui.ImageNotFoundException:
                    return None


# Tira screenshot do local com os ataques, organiza eles numa lista e retorna essa lista
def get_current_attacks():
    i = 0

    img = pyautogui.screenshot(region=[230, 845, 800, 160])
    # img.show()
    attacks = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'")
    current_poke_attacks = attacks.split()  # Coloca os resultados do image to string numa lista

    # Compara os resultados com a lista de todos os moves para corrigir erros de escrita e padronizar
    while i < len(current_poke_attacks):
        passa = current_poke_attacks.pop(0)
        move_certo = difflib.get_close_matches(passa, pokemoves, n=1)
        current_poke_attacks.append(move_certo)
        i = i + 1

    return current_poke_attacks


def escolhe_melhor_ataque():
    lista_atacks = get_current_attacks()
    tipos_inimigo = get_types_inimigo()
    dictlist = []
    maior_poder = 0
    melhor_ataque = None

    # Cria uma lista de dicionários com os 4 moves e seus nomes, poderes e tipos
    for i in range(len(lista_atacks)):
        move_name = str(lista_atacks.pop(0))
        move_name = re.sub(pattern=r"[\'\[\]]", repl='', string=move_name)
        dictlist.append(dict(name=move_name, power=pb.move(move_name).power, type=str(pb.move(move_name).type), acc=str(pb.move(move_name).accuracy)))

    for i in range(len(dictlist)-1):
        move_type = dictlist[i]["type"]
        efetividades = tipo_efetividade[move_type]
        for tipo in tipos_inimigo:
            if efetividades.get(tipo):
                newpower = dictlist[i]["power"] * efetividades.get(tipo)
                dictlist[i].update({"power": newpower})
        if dictlist[i]["power"] > maior_poder:
            maior_poder = dictlist[i]["power"]
            melhor_ataque = dictlist[i]["name"]

    return melhor_ataque


