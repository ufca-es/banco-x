import os
import sys
import subprocess

class Utils:

    def escolher_personalidade(self):
        print("\n--- Escolha a personalidade ---")
        print("1 - Sr.Bot (formal)")
        print("2 - Clara (engraçada)")
        print("3 - Byte (rude)")
        print("4 - Marcos (empreendedor)")
        opcao = input("Digite o número: ").strip()
        mapa = {
            "1": "formal",
            "2": "engracada",
            "3": "rude",
            "4": "empreendedor"
        }
        return mapa.get(opcao, "formal")
