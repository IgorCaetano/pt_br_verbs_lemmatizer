import msgpack
import pkg_resources

dic_verbs_filepath = pkg_resources.resource_filename('pt_br_verbs_lemmatizer','dataset/dic_pt_br_verbs_lemma.msgpack')

dic_duplicated_flex_verbs_filepath = pkg_resources.resource_filename('pt_br_verbs_lemmatizer','dataset/dic_duplicated_flex_verbs.msgpack')

# Opening/loading dictionary of verbs for lemmatization
try:
    with open(dic_verbs_filepath,'rb') as f:
        verbs_dic = msgpack.unpackb(f.read(), raw=False, use_list=True, strict_map_key=False)
        print('Verbs database loaded successfully.')
except Exception as e:
    error = f'{e.__class__.__name__}: {str(e)}'
    print('\n'+'-'*100+'\n'+f'! Something went wrong while openning our verbs dictionary:\n{error}'+'\n'+'-'*100+'\n')
    verbs_dic = None

# Opening/loading dictionary of duplicated/ambiguous verbs
try:
    with open(dic_duplicated_flex_verbs_filepath,'rb') as f:
        dic_duplicated_flex_verbs = msgpack.unpackb(f.read(), raw=False, use_list=False, strict_map_key=False)
        print('Duplicated flex verbs database loaded successfully.')
except Exception as e:
    error = f'{e.__class__.__name__}: {str(e)}'
    print('\n'+'-'*100+'\n'+f'! Something went wrong while openning our duplicated flex verbs dictionary:\n{error}'+'\n'+'-'*100+'\n')
    dic_duplicated_flex_verbs = None


def modifyDicAmbiguousVerbs(type : str,
                            verbs : list[str] | list[tuple[str,str]],
                            silence : bool = True) -> None:
    """
    This function will modify our datasets based on your desires, changing what you asks to change.

    Params:
    -------
    - type: String that will say wheter you are wanting to change an entire list of flex verbs based on the infinitive verb you give or change an especific flex verb based on a tuple of (flex_verb, infinitive_verb). So you need to choose between type="infinitive" or type="flex".
    - verbs: list of strings containing the infinitive verbs, if you choose type="infinitive" or list of tuple strings contaning the tuple of flex verb and the infinitive verb associated with the flex verb if you choose type="flex".
    - silece: Bool that will give the decision to print or don't print when a problem show up.
    
    Returns:
    --------
    - return: None. This function doesn't return anything, it just changes the dictionaries.
    """
    global dic_duplicated_flex_verbs
    global verbs_dic

    if dic_duplicated_flex_verbs:
        type = type.lower()
        lista_verbs_to_remove_flex_inf = []
        if type == 'infinitive':
            for verb in verbs:
                verb = verb.lower()
                lista_remocao = []
                try:
                    for tupla_ftl in dic_duplicated_flex_verbs:
                        for tupla_verbos_inf in dic_duplicated_flex_verbs[tupla_ftl]:
                            if verb in tupla_verbos_inf:
                                lista_remocao.append((tupla_ftl,tupla_verbos_inf))
                except Exception as e:
                    pass
                if lista_remocao:
                    lista_verbs_to_remove_flex_inf += [
                        [flex_verb, verb]
                        for tupla_ftl, tupla_verbos_inf in lista_remocao
                        for ftl in dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf]
                        for length in dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl]
                        for flex_verb in dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][length]
                        ]
                    for tupla_ftl,tupla_verbos_inf in lista_remocao:                                                                        
                        del(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf])
                    if not dic_duplicated_flex_verbs[tupla_ftl]:
                        del(dic_duplicated_flex_verbs[tupla_ftl])

        elif type == 'flex':
            for verb,verb_inf in verbs:
                verb = verb.lower()
                verb_inf = verb_inf.lower()
                ftl = verb[0:2]
                lenght = str(len(verb))
                for tupla_ftl in dic_duplicated_flex_verbs:
                    for tupla_verbos_inf in dic_duplicated_flex_verbs[tupla_ftl]:
                        try:
                            if verb in dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght]:
                                dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght] = list(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght]).remove(verb)
                                if dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght]:
                                    dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght] = tuple(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght])
                                else:
                                    del(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght])
                                    if not dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl]:
                                        del(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl])
                                lista_verbs_to_remove_flex_inf.append([verb,verb_inf])
                        except Exception as e:
                            pass
                        # else:
                        #     if not dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght]:
                        #         del(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl][lenght])
                        #     if not dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl]:
                        #         del(dic_duplicated_flex_verbs[tupla_ftl][tupla_verbos_inf][ftl])
        else:
            if not silence:
                print('\n'+'-'*100+'\n'+'! You need to give "flex" or "infinitive" as type input: type="infinitive", for example.'+'\n'+'-'*100+'\n')
    else:
        if not silence:
            print('\n'+'-'*100+'\n'+"! Something went wrong while openning our duplicated flex verbs dictionary, so we it can't be modified"+'\n'+'-'*100+'\n')
    if lista_verbs_to_remove_flex_inf and verbs_dic:
        for tupla_flexverb_verbinf in lista_verbs_to_remove_flex_inf:
            list_of_verb_type_keys = ['irregular','regular']

            first_3_letters = tupla_flexverb_verbinf[0][0:3]
            len_of_verb = str(len(tupla_flexverb_verbinf[0]))

            for verb_type in list_of_verb_type_keys:
                try:
                    verbs_dic[verb_type][first_3_letters][len_of_verb].remove(tupla_flexverb_verbinf)
                except Exception as e:
                    pass            


