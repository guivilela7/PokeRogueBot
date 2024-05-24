import time
import pyautogui
import keyboard
import pytesseract
import win32api, win32con
import pokebase as pb
from pytesseract import *
from PIL import Image
import csv
import pandas
import difflib
import requests

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

url = "https://pokeapi.co/api/v2/move?offset=0&limit=2000/"
poke_request = requests.get(url)
moves = poke_request.json()

# preciso manter info de: vida, moves,

# Lista de todos os nomes de pokemon
data = pandas.read_csv("Pokemon.csv")
pokenames = data["name"].values.tolist()

# Lista com todos os moves de pokemon
pokemoves = [mov["name"] for mov in moves["results"]]


# Descobrir qual o pokemon inimigo
def get_inimigo():
    img = pyautogui.screenshot(region=[220, 250, 200, 46]) # mudar região de acordo com o tamanho do monitor
    # img.show()
    saida = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'")
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

    for type in poke:
        tipos.append(type.type)

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

