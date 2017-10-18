from chemkin import *

reader = Xml2dict()
reader.parse('rxns.xml')
info =reader.get_info()

reaction1 = Reaction(info[1][0])
reaction2 = Reaction(info[1][1])
species_ls=info[0]

rs = ReactionSystem([reaction1, reaction2],species_ls)
rs.set_concs(dict(zip(species_ls,[1200,1212,322,4123,221])))
rs.set_temp(1500)
rs.get_reac_rate()