# -*- coding: utf-8 -*-

import ujson as json

from lottery import get_match_list
from lottery import get_match_info
from lottery import get_lottery_info

from utils import init_logger


logger = init_logger('portfolio')


def get_best_profit(item_w, item_d, item_l):

    def min_pay(item_w, item_d, item_l, p_w, p_d, p_l):
        """
        p_*: percent of item
        """
        
        profit = item_w['o_s_w'] * item_w['p_s_w'] * p_w + \
                 item_d['o_s_d'] * item_d['p_s_d'] * p_d + \
                 item_l['o_s_l'] * item_l['p_s_l'] * p_l

        return profit

    best_profit = 0
    best_p_w = None
    best_p_d = None
    best_p_l = None
    
    for i in range(101):
        for j in range(101-i):
            p_w = i/100.
            p_d = j/100.
            p_l = 1-p_w-p_d
            profit = min_pay(item_w, item_d, item_l, p_w, p_d, p_l)

            if profit > best_profit:
                best_profit = profit
                best_p_w = p_w
                best_p_d = p_d
                best_p_l = p_l

    portfolio = {
        'profit': best_profit,
        'item_w': item_w['c_name'],
        'item_d': item_d['c_name'],
        'item_l': item_l['c_name'],
        'p_w': p_w,
        'p_d': p_d,
        'p_l': p_l
    }

    return portfolio


def get_best_portfolio(lottery_info_dict):

    item_w = lottery_info_dict[0]
    item_d = lottery_info_dict[0]
    item_l = lottery_info_dict[0]

    for idx in lottery_info_dict:

        if item_w['o_s_w'] < lottery_info_dict[idx]['o_s_w']:
            item_w = lottery_info_dict[idx]

        if item_d['o_s_d'] < lottery_info_dict[idx]['o_s_d']:
            item_d = lottery_info_dict[idx]

        if item_l['o_s_l'] < lottery_info_dict[idx]['o_s_l']:
            item_l = lottery_info_dict[idx]

    portfolio = get_best_profit(item_w, item_d, item_l)

    return portfolio


def main():

    import datetime

    partition = datetime.date.today()

    match_list = get_match_list(partition)
    logger.info('Get Match List [{:%Y-%m-%d}]'.format(partition))

    for match_id in match_list:

        match_info = get_match_info(match_id)
        # print json.dumps(match_info, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Match Info [{}] [{}] [{}] [{} vs {}]'.format(match_id, match_info['name'], match_info['time'], match_info['host'], match_info['guest']))

        lottery_info_dict = get_lottery_info(match_id)
        # print json.dumps(lottery_info_dict, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Lottery Info')

        portfolio = get_best_portfolio(lottery_info_dict)
        # print json.dumps(portfolio, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Best Portfolio [profit: {}]'.format(portfolio['profit']))

        break

    return


if __name__ == '__main__':
    main()
