
#Written by Baptiste Lemaire
import xml.etree.ElementTree as ET

class xml2dict:
    """
    xml2dict turns an XML file into a array of all the species involved into the system of
    reactions and a list of dictionaries. This latter contains a dictionary for every single 
    reaction of the system of reactions. Each dictionary contains the information about the 
    reactants, the products, the stoichiometric coefficients and the kinetic law for the 
    reaction constant (Arrhenius Law, Modified Arrhenius Law, Constant Law, and so forth).
    where list of dictionary Reaction contains all the infomation from one given reaction.
    
    INPUTS
    ======
    
    file: XML file.
          The format of the this input file must follow
          the format given by Prof. David Sondak.
          
    METHODS
    =======
    
    parse(self, file): 
        extract all the information contained into the XML file provided by
        the user, namely the names of all the species involved in the system
        of reactions, stored into the array self.Species, and all the information
        about every reaction, stored into self.ListDictionaries
        
    get_info(self):
        return the array self.Species containing the names of the species involved
        and the list of dictionaries self.ListDictionaries
        OUTPUTS: self.Species, self.ListDictionaries
           
    __repr__(self):
        return a string of all the sppecies and all the information contained in 
        self.dictionaries
        OUTPUTS: str
    
    
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
                #    if len(coeff.attrib) != 0:
                #        ListCoeffUnits.append(coeff.attrib['units'])
                #    else:
                #        ListCoeffUnits.append('dimensionless')
            Dict['coeffParams'] = dict(zip(ListCoeffTag, ListCoeffValue))
            #Dict['coeffUnits'] = dict(zip(ListCoeffTag,ListCoeffUnits))
            Dict['ID'] = reaction.attrib['id']
            Dict['reversible'] = reaction.attrib['reversible']
            Dict['TYPE'] = reaction.attrib['type']
            Dict['reactants'] = dict(zip(reactants, Nup))
            Dict['products'] = dict(zip(products, Nupp))
            Dict['coeffLaw'] = Law
            self.ListDictionaries.append(Dict)
    
    def get_info(self):
        return self.Species, self.ListDictionaries
    
    def __repr__(self):
        return str(self.Species) + ' ' + str(self.ListDictionaries)
