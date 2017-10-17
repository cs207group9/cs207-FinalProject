
#Written by Baptiste Lemaire
import xml.etree.ElementTree as ET

class xml2dict:
    
    """Read the XML file of the reactions and returns a list of dictionaries with 
       the features of every reaction, and an array of all the species involved.
       
    INPUTS
    ======
    file : XML file. 
           The format of the this input file must follow
           the format given by Prof. David Sondak.
    
    RETURNS
    =======
    Species: array of strings. 
    
    ListDictionaries: list of dictionaries.
                      Includes all the parameters of the reactions provided in XML files.
             
    EXAMPLES
    ========
    >>> xml2dict('rxns.xml')
    (['H', 'O', 'OH', 'H2', 'O2'], [{'coeffParams': {'A': 35200000000.0, 'b': -0.7, 'E': 71400.0}, 'coeffUnits': {'A': 'm3/mol/s', 'b': 'dimensionless', 'E': 'J/mol'}, 'id': 'reaction01', 'reversible': 'yes', 'type': 'Elementary', 'reactants': {'H': 1, 'O2': 1}, 'products': {'OH': 1, 'O': 1}, 'coeffLaw': 'Arrhenius'}, {'coeffParams': {'A': 0.0506, 'b': 2.7, 'E': 26300.0}, 'coeffUnits': {'A': 'm3/mol/s', 'b': 'dimensionless', 'E': 'J/mol'}, 'id': 'reaction02', 'reversible': 'yes', 'type': 'Elementary', 'reactants': {'H2': 1, 'O': 1}, 'products': {'OH': 1, 'H': 1}, 'coeffLaw': 'Arrhenius'}])    
    """
    
    def parse(self, file):
        self.file = file
        tree = ET.parse(file)
        root = tree.getroot()

        SpeciesArray=root.find('phase').find('speciesArray')
        self.Species = SpeciesArray.text.strip().split(" ")
    
        self.ListDictionaries = []
    
        #Now: go through every reaction to read the features:
    
        for reaction in root.find('reactionData').findall('reaction'):
        
            #Initialization of the variables
        
            Dict = {}
            reactants = []
            products = []
            Nup = []
            Nupp = []
            ListCoeffUnits = []
        
            ListReactants = reaction.find('reactants').text.split()
            for elementsR in ListReactants:
                specie, nu = elementsR.split(':')
                reactants.append(specie)
                Nup.append(int(nu))
            ListProducts = reaction.find('products').text.split()
            for elementsP in ListProducts:
                specie, nu = elementsP.split(':')
                products.append(specie)
                Nupp.append(int(nu))
            for name in reaction.find('rateCoeff'):
                Law = name.tag
                ListCoeffTag = []
                ListCoeffValue = []
                for coeff in name:
                    ListCoeffTag.append(coeff.tag)
                    ListCoeffValue.append(float(coeff.text))
                    if len(coeff.attrib) != 0:
                        ListCoeffUnits.append(coeff.attrib['units'])
                    else:
                        ListCoeffUnits.append('dimensionless')
            Dict['coeffParams'] = dict(zip(ListCoeffTag, ListCoeffValue))
            Dict['coeffUnits'] = dict(zip(ListCoeffTag,ListCoeffUnits))
            Dict['id'] = reaction.attrib['id']
            Dict['reversible'] = reaction.attrib['reversible']
            Dict['type'] = reaction.attrib['type']
            Dict['reactants'] = dict(zip(reactants, Nup))
            Dict['products'] = dict(zip(products, Nupp))
            Dict['coeffLaw'] = Law
            self.ListDictionaries.append(Dict)
    
    def getParams(self):
        return self.Species, self.ListDictionaries
