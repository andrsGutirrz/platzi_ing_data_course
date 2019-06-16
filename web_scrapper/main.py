import argparse
import logging
import re
from requests.exceptions import HTTPError, InvalidSchema
from urllib3.exceptions import MaxRetryError
from web_scrapper.common import config
import web_scrapper.news_page_objects as news


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _news_scraper(news_site_uid): #news_site_uid: eluniversal
    host = config()['news_sites'][news_site_uid]['url'] # http://www.eluniversal.com.mx
    logger.info(f'Start scraper for {host}')
    homepage = news.Homepage(news_site_uid, host)
    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('ARTICLE FETCHED!!')
            articles.append(article)
            print(article.title)

    print(len(articles))


def _fetch_article(news_site_uid, host, link):
    logger.info(f'START FETCHING ARTICLE AT {link}')

    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError, InvalidSchema) as e:
        logger.warning(f'Error while fetching: {e}',exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None

    return article


def _build_link(host, link):
    link_spread = link['href']
    if is_well_formed_link.match(link_spread):
        return link
    elif is_root_path.match(link_spread):
        return f'{host}{link_spread}'
    else:
        f'{host}/{link}'


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