def lemmatize(verb : str,
              ignore_ambiguous_verbs : bool = True,
              silence : bool = True) -> str:
    """
    This function will give you the infinitive form of the verb (if it's inside our dataset).

    Params:
    -------
    - verb: String containing the verb you want to lemmatize.
    - ignore_ambigous_verbs: Bool that will give the decision to don't lemmatize flex verbs that are inside our flex verbs duplicated list (set as "False") or to lemmatize even if there is an ambiguity between which infinitive verb is really associated with the given flex verb (set as "True").
    - silece: Bool that will give the decision to print or don't print when a duplicated flex verb was gave as input.
    
    Returns:
    --------
    - return: String with the verb lemmatized (infinitive form), if it's inside our dataset. Otherwise it will return the originally verb gave as input.
    """
    if verbs_dic:
        verb = verb.lower()
        verb_duplicated = False
        if not ignore_ambiguous_verbs:
            if checkFlexVerbDuplicity(verb):
                verb_duplicated = True
        if not verb_duplicated:
                            
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
    """
    This function will say if the verb you give as input is (or isn't) inside our ambiguity dataset.
    This dataset was created for showing that some flex verbs have more than just one infinitive verb associated with it. So, as our tool is "rule-based", it doesn't know for sure what's the correct association.

    Params:
    -------
    - flex_verb: String containing the verb you want to analyze the ambiguity.
    
    Returns:
    --------
    - return: Bool that will say if the verb has ambiguity or don't have ambiguity, based on our dataset.
    """
    if dic_duplicated_flex_verbs:
        flex_verb = flex_verb.lower()
        ftl = flex_verb[0:2]

        # List comprehensive below:
        # lista_primeiras_tuplas = []
        # for chave in dic_duplicated_flex_verbs:
        #     if ftl in chave:
        #         for tupla in dic_duplicated_flex_verbs[chave]:
        #             if flex_verb in tupla:
        #                 lista_primeiras_tuplas.append(tupla)

        if [tupla for chave in dic_duplicated_flex_verbs if ftl in chave for tupla in dic_duplicated_flex_verbs[chave] if flex_verb in tupla]:
            return True
        
        lenght = str(len(flex_verb))

        # List comprehensive below:
        # lista_primeiras_tuplas = []
        # for chave in dic_duplicated_flex_verbs:
        #     for tupla in dic_duplicated_flex_verbs[chave]:    
        #         if ftl in dic_duplicated_flex_verbs[chave][tupla]:
        #             lista_primeiras_tuplas.append((chave,tupla))

        for tupla1,tupla2 in [(chave, tupla) for chave in dic_duplicated_flex_verbs for tupla in dic_duplicated_flex_verbs[chave] if ftl in dic_duplicated_flex_verbs[chave][tupla]]:
            try:
                if flex_verb in dic_duplicated_flex_verbs[tupla1][tupla2][ftl][lenght]:
                    return True
            except Exception as e:
                pass
    return False
