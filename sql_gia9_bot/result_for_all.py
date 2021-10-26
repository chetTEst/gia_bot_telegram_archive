import config
import utils
from time import time,sleep
my_list=['567741447','427106962','443860076','413909436','594703625','597527213','528730255','361936105','536229784','429733806','389423025']
for ids in my_list:
    utils.check_result_f(ids)
    sleep(1)
    utils.check_stat_f(ids)
    sleep(1)