"""Written by: Nguyen Khang Huynh
Student ID: 33326460
Last Modified: 24/08/2023"""
import abc

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):
    def __init__(self, attack, defense, speed, max_hp) -> None:
        # TODO: Implement the code
        """Get the attack, defense, speed, max_hp value to the simple stats class
        Input: Attack, Defense, Speed, Max_HP
        Return: Don't return any value        
        """
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp 

    def get_attack(self):   
        """Return the attack of the simple stats 
        No input
        Return: Attack       
        """
        return self.attack
    def get_defense(self): 
        """Return the defense of the simple stats
        No input
        Return: defense       
        """
        return self.defense
    def get_speed(self): 
        """Return the speed of the simple stats
        No input
        Return: speed       
        """
        return self.speed 
    def get_max_hp(self): 
        """Return the max hp of the simple stats
        No input
        Return: defense       
        """
        return self.max_hp
    

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        # TODO: Implement
    
        #Complexity: O(1) for best and worst case 
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    def get_attack(self, level: int): 
        """Return the attack of the complex stats 
        No input
        Return: defense       
        """
        return self.calculate_formula(self.attack_formula,level)    
    def get_defense(self, level: int): 
        """Return the defense of the complex stats 
        No input
        Return: defense      
        """
        return self.calculate_formula(self.defense_formula,level)   
     
    def get_speed(self, level: int):  
        """Return the speed of the complex stats 
        No input
        Return: speed       
        """
        return self.calculate_formula(self.speed_formula,level)    
    def get_max_hp(self, level: int):    
       """Return the max_hp of the complex stats 
        No input
        Return: speed       
        """
       return self.calculate_formula(self.max_hp_formula,level)     
    
    def calculate_formula(self, formula:ArrayR[str], level_num: int) -> int:  
        """Calculate and return the calculated attack,speed,get_max_hp,speed in complex stats via those input in Polish notation
        No input
        Return: attack, speed, get_max_hp, speed 
        Complexity: O(n) for best and worst case      
        """
        stored_number = ArrayStack(len(formula))

        for element in formula: # Loop through the elememnt
            
            if element == "level":
                stored_number.push(level_num)  #push the level to the stack 
     
            elif element == "sqrt":
                result = self.square_roorts(stored_number.pop()) #calculate the square roots of the number then push to the stack 
                stored_number.push(result)

            elif element == "middle":
                result_array = self.middle(stored_number) #calculate the middle then push to the stack O(1)
                stored_number.push(result_array)
            
            elif element == "+": #calculate the total then push to the stack 
                num2 = stored_number.pop()
                num1 = stored_number.pop()
                result = num2 + num1
                stored_number.push(result) 

            elif element == "-": #calculate the difference then push to the stack 
                num2 = stored_number.pop()
                num1 = stored_number.pop()
                result =  num1 - num2
                stored_number.push(result) 

            elif element == "/": #calculate the division then push to the stack 
                num2 = stored_number.pop()
                num1 = stored_number.pop()
                result =  num1/num2
                stored_number.push(result)

            elif element == "*": #calculate the multiplication then push to the stack 
                num2 = stored_number.pop()
                num1 = stored_number.pop()
                result =  num1*num2
                stored_number.push(result) 

            elif element == "power": #calculate the power number then push to the stack 
                num2 = stored_number.pop()
                num1 = stored_number.pop()
                result =  num1**num2
                stored_number.push(result)
            else: #push and convert to int to the stack 
                stored_number.push(int(element))

        return stored_number.pop() #return the final number in the stack 
        

    def square_roorts(self,num:int) -> int: 
        """Calculate and return square roots
        Input: int num
        Return: the square root of the input
        Complexity: O(1) for best and worst case      
        """
        return num**0.5


    def middle(self,list: ArrayStack) -> int: #find the median of the 3 numbers 
        """Calculate and return the median number
        Input: array stack
        Return: the median number
        Complexity: O(1) for best and worst case      
        """
        num1 = list.pop()
        num2 = list.pop()
        num3 = list.pop()
        if (num1 < num2 and num1 > num3) or (num1 < num3 and num1 > num2):
            median = num1
        elif (num2 < num3 and num2 > num1) or (num2 < num1 and num2 > num3):
            median = num2
        else: 
            median = num3
        return median
