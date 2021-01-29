import argparse
import os
from p_acquisition.m_acquisition import acquire, acquire_bonus
from p_wrangling.m_wrangling import build_data, build_data_bonus
from p_reporting.m_reporting import report_csv, report_csv_bonus

def argument_parser():
    """
    parse arguments to script
    """
    parser=argparse.ArgumentParser(description='pass csv file')
    parser.add_argument("-c","--country", help='specify country or type all', type=str)
    parser.add_argument("-b", "--bonus", help='specify bonus 1 or 2', type=str)
    parser.add_argument("-d", "--delete", help='specify Y or y', type=str)
    args=parser.parse_args()
    return args

def main(arguments):
    print("starting process")
    if arguments.delete != None:
        if arguments.delete.lower() == 'y':
            folder= "data"
            files = os.listdir(folder)
            csv_files = [file for file in files if file.endswith(".csv")]
            for file in csv_files:
                path_to_file = os.path.join(folder, file)
                os.remove(path_to_file)
    if arguments.bonus!=None:
        try:
            bonus=int(arguments.bonus)
            if bonus!=1 and bonus!=2:
                raise ValueError("Sorry, bonus argument only supports the values: \'1\' or \'2\'")
        except:
            raise ValueError("Sorry, bonus argument only supports the values: \'1\' or \'2\'")
        print(f'BONUS TIME!\nBonus {bonus} selected!')
        bonus_df=acquire_bonus()
        result=build_data_bonus(bonus_df,bonus)
        report_csv_bonus(result,bonus)

    else:
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