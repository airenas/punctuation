class PunctS:
    colon = ":COLON"
    semicolon = ";SEMICOLON"
    period = ".PERIOD"
    comma = ".COMMA"
    question = "?QUESTIONMARK"
    exclamation = "!EXCLAMATIONMARK"


punct_dic = {',': PunctS.comma,
             '.': PunctS.period,
             '?': PunctS.question,
             '!': PunctS.exclamation,
             ':': PunctS.colon,
             ';': PunctS.semicolon,
             '-': "-DASH"}
