import pkg_resources

from decouple import config

from shutil import which

#SELENIUM_DRIVER_NAME = 'chrome'
#SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
#SELENIUM_DRIVER_ARGUMENTS = ['--headless']

#DOWNLOADER_MIDDLEWARES = {
#    'scrapy_selenium.SeleniumMiddleware': 800
#}

BOT_NAME = "nxt_crawler"
SPIDER_MODULES = ["nxt_crawler.spiders"]
NEWSPIDER_MODULE = "nxt_crawler.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "nxt_crawler.pipelines.GazetteDateFilteringPipeline": 100,
    "nxt_crawler.pipelines.DefaultValuesPipeline": 200,
    "nxt_crawler.pipelines.QueridoDiarioFilesPipeline": 300,
}

# DOWNLOADER_CLIENTCONTEXTFACTORY = 'nxt_crawler.middlewares.LegacyConnectContextFactory'

DOWNLOAD_TIMEOUT = 360

DOWNLOAD_DELAY = 0.5

FILES_STORE = config("FILES_STORE", default="data")
MEDIA_ALLOW_REDIRECTS = True

EXTENSIONS = {
    # "spidermon.contrib.scrapy.extensions.Spidermon": 500,
    "nxt_crawler.extensions.StatsPersist": 600,
}
SPIDERMON_ENABLED = config("SPIDERMON_ENABLED", default=True, cast=bool)
SPIDERMON_VALIDATION_SCHEMAS = [
    pkg_resources.resource_filename("nxt_crawler", "resources/gazette_schema.json")
]

SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True
SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = True
# SPIDERMON_SPIDER_CLOSE_MONITORS = ("nxt_crawler.monitors.SpiderCloseMonitorSuite",)
SPIDERMON_MAX_ERRORS = 0
SPIDERMON_MAX_ITEM_VALIDATION_ERRORS = 0

SPIDERMON_DISCORD_FAKE = config("SPIDERMON_DISCORD_FAKE", default=True, cast=bool)
SPIDERMON_DISCORD_WEBHOOK_URL = config(
    "SPIDERMON_DISCORD_WEBHOOK_URL", default="<DISCORD_WEBHOOK_URL>"
)

QUERIDODIARIO_DATABASE_URL = config(
    "QUERIDODIARIO_DATABASE_URL", default="sqlite:///querido-diario.db"
)
QUERIDODIARIO_MAX_REQUESTS_ITEMS_RATIO = 5
QUERIDODIARIO_MAX_DAYS_WITHOUT_GAZETTES = 5

# These settings are needed only when storing downloaded files
# in a S3 bucket
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_ENDPOINT_URL = config("AWS_ENDPOINT_URL", default="")
AWS_REGION_NAME = config("AWS_REGION_NAME", default="")
FILES_STORE_S3_ACL = config("FILES_STORE_S3_ACL", default="public-read")


NXT_TOKEN = config('NXT_TOKEN', default='')
NXT_API_URL = config('NXT_API_URL', default='http://local.agencianxt.com.br:8000/')

LOG_FILE = config('LOG_FILE', default=None)

