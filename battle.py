from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam
from monster_base import MonsterBase


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity

    
    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        Complexity O(n) for best and worst case where n is the length of both team
        """
    
        # Get the action from each team
        team2_act = self.team2.choose_action(self.out2, self.out1)
        team1_act = self.team1.choose_action(self.out1, self.out2)

        #Check each action of each team
        #If not attack, work on before the attack
        if team1_act != Battle.Action.ATTACK:
            self.out1 = self.attack_before(self.team1, team1_act, self.out1)
        if team2_act != Battle.Action.ATTACK:
            self.out2 = self.attack_before(self.team2, team2_act,self.out2)
        
        #If attack, work on the function after attack
        if team1_act == Battle.Action.ATTACK or team2_act == Battle.Action.ATTACK:
            self.battle_attack(team1_act, team2_act)
        
        #Decrease each mons health if they alive
        if self.out1.alive() and self.out2.alive():
            self.out1.set_hp(self.out1.get_hp()- 1)
            self.out2.set_hp(self.out2.get_hp()- 1)
        #increase turn by 1
        self.turn_number +=1    

        #return None if both monster a live
        if self.out1.alive() and self.out2.alive():
            return None
        
        # if team 2 alive and team 1 die, mons in team 2 level up and evolve
        elif self.out2.alive() and not self.out1.alive() :
            self.out2.level_up()
            if self.out2.ready_to_evolve():
                self.out2 = self.out2.evolve()
            # if team lose in the battle has no monster left --> return result
            
            if len(self.team1) == 0:
                return Battle.Result.TEAM2
            
            else: # else replace the dead mons
                self.out1 = self.team1.retrieve_from_team()
                return None
        
        # if team 1 alive and team 2 not, mons in team 1 level up and evolve
        elif self.out1.alive() and not self.out2.alive():
            self.out1.level_up()
            if self.out1.ready_to_evolve():
                self.out1 = self.out1.evolve()

           # if team 2 lose in the battle has no monster left --> return result
            if len(self.team2) == 0:
                return Battle.Result.TEAM1 
            else: # else retrieve the dead mons
                self.out2 = self.team2.retrieve_from_team()
                return None
        
        #If both monster die check and each team monster remain and give back result
        elif not self.out1.alive() and not self.out2.alive():
            if len(self.team1) == 0 and len(self.team2) == 0:
                return Battle.Result.DRAW
            
            # if team 1 lose in the battle has no monster left --> return result
            elif len(self.team2) == 0:
                return Battle.Result.TEAM1
            
            elif len(self.team1) == 0:
                return Battle.Result.TEAM2
            
            else:
                self.out1 = self.team1.retrieve_from_team()
                self.out2 = self.team2.retrieve_from_team()
                return None
            


    def attack_before(self, team: MonsterTeam, act: Battle.Action, mons: MonsterBase): # before the battle
        """Return the monster to join in the battle
        Complexity O(n) for best and worst case where n is the of the team """
        if act == Battle.Action.SPECIAL:
            team.add_to_team(mons)
            team.special()
            return team.retrieve_from_team()

        elif act == Battle.Action.SWAP:
            team.add_to_team(mons)
            return team.retrieve_from_team()
        else:
            return mons

    def battle_attack(self, act1: Battle.Action, act2:Battle.Action): #during the battle
        """Let two monster attack each other, compare special condition
        Complexity O(1) for best and worst case"""
        if act1 == Battle.Action.ATTACK and act2 == Battle.Action.ATTACK:
            speed_1 = self.out1.get_speed()
            speed_2 = self.out2.get_speed()
            if speed_1 == speed_2: #Equal speed
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)

            elif speed_1 > speed_2: #Mons 1 faster than Mons 2
                self.out1.attack(self.out2)
                if self.out2.alive():
                    self.out2.attack(self.out1)

            elif speed_2 > speed_1:#Mons 2 faster than Mons 1
                self.out2.attack(self.out1)
                if self.out1.alive():
                    self.out1.attack(self.out2)
    
        elif act2 == Battle.Action.ATTACK:
            self.out2.attack(self.out1)
        elif act1 == Battle.Action.ATTACK:
            self.out1.attack(self.out2)

    
    
    
    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
