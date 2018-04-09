# -*- coding: utf-8 -*-

import re
import traceback

import requests

from utils import init_logger


GB_CODE = 'gb2312'
GB_CODE = 'gbk'
GB_CODE = 'gb18030'

logger = init_logger('lottery')


def get_match_list(partition):

    url = 'http://trade.500.com/jczq/?date={:%Y-%m-%d}'.format(partition)
    match_pattern = re.compile('fid="(\d+)"')

    try:
        resp = requests.get(url)
        content = resp.content.decode(GB_CODE).encode('utf-8')
        match_list = sorted(match_pattern.findall(content))

    except:
        match_list = []
        logger.exception('Uncaught Exception [get_match_list]')
        print traceback.format_exc()

    return match_list


def get_match_info(match_id):

    url = 'http://odds.500.com/fenxi/shuju-{}.shtml'.format(match_id)
    url = 'http://odds.500.com/fenxi/yazhi-{}.shtml'.format(match_id)
    url = 'http://odds.500.com/fenxi/ouzhi-{}.shtml'.format(match_id)

    match_info_pattern = re.compile('hd_name.*?>(.*?)<')
    match_time_pattern = re.compile('game_time.*?>(.*?)<')

    try:
        resp = requests.get(url)
        content = resp.content.decode(GB_CODE).encode('utf-8')

        match_host, match_name, match_guest = match_info_pattern.findall(content)

        match_time, = match_time_pattern.findall(content)

        match_info = {
            'name':  match_name.strip(),
            'time':  match_time.strip(),
            'host':  match_host.strip(),
            'guest': match_guest.strip()
        }

    except:
        match_info = {'name': '', 'time': '','host': '', 'guest': ''}
        logger.exception('Uncaught Exception [get_match_list]')
        print traceback.format_exc()


    return match_info


def get_lottery_info(match_id):

    # url = 'http://odds.500.com/fenxi/ouzhi-{}.shtml'.format(match_id)
    url = 'http://odds.500.com/fenxi1/ouzhi.php?id={}&ctype=1&start=1&r=1&style=0&guojia=0&chupan=1&last=1'.format(match_id)

    try:
        resp = requests.get(url)
        content = ''.join(re.split(' |\t|\r|\n', resp.content))

        pattern_01   = re.compile('<p>(.*?)</p>')
        
        pattern_id   = re.compile('<p><inputid="ck(.*?)"type=.*?</p>')
        pattern_name = re.compile('<p>.*?<spanclass.*?>(.*?)<.*?</p>')

        pattern_rec  = re.compile('<table.*?</table>')
        pattern_cp   = re.compile('<trclass="tr_bdbtd_show_cp".*?</tr>')           # 初盘
        pattern_zp   = re.compile('<trclass="tr_bdbtd_show_cp".*?</tr>(.*?)</tr>') # 终盘
        pattern_val  = re.compile('<tdrow.*?>(.*?)</td>')

        list_id   = pattern_id.findall(content)
        list_name = pattern_name.findall(content)

        list_data = []
        data = []
        for idx, i in enumerate(pattern_rec.findall(content)):
            for j in pattern_cp.findall(i):
                data.extend(pattern_val.findall(j))
            for j in pattern_zp.findall(i):
                data.extend(pattern_val.findall(j))

            if (idx+1)%4 == 0:
                list_data.append(data)
                data = []

        lottery_info_dict = {}
        for i in range(len(list_id)):
            lottery_info_dict[i] = {
                'c_id':   list_id[i],               # 公司ID
                'c_name': list_name[i],             # 公司名字
                'o_s_w':  float(list_data[i][0]),   # 即时欧赔 odd 初盘 start 胜 win
                'o_s_d':  float(list_data[i][1]),   # 即时欧赔 odd 初盘 start 平 draw
                'o_s_l':  float(list_data[i][2]),   # 即时欧赔 odd 初盘 start 负 lose
                'o_e_w':  float(list_data[i][3]),   # 即时欧赔 odd 终盘 end   胜 win
                'o_e_d':  float(list_data[i][4]),   # 即时欧赔 odd 终盘 end   平 draw
                'o_e_l':  float(list_data[i][5]),   # 即时欧赔 odd 终盘 end   负 lose
                'p_s_w':  float(list_data[i][6].replace('%',''))/100,   # 即时概率 probability 初盘 start 胜 win
                'p_s_d':  float(list_data[i][7].replace('%',''))/100,   # 即时概率 probability 初盘 start 平 draw
                'p_s_l':  float(list_data[i][8].replace('%',''))/100,   # 即时概率 probability 初盘 start 负 lose
                'p_e_w':  float(list_data[i][9].replace('%',''))/100,   # 即时概率 probability 终盘 end   胜 win
                'p_e_d':  float(list_data[i][10].replace('%',''))/100,  # 即时概率 probability 终盘 end   平 draw
                'p_e_l':  float(list_data[i][11].replace('%',''))/100,  # 即时概率 probability 终盘 end   负 lose
                'r_s':    list_data[i][12],         # 返还率 return rate 初盘 start
                'r_e':    list_data[i][13],         # 返还率 return rate 终盘 end 
                'k_s_w':  float(list_data[i][14]),  # 即时凯利 kelly 初盘 start 胜 win
                'k_s_d':  float(list_data[i][15]),  # 即时凯利 kelly 初盘 start 平 draw
                'k_s_l':  float(list_data[i][16]),  # 即时凯利 kelly 初盘 start 负 lose
                'k_e_w':  float(list_data[i][17]),  # 即时凯利 kelly 终盘 end   胜 win
                'k_e_d':  float(list_data[i][18]),  # 即时凯利 kelly 终盘 end   平 draw
                'k_e_l':  float(list_data[i][19])   # 即时凯利 kelly 终盘 end   负 lose
            }

    except:
        lottery_info_dict = {}
        logger.exception('Uncaught Exception [get_match_list]')
        print traceback.format_exc()

    return lottery_info_dict


def main():

    import datetime

    import ujson as json

    partition = datetime.date.today()

    match_list = get_match_list(partition)
    logger.info('Get Match List [{:%Y-%m-%d}]'.format(partition))

    for match_id in match_list:

        match_info = get_match_info(match_id)
        print json.dumps(match_info, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Match Info [{}] [{}] [{}] [{} vs {}]'.format(match_id, match_info['name'], match_info['time'], match_info['host'], match_info['guest']))

        lottery_info_dict = get_lottery_info(match_id)
        # print json.dumps(lottery_info_dict, indent=4, sort_keys=True, ensure_ascii=False)
        logger.info('Get Lottery Info')

        break

    return


if __name__ == '__main__':
    main()
