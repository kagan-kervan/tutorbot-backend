knowledge = {
    "fonksiyon": "Fonksiyon, her girdi değerine yalnızca bir çıktı değerini eşleyen bir yapıdır. Örnek: f(x) = 2x + 3",
    "üçgen": "Üçgen, üç kenarı ve üç açısı olan kapalı bir geometrik şekildir.",
    "fiil": "Fiil, eylemi ya da oluşu bildiren kelime türüdür."
}

def get_context(question: str) -> str:
    for keyword in knowledge:
        if keyword in question.lower():
            return knowledge[keyword]
    return "Bu konuda elimde bilgi yok."