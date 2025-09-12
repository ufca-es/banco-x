def escolher_personalidade():
    print("\n--- Escolha a personalidade ---")
    print("1 - Sr.Bot (formal)")
    print("2 - Clara (engracada)")
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
