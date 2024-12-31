import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krl.settings')
django.setup()

from lessons.models import Lesson

lessons_data = [
    {
        "num": 4,
        "title": "(nelläš) urokka",
        "slogan": "Yheštä opaštunnuošta kolmie opaštumatonda ei pie",
        "description": "Äijägo vuotta on?\r\nLugušanat",
        "is_enabled": True
    },
    {
        "num": 5,
        "title": "(viiješ) urokka",
        "slogan": "Ken ruaduo varajau, a kedä i ruado",
        "description": "Mi / Ken tämä on? Mit / Ket nämä ollah?\r\nMonikon nominativa (Ket? Mit?). Konsonantoin vaihoš",
        "is_enabled": True
    },
    {
        "num": 6,
        "title": "(kuuveš) urokka",
        "slogan": "Veri on vettä šagiembi",
        "description": "Pereh (nimišanat, tunnuššanat)\r\nGenetiva (Kenen?). Adessiva (Kellä?)",
        "is_enabled": True
    },
    {
        "num": 7,
        "title": "(šeiččimeš) urokka",
        "slogan": "Rodu eu redu",
        "description": "Omahizet (nimišanat, aziešanat)\r\nGenetiva (Kenen?). Adessiva (Kellä?). Aziešanoin muuttuačenda",
        "is_enabled": True
    },
    {
        "num": 8,
        "title": "(kahekšaš) urokka",
        "slogan": "Eu kaikki puut mečäššä yhenmuozet, ei što rahvaš",
        "description": "Ulgonägö. Cvietut\r\nMonikon nominativa. Adessiva (Kellä?)",
        "is_enabled": True
    },
    {
        "num": 9,
        "title": "(yhekšäš) urokka",
        "slogan": "Kuin elät, niin i kuulut",
        "description": "Ristikanžan taba\r\nTunnuššana (Mityš?). Komparativa. Superlativa",
        "is_enabled": True
    },
    {
        "num": 10,
        "title": "(kymmeneš) urokka",
        "slogan": "Ruado mieštä ei riko",
        "description": "Ruado\r\nEssiva (Kenä?). Translativa (Kekši?)",
        "is_enabled": True
    },
    {
        "num": 11,
        "title": "(yheštoista) urokka",
        "slogan": "Midä i maha – kaikki godiečou",
        "description": "Aziešanat\r\nAziešanoin muuttuačenda",
        "is_enabled": True
    },
    {
        "num": 12,
        "title": "(kaheštoista) urokka",
        "slogan": "Kanoinke laškieče, kukkoloinke nouže",
        "description": "Aiga. Ruadopäivä\r\nAziešanoin muuttuačenda. Iččiehizet aziešanat",
        "is_enabled": True
    },
    {
        "num": 13,
        "title": "(kolmaštoista) urokka",
        "slogan": "Tervehyš on kuldua kallehembi",
        "description": "Tervehyš\r\nPartitiva (Midä?)",
        "is_enabled": True
    },
    {
        "num": 14,
        "title": "(nelläštoista) urokka",
        "slogan": "Vuotta myöt’ lindu laulau",
        "description": "Šiä. Vuuven aijat. Kuut. Nedelin päivät. Suutkat. Konža?\r\nEssiva, adessiva. Aziešanoin muuttuačenda. Translativa (Miksi?)",
        "is_enabled": True
    },
    {
        "num": 15,
        "title": "(viiještoista) urokka",
        "slogan": "Čirozešša on hyvä, vielä parembi on omalla mualla",
        "description": "Kylä. Puut. Žiivatat da zvierit, linnut\r\nPaikkamuutokšet",
        "is_enabled": True
    },
    {
        "num": 16,
        "title": "(kuuveštoista) urokka",
        "slogan": "Jogo linnulla on oma pežo kallisʼ",
        "description": "Muutokšet. Abessiva (Kettä? Mittä?). Komitativa (Kenenke? Minke?)",
        "is_enabled": True
    },
    {
        "num": 17,
        "title": "(šeiččimeštoista) urokka",
        "slogan": "Koissa i šeinät paissah",
        "description": "Talo. Fatera. Miebeli\r\nEzi- da jälgišanat",
        "is_enabled": True
    },
    {
        "num": 18,
        "title": "(kahekšaštoista) urokka",
        "slogan": "Vuatteida myöten vaššatah, a hajuo myöten šuatetah",
        "description": "Vuattiet\r\nMuutokšet. Monikko",
        "is_enabled": True
    },
    {
        "num": 19,
        "title": "(yhekšäštoista) urokka",
        "slogan": "Kuni jalgane kapšau, šini šuuhut n’apšau",
        "description": "Kalat, marjat, šienet da gribat\r\nImperfekta. Neuvondašana (Konža?)",
        "is_enabled": True
    },
    {
        "num": 20,
        "title": "(kaheškymmeneš) urokka",
        "slogan": "Eu kaikki šuuh, midä šilmä nägöy",
        "description": "Šyömizet. Einehet da fruuktat\r\nObjektan muutokšet (akkuzativa da partitiva)",
        "is_enabled": True
    },
    {
        "num": 21,
        "title": "(kaheškymmenešenžimäne) urokka",
        "slogan": "Paistua vois’, vain mistä ois’",
        "description": "Šyömizen varuššanda\r\nAziešanoin muuttuačenda. Imperativa. Objekta",
        "is_enabled": True
    },
    {
        "num": 22,
        "title": "(kaheškymmeneštoine) urokka",
        "slogan": "Gostʼa kahičči ihaššuttau: tullešša da lähtiessä",
        "description": "Gostissa\r\nEzi- da jälgišanat. Neuvondašanat",
        "is_enabled": True
    },
    {
        "num": 23,
        "title": "(kaheškymmeneškolmaš) urokka",
        "slogan": "Mierošša kuin mereššä – kaikkie on",
        "description": "Matkuššanda\r\nKondicionala",
        "is_enabled": True
    },
    {
        "num": 24,
        "title": "(kaheškymmenešnelläš) urokka",
        "slogan": "Lebävö luuda ei katkua",
        "description": "Pruazniekat\r\nInfinitivat. Pričastijat",
        "is_enabled": True
    },
    {
        "num": 25,
        "title": "(kaheškymmenešviiješ) urokka",
        "slogan": "Hyvin ruata – uniloitta muata",
        "description": "",
        "is_enabled": True
    },
]

# Создание уроков
def create_lessons():
    for lesson_data in lessons_data:
        Lesson.objects.create(**lesson_data)
    print(f"Created {len(lessons_data)} lessons.")

if __name__ == "__main__":
    create_lessons()