
from xml2dict import xml2dict

def test_class1():
    r = xml2dict()
    r.parse('rxns.xml')
    assert(r1.get_info()[1][1]['TYPE'] == 'Elementary')
    
def test_class2():
    r = xml2dict()
    r.parse('rxns.xml')
    assert(r1.get_info()[0][1] == 'O')    
    
def test_class3():
    r = xml2dict()
    r.parse('rxns.xml')
    assert(r1.get_info()[1][1]['products'] == {'H': 1, 'OH': 1})
    
def test_class4():
    r = xml2dict()
    r.parse('rxns2.xml')
    assert(r1.get_info()[1][2]['coeffParams'] == {'A': 10000000.0, 'E': 10000.0}) 
    
def test_class5():
    r = xml2dict()
    r.parse('rxns2.xml')
    assert(r1.get_info()[1][1]['coeffUnits'] == {'k': 'm3/mol/s'})     
    
def test_class6():
    r = xml2dict()
    r.parse('rxns2.xml')
    assert(r1.get_info()[1][1]['reactants'] == {'HO2': 1, 'OH': 1}) 
    
def test_class7():
    r = xml2dict()
    r.parse('rxns2.xml')
    assert(r1.get_info()[1][2]['ID'] == 'reaction03') 
    
def test_class8():
    r = xml2dict()
    r.parse('rxns2.xml')
    assert(r1.get_info()[1][2]['reversible'] == 'yes') 