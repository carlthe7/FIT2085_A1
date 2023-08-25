from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle
from elements import Element
from typing import Generic, TypeVar

from data_structures.queue_adt import CircularQueue
from data_structures.referential_array import ArrayR
from data_structures.bset import BSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.array_sorted_list import ListItem

class Iterator(Generic[TypeVar("T")]):
    def __init__(self, battle_tower: BattleTower) -> None:
        """Assign battle_tower to a variable
        Input: Battle tower
        No return 
        Complexity O(1) for best and worst case       
        """
        self.battle_tower = battle_tower
        self.battle_tower.next_team()

    def __iter__(self):
        """Return the instance of the class 
        Complexity O(1) for best and worst case       
        """
        return self
    
    def __next__(self):
        """Return the next battle tower 
        Complexity O(1) for best and O(n) worst case where n is the number of monster in the tower team  
        """
        if self.battle_tower.battles_remaining():
            tower_ans = self.battle_tower.next_battle()
            return tower_ans
        else:
            raise StopIteration


class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        """Initialize a BattleTower instance
        :param: battle: Battle: a Battle instance to execute the
        mine: Our team
        mine_lives: our team lives
        enemy: Enemy team
        enemy_lives: Enemy team lives
        current_enemy: Current enemy team
        current_enemy_live: Current enemy team live
        Complexity O(1) for best and worst case
        """
        self.battle = battle or Battle(verbosity=0)
        self.mine = None
        self.mine_lives = None
        self.enemy = None
        self.enemy_lives = None
        self.current_enemy = None
        self.current_enemy_lives = None

        self.internal_meta = BSet(len(Element.__members__))
        self.external_meta = BSet(len(Element.__members__))


    def set_my_team(self, team: MonsterTeam) -> None:
        """Set our team 
        Complexity O(1) for best and worst case"""
        # Generate the team lives here too.
        self.mine = team
        self.mine_lives = RandomGen.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES)
        self.internal_meta = self.internal_meta.union(self.mine.get_the_element())

    def generate_teams(self, n: int) -> None:
        """Generate both team
        Complexity O(n) for best and worst case where n is the team size/input of the function"""
        self.enemy_lives = CircularQueue(n)
        self.enemy = CircularQueue(n)
        for _ in range(n):
            self.enemy.append(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
            self.enemy_lives.append(RandomGen.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES))

        self.next_team()
        
    def battles_remaining(self) -> bool:
        """Return False if either the our team or enemmy team run out of lives and True if the battle continue
        Complexity O(1) for best and worst case"""
        if self.mine_lives == 0:
            return False
        
        if len(self.enemy) == 0 and self.current_enemy == None:
            return False
        else:
            return True
        
    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """Return Tuple of the Battle Result, Monster Team, my team lives and current enemy lives
        Complexity O(1) for best and worst case"""
        self.mine.regenerate_team()
        self.current_enemy.regenerate_team()
        

        result = self.battle.battle(self.mine, self.current_enemy)
        
        if result == Battle.Result.TEAM1:
            self.current_enemy_lives -= 1

        elif result == Battle.Result.TEAM2:
            self.mine_lives -= 1
            
        elif result == Battle.Result.DRAW:
            self.current_enemy_lives -= 1
            self.mine_lives -= 1
        
        if self.current_enemy_lives > 0:
            self.enemy.append(self.current_enemy)
            self.enemy_lives.append(self.current_enemy_lives)

        tower_ans = (result, self.mine, self.current_enemy, self.mine_lives, self.current_enemy_lives)
        self.updates()
        return tower_ans
    
    def updates(self):
        """ Update the internal and external meta
        Complexity O(1) for best and worst case"""
        # Update the internal meta
        team_element = self.mine.get_the_element()
        enemy_element = self.current_enemy.get_the_element()
        self.internal_meta = self.internal_meta.union(enemy_element).union(team_element)
        self.internal_meta = self.internal_meta.difference(self.external_meta)
        self.next_team()
        if self.current_enemy is not None:
            #update the external meta
            self.external_meta = self.external_meta.union(self.internal_meta)
            self.external_meta = self.external_meta.difference(self.current_enemy.get_the_element())
            self.external_meta = self.external_meta.difference(self.mine.get_the_element())
    

    def next_team(self):
        """Serve the monster out of the enemy team
        Complexity O(1) for best and worst case"""
        try:
            self.current_enemy = self.enemy.serve()
            self.current_enemy_lives = self.enemy_lives.serve()
        except:
            self.current_enemy = None
            self.current_enemy_lives = None

    
    def out_of_meta(self) -> ArrayR[Element]:
        """Return the array of elements
        Complexity O(1) for best and O(n) worst case where n is the length of Elements"""
        sorted_list = ArraySortedList(len(self.external_meta))
        for element in Element:
            if element.value in self.external_meta:
                element = ListItem(element, element.value)
                sorted_list.add(element)

        tower_ans = ArrayR(len(self.external_meta))
        for i in range(len(sorted_list)):
            tower_ans[i] = sorted_list[i].value
        return tower_ans

    
    def __iter__(self):
        """Return the instance of the class
        Complexity O(1) for best and worst case"""
        return self
    

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)
