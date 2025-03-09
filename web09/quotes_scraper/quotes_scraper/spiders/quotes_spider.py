import scrapy
import json
from pathlib import Path

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com"]

    authors = {}

    def parse(self, response):
        for quote in response.css("div.quote"):
            author_name = quote.css("span small::text").get()
            quote_text = quote.css("span.text::text").get()
            tags = quote.css("div.tags a.tag::text").getall()

            # Додаємо автора до списку, якщо його ще немає
            if author_name not in self.authors:
                author_link = quote.css("span a::attr(href)").get()
                yield response.follow(author_link, self.parse_author)

            yield {
                "author": author_name,
                "quote": quote_text,
                "tags": tags
            }

        # Переходимо на наступну сторінку, якщо вона є
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        name = response.css("h3.author-title::text").get().strip()
        born_date = response.css("span.author-born-date::text").get()
        born_location = response.css("span.author-born-location::text").get()
        description = " ".join(response.css("div.author-description::text").getall()).strip()

        self.authors[name] = {
            "fullname": name,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }

    def closed(self, reason):
        # Зберігаємо quotes.json
        quotes_file = Path("quotes.json")
        quotes_data = list(self.crawler.stats.get_value("item_scraped_count") or [])

        with quotes_file.open("w", encoding="utf-8") as f:
            json.dump(quotes_data, f, indent=4, ensure_ascii=False)

        # Зберігаємо authors.json
        authors_file = Path("authors.json")
        with authors_file.open("w", encoding="utf-8") as f:
            json.dump(list(self.authors.values()), f, indent=4, ensure_ascii=False)
