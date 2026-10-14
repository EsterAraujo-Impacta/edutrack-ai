print("Hello, World!")
import sys

# Garante compatibilidade UTF-8 no terminal Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_cat_face(message: str) -> tuple[str, str, str]:
    msg = message.lower()
    
    # Detecção de sentimentos/intenção por palavras-chave
    if any(word in msg for word in ["feliz", "amor", "amo", "gosto", "legal", "bom", "obrigado", "maravilha", "lindo", ":)", "s2", "<3"]):
        eyes = "^.^"
        chest = " <3 "
        status = "Feliz / Apaixonado"
    elif any(word in msg for word in ["triste", "choro", "chorar", "mal", "ruim", "depre", "aff", ":(", "t.t", "snif"]):
        eyes = "T.T"
        chest = " ^ "
        status = "Triste"
    elif any(word in msg for word in ["bravo", "raiva", "odeio", "odio", "irritado", "nervoso", ">:("]):
        eyes = ">.<"
        chest = " # "
        status = "Bravo"
    elif any(word in msg for word in ["uau", "nossa", "eita", "surpreso", "chocado", "omg", ":o", ":O"]):
        eyes = "o.O"
        chest = " o "
        status = "Surpreso"
    elif any(word in msg for word in ["sono", "dormir", "cansado", "preguica", "preguiça", "zzz"]):
        eyes = "-.-"
        chest = " z "
        status = "Com sono"
    elif any(word in msg for word in ["kkk", "haha", "rsrs", "piada", "engracado", "engraçado", ";)"]):
        eyes = "^.~"
        chest = " ^ "
        status = "Divertido"
    elif any(word in msg for word in ["duvida", "dúvida", "humm", "como", "porque", "por que", "?"]):
        eyes = "?.?"
        chest = " ? "
        status = "Curioso"
    else:
        eyes = "o.o"
        chest = " ^ "
        status = "Neutro"
        
    return eyes, chest, status

def draw_cat(message: str):
    eyes, chest, status = get_cat_face(message)
    bubble_line = "-" * (len(message) + 2)
    
    cat = f"""
     +{bubble_line}+
     | {message} |   [{status}]
     +{bubble_line}+
        \\
         \\  /\\_/\\  
           ( {eyes} ) 
            >{chest}<
           /|   |\\
          (_|   |_)
    """
    print(cat)

def main():
    print("=" * 50)
    print("  Gatinho Interativo de Expressões ")
    print("  Digite sua mensagem (ou 'sair' para encerrar)")
    print("=" * 50)
    
    # Demonstração inicial
    draw_cat("Olá! Envie uma mensagem para ver minha reação!")
    
    while True:
        try:
            user_msg = input("\nVocê: ").strip()
            if not user_msg:
                continue
            if user_msg.lower() in ["sair", "exit", "quit"]:
                print("\n /\\_/\\ \n( ^.^)/ Tchauzinho!")
                break
            
            draw_cat(user_msg)
        except (KeyboardInterrupt, EOFError):
            print("\n\nAté logo!")
            break

if __name__ == "__main__":
    main()


