import argparse
import datetime as dt

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from nxt_crawler.spiders.pe_recife import PeRecifeSpider, PeUFSpider
from nxt_crawler.spiders.ba_salvador import BaSalvadorSpider
from nxt_crawler.spiders.sp_sao_paulo import SpSaoPauloSpider
from nxt_crawler.spiders.am_manaus import AmManausSpider, AMUFSpider
from nxt_crawler.spiders.ce_fortaleza import CeFortalezaSpider
from nxt_crawler.spiders.rn_natal import RnNatalSpider
from nxt_crawler.spiders.pb_joao_pessoa import PbJoaoPessoaSpider, PbUFSpider
from nxt_crawler.spiders.al_maceio import AlMaceioSpider
from nxt_crawler.spiders.pi_teresina import PiTeresina
from nxt_crawler.spiders.pa_belem import PaBelemSpider
from nxt_crawler.spiders.rr_boa_vista import RrBoaVistaSpider
from nxt_crawler.spiders.ro_porto_velho import RoPortoVelho
from nxt_crawler.spiders.rj_rio_de_janeiro import RjRioDeJaneiroSpider
from nxt_crawler.spiders.ap_macapa import ApMacapaSpider
from nxt_crawler.spiders.rs_porto_alegre import RsPortoAlegreSpider
from nxt_crawler.spiders.sc_florianopolis import ScFlorianopolisSpider
from nxt_crawler.spiders.go_goiania import GoGoianiaSpider, GoUFSpider
from nxt_crawler.spiders.pr_curitiba import PrCuritibaSpider
from nxt_crawler.spiders.ms_campo_grande import MsCampoGrandeSpider
from nxt_crawler.spiders.mt_cuiaba import MtCuiabaSpider
from nxt_crawler.spiders.mg_belo_horizonte import MgBeloHorizonteSpider
from nxt_crawler.spiders.to_palmas import ToPalmasSpider
from nxt_crawler.spiders.ma_sao_luis import MaSaoLuisSpider
from nxt_crawler.spiders.df_brasilia import DfBrasiliaSpider, DfUFSpider
from nxt_crawler.spiders.es_vitoria import EsUFSpider, EsVitoriaSpider

parser = argparse.ArgumentParser(description='Crawler runner')
parser.add_argument('--start_date', help='Start date for crawlers')
parser.add_argument('--end_date', help='End date for crawlers')
args = parser.parse_args()

start_date = args.start_date
if start_date is None:
    start_date = dt.date.today().strftime('%Y-%m-%d')
end_date = args.end_date
if end_date is None:
    end_date = dt.date.today().strftime('%Y-%m-%d')

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    #yield runner.crawl(PeUFSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(PeRecifeSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(BaSalvadorSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(SpSaoPauloSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(AmManausSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(AMUFSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(AMUFSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(CeFortalezaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(RnNatalSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(PbJoaoPessoaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(PbUFSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(AlMaceioSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(PiTeresina, start_date=start_date, end_date=end_date)
    # yield runner.crawl(PaBelemSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(RrBoaVistaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(RoPortoVelho, start_date=start_date, end_date=end_date)
    # yield runner.crawl(RjRioDeJaneiroSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(ApMacapaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(RsPortoAlegreSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(ScFlorianopolisSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(BaSalvadorSpider, start_date=start_date, end_date=end_date)
    yield runner.crawl(GoGoianiaSpider, start_date=start_date, end_date=end_date)
    yield runner.crawl(GoUFSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(PrCuritibaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(MsCampoGrandeSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(MtCuiabaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(MgBeloHorizonteSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(ToPalmasSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(MaSaoLuisSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(DfBrasiliaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(DfUFSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(EsVitoriaSpider, start_date=start_date, end_date=end_date)
    # yield runner.crawl(EsUFSpider, start_date=start_date, end_date=end_date)
    reactor.stop()

crawl()
reactor.run()
