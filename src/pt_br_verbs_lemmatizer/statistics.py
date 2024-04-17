import pt_br_verbs_lemmatizer as ptbr_vl
import  time

def checkTime(verb : str,
              analyze : str = 'lemmatize' | 'checkduplicity') -> float:
    analyze = analyze.lower()
    if analyze == 'lemmatize':
        t1 = time.time()
        ptbr_vl.lemmatize(verb)
        time.sleep(0.1)
        t2 = time.time()
    elif analyze == 'checkduplicity':
        t1 = time.time()
        ptbr_vl.checkFlexVerbDuplicity(verb)
        time.sleep(0.1)
        t2 = time.time()
    exec_time = round(t2-t1-0.1,8)
    return exec_time


def getInfo(data_set : str = 'lemmas' | 'duplicity',
            search_type : str = 'inf_verbs' | 'flex_verbs',
            info : str = 'number' | 'list_of_verbs') -> int|str:
    pass


