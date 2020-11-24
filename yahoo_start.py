import argparse
from db import connection
from yahoo.api import Yahoo
from datetime import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Yahoo stocks parser')
    parser.add_argument('-c', '--company', help='The company name to be parsed)', required=True)
    parser.add_argument('-o', '--out', help='Folder where downloaded CSV  files will be placed)', required=True)
    parameters = parser.parse_args()
    company_name = parameters.company
    out_path = parameters.out
    print(f'Start processing for company: {company_name} at {datetime.utcnow()}')
    ya = Yahoo(connection=connection, output_folder=out_path)
    found_companies = ya.find_company_by_name(company_name=company_name)
    if found_companies['quotes']:
        company_symbol = found_companies['quotes'][0]['symbol']
        metadata = ya.get_company_metadata(company_symbol=company_symbol)
        print(f'metadata: {metadata}')
        if not metadata['chart']['error']:
            start_date = metadata['chart']['result'][0]['meta']['firstTradeDate']
            finish_date = int(datetime.utcnow().timestamp())
            print(f"First Trade Date:{ya.unixtimestamp_to_date(metadata['chart']['result'][0]['meta']['firstTradeDate'])}")
            out_file = ya.download_hystorical_csv_file(company_symbol=company_symbol, start_date=start_date,
                                                       finish_date=finish_date)
            df = ya.add_3day_before_change_to_csv_file(company_symbol, out_file)
            ya.save_data_to_db(type='historical', data=df)
            last_news = ya.get_last_news(company_symbol)
            ya.save_data_to_db(type='news', data=last_news)
    print(f'Process was finished at {datetime.utcnow()}')



