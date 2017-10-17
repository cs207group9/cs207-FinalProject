# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 12:02:05 2017

@author: Camilo
"""
from  more_itertools import unique_everseen

class ReactionSystem:
    
    def __init__(self, reactions, initial_concentrations =  None):
        # TODO: check for bad inputs
        self.reactions = reactions
        self.species = self.get_species()
        if initial_concentrations == None:
            self.initial_concentrations = [1 for i in self.species]
        else:
            self.initial_concentrations = initial_concentrations
            
            
        
    def remove_duplicates(seq):
        '''
        Very fast function for removing duplicates in a sequence
        '''
        
        seen = set()            # Creating a set, works without duplicates
        seen_add = seen.add     # Putting the function in a variable because it is faster to resolve the variable
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    def get_species(self):
        '''
        Returns array of species contained in reactions, without duplicates.
        '''
        
        species = []
        
        for reac in self.reactions:
            species.append(reac.get_species())
            
#        self.remove_duplicates(species)
        
        return list(unique_everseen(species))
    
