import scrapy

from scrapy.loader import ItemLoader

from ..items import EpirusbankItem
from itemloaders.processors import TakeFirst


class EpirusbankSpider(scrapy.Spider):
	name = 'epirusbank'
	start_urls = ['https://www.epirusbank.com/blog']

	def parse(self, response):
		post_links = response.xpath('//div[@class="blog_box_desc"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//section[@class="pages_body"]//h1/text()').get()
		description = response.xpath('//*[(@id = "ajaxcontent")]//li//text()[normalize-space()] | //h2//text()[normalize-space()] | //*[contains(concat( " ", @class, " " ), concat( " ", "blog_view", " " ))]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="created_date"]/text()').get()

		item = ItemLoader(item=EpirusbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
