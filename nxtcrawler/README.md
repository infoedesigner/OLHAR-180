# NXT Crawler

### Para rodar os diários

`python runner --start_date=2023-04-05 --end_date=2023-04-05`

No caso acima as datas são opcionais, se não passadas será considerado o dia atual

### Para rodar o crawler dos sites:

`scrapy crawl nxt_news`

O crawler acima precisa que o arquivo .env tenha as configurações da API do nxtweb, o exemplo de .env está no arquivo .env-sample
