#Install these packages (i.e newspaper3k, gnews, pandas) required to run the program. Commands to install the package are mentioned below.
#pip install newspaper3k
#pip install gnews
#pip install pandas


import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
from newspaper import Article
from newspaper import Config
from gnews import GNews
import csv
import os

def read_file_to_df(path):
    try:
        company_name_df = pd.read_csv(path)
        return company_name_df
    except:
        raise Exception("Please check again the file path")


def write_df_to_file(path,df):
    try:
        df.to_csv(path)
    except:
        raise Exception("Unable to write results to the file")


def extract_news(df,max_news_per_company):
    google_news = GNews(max_results=max_news_per_company)
    all_news_df = pd.DataFrame()
    for index, row in df.iterrows():

        cin = row["cin"]
        company_name = row["company_name"]
        
        if company_name != '':
            print(f'Searching news for {company_name} ...')

            #Extracting news for specific company using GNews
            news_list = google_news.get_news(company_name)
            print(len(news_list))
            news_df = pd.DataFrame(news_list)
            news_df['company_name'] = company_name
            all_news_df = pd.concat([all_news_df, news_df], ignore_index = True)
            #all_news_df.append(news_df)

        else:
            pass

    if all_news_df.empty:
        raise Exception("No new news found")
    else:
        selected_col_df = all_news_df[['company_name','title','url','published date','description']]
        df_nested_list = pd.json_normalize(all_news_df['publisher']).rename(columns = {"title": "source"})
        return pd.concat([selected_col_df, df_nested_list], axis=1, join='inner')[['company_name','title','url','published date','description','source']]


def main():
    directory = os.getcwd()
    input_file_path =  directory + "\\sample_companies.csv"
    output_file_path = directory + "\\companies_name.csv"
    max_news_per_company = 100
    try:
        input_file_df = read_file_to_df(input_file_path)
        company_names = extract_news(input_file_df,max_news_per_company)
        write_df_to_file(output_file_path,company_names)
    except Exception as e:
        print("Error message: " + str(e))


main()