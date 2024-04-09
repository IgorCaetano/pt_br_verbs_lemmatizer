import msgpack
import pkg_resources

dic_verbs_filepath = pkg_resources.resource_filename('pt_br_verbs_lemmatizer','dataset/dic_pt_br_verbs_lemma.msgpack')

dic_duplicated_flex_verbs_filepath = pkg_resources.resource_filename('pt_br_verbs_lemmatizer','dataset/dic_duplicated_flex_verbs.msgpack')

try:
    with open(dic_verbs_filepath,'rb') as f:
        verbs_dic = msgpack.unpackb(f.read())
        print('Verbs database loaded successfully.')
except Exception as e:
    error = f'{e.__class__.__name__}: {str(e)}'
    print(f'Something went wrong while openning our verbs dictionary:\n{error}')
    verbs_dic = None

try:
    with open(dic_duplicated_flex_verbs_filepath,'rb') as f:
        dic_duplicated_flex_verbs = msgpack.unpackb(f.read())
        print('Duplicated flex verbs database loaded successfully.')
except Exception as e:
    error = f'{e.__class__.__name__}: {str(e)}'
    print(f'Something went wrong while openning our duplicated flex verbs dictionary:\n{error}')
    dic_duplicated_flex_verbs = None


def lemmatize(verb : str,
              consider_duplicity : bool = False,
              silence : bool = True) -> str:
    """
    This function will give you the infinitive form of the verb (if it's inside our dataset).

    Params:
    -------
    - :param verb: String containing the verb you want to lemmatize.

    Returns:
    --------
    - :return: String with the verb lemmatized (infinitive form), if it's inside our dataset. Otherwise it will return the originally verb gave as input.
    """
    verb_duplicated = False
    if consider_duplicity:
        if checkFlexVerbDuplicity(verb):
            verb_duplicated = True
    if not verb_duplicated:
        if verbs_dic:
            verb = verb.lower()
            
            list_of_verb_type_keys = ['irregular','regular']

            first_3_letters = verb[0:3]
            len_of_verb = str(len(verb))

            for verb_type in list_of_verb_type_keys:
                if verb_type in verbs_dic.keys():
                    if first_3_letters in verbs_dic[verb_type].keys():
                        if len_of_verb in verbs_dic[verb_type][first_3_letters]:
                            for flex_verb, infinitive_verb in verbs_dic[verb_type][first_3_letters][len_of_verb]:
                                if flex_verb == verb:
                                    return infinitive_verb
        return verb
    else:
        if not silence:
            print(f"! Verb: {verb} was consider with duplicity (there are more than one infinitive verb that has this flex verb as well), so it wasn't lemmatized.")
        return verb

def checkFlexVerbDuplicity(flex_verb : str) -> bool:
    if dic_duplicated_flex_verbs:
        try:
            first_two_letters = flex_verb[0:2]
            length = str(len(flex_verb))        
            if flex_verb in dic_duplicated_flex_verbs[first_two_letters][length]:
                return True
            else:
                return False
        except Exception as e:
            return False
    return False