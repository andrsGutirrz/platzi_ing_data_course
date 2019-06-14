import argparse
import logging
from web_scrapper.common import config
import web_scrapper.news_page_objects as news


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logger.info(f'Start scraper for {host}')
    homepage = news.Homepage(news_site_uid, host)
    for link in homepage.article_links:
        print(link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choises = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choises
                        )
    args = parser.parse_args()
    _news_scraper(args.news_site)
