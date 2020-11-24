import os
import requests
import datetime
import pandas as pd
from util.utils import mkdir_p
from lxml.html import fromstring


class Yahoo:
    BASE_URL = 'https://finance.yahoo.com'
    XPATH_LAST_NEWS = '//div[contains(@id, "quoteNews") and @data-locator="subtree-root"]//ul//li//h3//a'

    def __init__(self, connection, output_folder, user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'):
        self.connection = connection
        self.output_folder = os.path.abspath(output_folder)
        self.user_agent = user_agent
        self.session = requests.Session()
        mkdir_p(self.output_folder)


    def _do_get_request(self, url, headers, params, json_data=True):
        status = 0
        data = {}
        # headers_before = self.session.headers
        self.session.headers.update(headers)
        try:
            response = self.session.get(url, headers=headers, params=params)
            status = response.status_code
            if status == 200:
                if json_data:
                    data = response.json()
                else:
                    data = response.content
        except Exception as exc:
            print(f'Exception: {exc}')
        finally:
            # self.session.headers = headers_before
            return status, data

    def _do_download_request(self, url, output_file, json_data=True):
        try:
            with self.session.get(url, stream=True) as response:
                with open(output_file, 'wb') as f:
                    for part in response.iter_content(chunk_size=16384):
                        f.write(part)
        except Exception as exc:
            print(f'Download exception: {exc}')
            return False
        else:
            return True


    def find_company_by_name(self, company_name):
        headers = {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://finance.yahoo.com/',
            'Origin': 'https://finance.yahoo.com',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

        params = (
            ('q', company_name.lower()),
            ('lang', 'en-US'),
            ('region', 'US'),
            ('quotesCount', '6'),
            ('newsCount', '4'),
            ('enableFuzzyQuery', 'false'),
            ('quotesQueryId', 'tss_match_phrase_query'),
            ('multiQuoteQueryId', 'multi_quote_single_token_query'),
            ('newsQueryId', 'news_cie_vespa'),
            ('enableCb', 'true'),
            ('enableNavLinks', 'true'),
            ('enableEnhancedTrivialQuery', 'true'),
        )

        status, data = self._do_get_request(url = 'https://query2.finance.yahoo.com/v1/finance/search',
                                            headers=headers,
                                            params=params
                                            )
        if status:return data
        else:return {}


    def get_company_metadata(self, company_symbol):
        headers = {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://finance.yahoo.com/quote/ZUO/',
            'Origin': 'https://finance.yahoo.com',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

        params = (
            ('region', 'US'),
            ('lang', 'en-US'),
            ('includePrePost', 'false'),
            ('interval', '2m'),
            ('range', '1d'),
            ('corsDomain', 'finance.yahoo.com'),
            ('.tsrc', 'finance'),
        )

        status, data = self._do_get_request(url = f'https://query1.finance.yahoo.com/v8/finance/chart/{company_symbol}',
                                            headers=headers,
                                            params=params
                                            )
        if status:return data
        else:return {}

    @staticmethod
    def unixtimestamp_to_date(unixtimestamp):
        return datetime.datetime.utcfromtimestamp(unixtimestamp)
        # .strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def date_to_unixtimestamp(date):
        return date.timestamp()

    def download_hystorical_csv_file(self, company_symbol, start_date, finish_date):
        download_url = f'https://query1.finance.yahoo.com/v7/finance/download/{company_symbol}?period1={start_date}&' \
                       f'period2={finish_date}&interval=1d&events=history&includeAdjustedClose=true'
        output_file = f"{company_symbol}_{self.unixtimestamp_to_date(start_date).strftime('%Y%m%d%H%M%S')}_" \
                      f"{self.unixtimestamp_to_date(finish_date).strftime('%Y%m%d%H%M%S')}.csv"
        full_file_name = os.path.join(self.output_folder, output_file)
        if self._do_download_request(download_url, full_file_name):
            return full_file_name
        else:
            return None

    def add_3day_before_change_to_csv_file(self, company_symbol, path_to_csf_file):
        df = pd.read_csv(path_to_csf_file)
        df.sort_values('Date', ascending=False, inplace=True)
        df['3day_before_change'] = 0
        df['Symbol'] = company_symbol
        for index, row in df.iterrows():
            dt = datetime.datetime.strptime(row['Date'], '%Y-%m-%d') - datetime.timedelta(days=3)
            found_val = df.loc[df['Date'] == dt.strftime('%Y-%m-%d'), ['Close']]
            if not found_val.empty:
                val_3_days_ago =  found_val['Close'].values[0]
                df.loc[index, '3day_before_change'] = df.loc[index, 'Close']/val_3_days_ago
        return df

    def save_data_to_db(self, type, data):
        db_res = None
        if type.lower() == 'historical':
            data.to_sql('tmp_yahoo_historical', self.connection.get_engine(), if_exists='replace', index=False)
            db_res = self.connection.execute_sql(
                f'''INSERT INTO yahoo_historical  (Date, Symbol, Open, High, Low, Close, `Adj Close`, Volume, 3day_before_change)
                    SELECT Date, Symbol, Open, High, Low, Close, `Adj Close`, Volume, 3day_before_change
                    FROM tmp_yahoo_historical as tmp
                    ON DUPLICATE KEY UPDATE
                        Open = tmp.Open,  
                        High = tmp.High, 
                        Low = tmp.Low, 
                        Close = tmp.Close, 
                        `Adj Close` = tmp.`Adj Close`, 
                        Volume = tmp.Volume, 
                        3day_before_change = tmp.3day_before_change;
            ''')
        elif type.lower() == 'news':
            df = pd.DataFrame(data)
            df.to_sql('tmp_yahoo_news', self.connection.get_engine(), if_exists='replace', index=False)
            db_res = self.connection.execute_sql(
                f'''INSERT INTO yahoo_news  (Symbol, Link, Title)
                    SELECT Symbol, Link, Title
                    FROM tmp_yahoo_news as tmp
                    ON DUPLICATE KEY UPDATE
                        Symbol = tmp.Symbol,  
                        Link = tmp.Link, 
                        Title = tmp.Title;
            ''')
        return db_res

    def get_last_news(self, company_symbol):
        news_list = []
        url = f'https://finance.yahoo.com/quote/{company_symbol}?p={company_symbol}&.tsrc=fin-srch'
        result, data = self._do_get_request(url=url, headers={}, params=(), json_data=False)
        if result:
            tree = fromstring(data)
            for article in tree.xpath(Yahoo.XPATH_LAST_NEWS):
                link = article.get('href')
                title = article.xpath('.//text()')[0]
                news_list.append({'symbol':company_symbol, 'link':Yahoo.BASE_URL + link, 'title':title})
        return news_list






