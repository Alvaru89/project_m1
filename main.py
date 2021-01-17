import argparse
from p_acquisition.m_acquisition import acquire
from p_wrangling.m_wrangling import build_data
from p_reporting.m_reporting import report_csv

def argument_parser():
    """
    parse arguments to script
    """
    parser=argparse.ArgumentParser(description='pass csv file')
    parser.add_argument("-c","--country", help='specify country or type all', type=str)
    args=parser.parse_args()
    return args

def main(arguments):
    print("starting process")

    raw_df=acquire()
    clean_df=build_data(raw_df)

    if arguments.country!=None:
        country=arguments.country
        report_csv(clean_df,country)
    else:
        report_csv(clean_df)
    print('process completed')
    return

if __name__ == '__main__':
    print("starting pipeline")
    my_arguments= argument_parser()
    main(my_arguments)

    print('pipeline completed')