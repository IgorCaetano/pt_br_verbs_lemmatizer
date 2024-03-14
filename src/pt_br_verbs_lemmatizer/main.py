import msgpack
import pkg_resources

dic_verbs_filepath = pkg_resources.resource_filename('pt_br_verbs_lemmatizer','dataset/dic_pt_br_verbs_lemma.msgpack')

try:
    with open(dic_verbs_filepath,'rb') as f:
        verbs_dic = msgpack.unpackb(f.read())
        print('Dataset carregado com sucesso.')
except Exception as e:
    error = f'{e.__class__.__name__}: {str(e)}'
    print(f'Something went wrong while openning our verbs dictionary:\n{error}')
    verbs_dic = None


def lemmatize(verb : str) -> str:
    """
    This function will give you the infinitive form of the verb (if it's inside our dataset).

    Params:
    -------
    - :param verb: String containing the verb you want to lemmatize.

    Returns:
    --------
    - :return: String with the verb lemmatized (infinitive form), if it's inside our dataset. Otherwise it will return the originally verb gave as input.
    """
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