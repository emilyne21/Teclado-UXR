
class Category(object):
    def __init__(self, id, label, icon, color, items):
        self.id = id
        self.label = label
        self.icon = icon         
        self.color = color     
        self.items = items


MAX_GRANDE = 15     

CATEGORIES = [
    # Tablero de elección original: necesidades básicas
    Category("necesidades", "NECESIDADES", "yo", (214, 102, 20), [
        "yo", "quiero", "comer", "beber", "bano",
        "dormir", "duchar", "musica", "tele", "pasear",
        "jugar", "hablar", "leer", "ordenador", "videojuegos",
    ]),
    Category("personas", "PERSONAS", "mama", (196, 150, 0), [
        "yo", "tu", "mama", "papa", "hermano",
        "abuelo", "abuela", "amigo", "profe", "medico",
        "nino", "nina", "bebe",
    ]),
    Category("acciones", "ACCIONES", "correr", (46, 139, 87), [
        "ir", "venir", "ver", "escuchar", "dar",
        "abrir", "cerrar", "parar", "escribir", "abrazar",
        "cantar", "bailar", "correr", "sentarse", "vestirse",
    ]),
    Category("comida", "COMIDA", "manzana", (192, 57, 43), [
        "manzana", "platano", "uvas", "naranja", "zanahoria",
        "pan", "queso", "huevo", "pollo", "pescado",
        "pasta", "sopa", "pizza", "patatas", "yogur",
    ]),
    Category("bebida", "BEBIDA Y POSTRES", "agua", (41, 128, 185), [
        "agua", "leche", "zumo", "refresco", "te",
        "cafe", "cacao", "batido", "galleta", "helado",
        "tarta",
    ]),
    Category("emociones", "EMOCIONES", "feliz", (142, 68, 173), [
        "feliz", "risa", "triste", "enfadado", "miedo",
        "sorpresa", "cansado", "aburrido", "carino", "enfermo",
        "tranquilo", "nervioso", "verguenza",
    ]),
    Category("lugares", "LUGARES", "casa", (22, 150, 130), [
        "casa", "colegio", "parque", "supermercado", "hospital",
        "playa", "piscina", "cocina", "habitacion", "salon",
        "coche", "autobus", "bano",
    ]),
    Category("respuestas", "RESPUESTAS", "si", (190, 70, 140), [
        "si", "no", "hola", "adios", "gracias",
        "porfavor", "perdon", "mas", "acabado", "nose",
        "bien", "mal", "ayuda", "otravez", "esperar",
    ]),
    Category("salud", "SALUD", "fiebre", (84, 98, 120), [
        "duele", "cabeza", "tripa", "garganta", "fiebre",
        "medicina", "tos", "frio", "calor", "hambre",
        "sed", "tirita", "lavar",
    ]),
]

BY_ID = {c.id: c for c in CATEGORIES}


def check(icons):
    """Devuelve la lista de ids de las páginas que no existen en `icons`."""
    return sorted({i for c in CATEGORIES for i in c.items if i not in icons} |
                  {c.icon for c in CATEGORIES if c.icon not in icons})