# -*- coding: utf-8 -*-

import datetime

import ujson as json

from lottery import get_match_list
from lottery import get_match_info
from lottery import get_lottery_info
from portfolio import get_best_portfolio
from utils import init_logger


logger = init_logger('main')


def main():
    partition = datetime.datetime.strptime('2018-03-26', '%Y-%m-%d')
    partition = datetime.date.today()

    match_list = get_match_list(partition)
    logger.info('Get Match List [{:%Y-%m-%d}]'.format(partition))

    for match_id in match_list[10:20]:

        match_info = get_match_info(match_id)
        # print json.dumps(match_info, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Match Info [{}] [{}] [{}] [{} vs {}]'.format(match_id, match_info['name'], match_info['time'], match_info['host'], match_info['guest']))

        lottery_info_dict = get_lottery_info(match_id)
        # print json.dumps(lottery_info_dict, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Lottery Info')

        portfolio = get_best_portfolio(lottery_info_dict)
        print json.dumps(portfolio, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Best Portfolio [profit: {}]'.format(portfolio['profit']))

    return


if __name__ == '__main__':
    main()
