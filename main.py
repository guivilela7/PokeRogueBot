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

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# preciso manter info de: vida, moves,

# Lista de todos os nomes de pokemon
data = pandas.read_csv("Pokemon.csv")
pokenames = data["name"].values.tolist()


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
def menu_status():
    img = pyautogui.screenshot(region=[220, 250, 200, 46])


time = ["tinkatink"]

