import json
from models import Author, Quote

def load_authors():
    with open("authors.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            author = Author(**item)
            author.save()

def load_quotes():
    with open("quotes.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            author = Author.objects(fullname=item["author"]).first()
            if author:
                quote = Quote(tags=item["tags"], author=author, quote=item["quote"])
                quote.save()

if __name__ == "__main__":
    load_authors()
    load_quotes()
    print("Дані завантажено в MongoDB!")
