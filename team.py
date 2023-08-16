from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.referential_array import ArrayR

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.team_mode = team_mode
        self.key = kwargs.get('sort_key') #key
        self.prov_mons = kwargs.get('provided_monsters') #listed of Monster
        self.init_team = ArrayR(self.TEAM_LIMIT)
        self.memory_key = -1

        if self.team_mode == self.TeamMode.FRONT: #Stack Ideas
            self.team = ArrayStack(self.TEAM_LIMIT)
        elif self.team_mode == self.TeamMode.BACK: # Circular Queue Ideas
            self.team = CircularQueue(self.TEAM_LIMIT)
        elif self.team_mode == self.TeamMode.OPTIMISE: #Sorted listed ideas
            self.team = ArraySortedList(self.TEAM_LIMIT)

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(self.prov_mons)
            self.init_team = self.prov_mons
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.") 



    def __len__(self):
        return len(self.team) #return the number of monster in the team
    
    def add_to_team(self, monster: MonsterBase):
        if self.team.is_full():
            return
        if self.team_mode == self.TeamMode.FRONT: #Stack Ideas
            self.team.push(monster)
        elif self.team_mode == self.TeamMode.BACK: # Circular Queue Ideas
            self.team.append(monster)
        elif self.team_mode == self.TeamMode.OPTIMISE: #Sorted Lists idea
            if self.key == self.SortMode.ATTACK:
                self.team.add(ListItem(monster,self.memory_key*monster.get_attack()))
            elif self.key == self.SortMode.DEFENSE:
                self.team.add(ListItem(monster,self.memory_key*monster.get_defense()))
            elif self.key == self.SortMode.HP:
                self.team.add(ListItem(monster,self.memory_key*monster.get_hp()))
            elif self.key == self.SortMode.LEVEL:
                self.team.add(ListItem(monster,self.memory_key*monster.get_level()))
            elif self.key == self.SortMode.SPEED:
                self.team.add(ListItem(monster,self.memory_key*monster.get_speed()))
            
            
            
            
        

    def retrieve_from_team(self) -> MonsterBase:
        if self.team.is_empty():
            return
        if self.team_mode == self.TeamMode.FRONT: #Stack Ideas
            return self.team.pop()
        elif self.team_mode == self.TeamMode.BACK: # Queue Ideas
            return self.team.serve()
        elif self.team_mode == self.TeamMode.OPTIMISE:
            return self.team.delete_at_index(0).value
            


    def special(self) -> None:
        newStack = ArrayStack(self.TEAM_LIMIT)
        newQueue = CircularQueue(self.TEAM_LIMIT)
        if self.team_mode == self.TeamMode.FRONT: #Stack Ideas
            if len(self.team) == 2:
                for _ in range(2):
                    newQueue.append(self.retrieve_from_team())
            elif len(self.team) >=3: 
                for _ in range(3):
                    newQueue.append(self.retrieve_from_team())
                
            for _ in range(len(newQueue)):
                self.add_to_team(newQueue.serve())
        
        elif self.team_mode == self.TeamMode.BACK: # Circular Queue Ideas
            mid = (len(self.team))/2
            for i in range(len(self.team)): 
                if i <= mid-1:
                    newQueue.append(self.retrieve_from_team())
                else:
                    newStack.push(self.retrieve_from_team())
            for _ in range(len(newStack)):
                self.add_to_team(newStack.pop())
            for _ in range(len(newQueue)): 
                self.add_to_team(newQueue.serve())


        elif self.team_mode == self.TeamMode.OPTIMISE:
            self.memory_key = -self.memory_key
            for _ in range(len(self.team)):
                mons = self.team.delete_at_index(0)
                mons.key = -(mons.key)
                self.team.add(mons)
            
    def regenerate_team(self) -> None:
        if self.team_mode == self.TeamMode.FRONT: #Stack Ideas
            self.team = ArrayStack(self.TEAM_LIMIT)
        elif self.team_mode == self.TeamMode.BACK: # Circular Queue Ideas
            self.team = CircularQueue(self.TEAM_LIMIT)
        elif self.team_mode == self.TeamMode.OPTIMISE: #Sorted listed ideas
            self.team = ArraySortedList(self.TEAM_LIMIT)
            self.memory_key = -1

        
        for i in range(len(self.init_team)):
            if self.init_team[i] != None:
                self.add_to_team(self.init_team[i]())

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        i = 0
        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.init_team[i] = monsters[x]
                        self.add_to_team(monsters[x]())
                        i += 1
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        #raise NotImplementedError
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        while True: 
            try:
                team_amount = int(input(" Team size. Single integer: "))
                if team_amount <= self.TEAM_LIMIT and team_amount >=1:
                    break
                else:
                    print("Invalid input")
            except ValueError:
                print("Wrong type")
    
        print(f"How many monsters are there? {team_amount} \n Monster are: \n")
        manually_list = get_all_monsters()
        i = 0
        for man_mons in range(len(manually_list)):
            if manually_list[man_mons].can_be_spawned() == "✔️":
                print(f"{man_mons+1}: {manually_list[man_mons].get_name()} [✔️]")
            elif manually_list[man_mons].can_be_spawned() == "❌":
                print(f"{man_mons+1}: {manually_list[man_mons].get_name()} [❌]")

        for _ in range(team_amount): 
            while True: 
                choose_mons = int(input("Which monster are you spawning? "))
                if choose_mons <= len(manually_list) and choose_mons >=1:
                    if manually_list[choose_mons-1].can_be_spawned():
                        self.init_team[i] =  manually_list[choose_mons-1]
                        i+=1
                        self.add_to_team(manually_list[choose_mons-1]())
                        break
                    else:
                        print("This monster cannot be spawned.")
                else:
                    print("Invalid input")
                
           
            

                
                
                
                
        

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        if provided_monsters is None:
            raise ValueError("No provided List")
        if len(provided_monsters) > self.TEAM_LIMIT:
            raise ValueError
        for prov_mons in provided_monsters:
            if prov_mons.can_be_spawned():
                self.add_to_team(prov_mons())
            else:
                raise ValueError


    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
