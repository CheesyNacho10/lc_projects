from main import transform_tags

string_ejemplo = [(u'*0*', u'sn.e-SUJ'), (u'Era', u'vsii3s0'), (u'el', u'da0ms0'), 
                    (u'sustituto', u'ncms000'), (u'natural', u'aq0cs0'), 
                    (u'de', u'sps00'), (u'Redondo', u'np0000p'), (u',', u'Fc'), 
                    (u'pero', u'cc'), (u'las', u'da0fp0'), (u'discrepancias', u'ncfp000'), 
                    (u'acabaron', u'vmis3p0'), (u'con', u'sps00'), 
                    (u'su', u'dp3cs0'), (u'uni\xf3n', u'ncfs000'), (u'-', u'Fg'), 
                    (u'.', u'Fp')]
string_esperada_ejemplo_transofrmado = [(u'Era', u'vsi'), (u'el', u'da'), (u'sustituto', u'nc'), 
                                        (u'natural', u'aq'), (u'de', u'sp'), (u'Redondo', u'np'), (u',', u'Fc'), 
                                        (u'pero', u'cc'), (u'las', u'da'), (u'discrepancias', u'nc'), 
                                        (u'acabaron', u'vmi'), (u'con', u'sp'), (u'su', u'dp'), 
                                        (u'uni\xf3n', u'nc'), (u'-', u'Fg'), (u'.', u'Fp')]

string_ejemplo_transformado = transform_tags(string_ejemplo)
print('Oración de ejemplo:', string_esperada_ejemplo_transofrmado)
print('Oración de ejemplo transformada:', string_ejemplo_transformado)

assert(string_ejemplo_transformado == string_esperada_ejemplo_transofrmado)
