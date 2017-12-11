
from chemkin_CS207_G9.parser.xml2dict import xml2dict
from chemkin_CS207_G9.parser.database_query import CoeffQuery
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem

def Reaction_Creator(path_xml, path_sql, start = None, end = None):
    reader = xml2dict()
    reader.parse(path_xml)
    info = reader.get_info()
    species = info[0]
    reactions = [Reaction(**r) for r in info[1]]
    cq = CoeffQuery(path_sql)

    if end is None or start is None:
        rs = ReactionSystem(reactions, species, nasa_query = cq)
        
    else:
        rs = ReactionSystem(reactions[start:end], nasa_query = cq)
    
    return rs                              