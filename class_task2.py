#============= 1 დავალება ========================

class Character :
    def __init__(self,name , health, power):
        self.name = name
        self.health = health
        self.power = power


    def attack(self, other):

        if (isinstance(self,Warrior) and isinstance (other , Mage)) or \
           (isinstance (self, Mage) and isinstance (other , Archer)) or \
           (isinstance (self, Archer) and isinstance (other , Warrior)):
            print(f"{self.name} -მა გაიმარჯვა! {other.name} დამარცხდა.")
        else : print (f"{other.name } - მა გაიმარჯვა! {self.name} დამარცხდა.")

class Warrior (Character):
    def __init__(self,name , health, power):
        super().__init__(name,health,power)


class Mage (Character):
    def __init__(self,name , health, power):
        super().__init__(name,health,power)


class Archer (Character):
    def __init__(self,name , health, power):
        super().__init__(name,health,power)

warrior=Warrior("მეომარი",100,20)
mage= Mage ("მაგი", 80,25)
archer=Archer ("მშვილდოსანი", 90 ,15)

warrior.attack(mage)
mage.attack(archer)
archer.attack(warrior)


#==================== 2 დავალება ========================

class Monster:
    def __init__(self,name , power, task):
        self.name = name
        self.power = power
        self.task = task

    @classmethod
    def create_from_level(cls, level):

        monsters_data = {
           1: ("მზესუმზირა" ,10 , "ყვავილების მოვლა"),
           2: ("თბილუნა" , 20 , "ადამიანების ჩახუტება"),
           3: ("ცოდნის-მცველი" , 35 , "ბავშვებს ეხმარება სწავლაში"),
           4: ("ნათება" , 45 , "ღამით გზის განათება"),
           5: ("წვიმის მეგობარი" , 55 , "მცენარეების მორწყვა" ),
           6: ("მშვიდობის მცველი" , 65 , "ჩხუბის შეჩერება"),
           7: ("ექიმი-მონსტრი" ,75 , "ჭრილობის განკურნება"),
           8: ("მშენებელი-გიგანტი" , 80 , "სახლების აშენება"),
           9: ("ეკო-მონსტრი" , 90 , "ბუნების დასუფთავება"),
           10: ("სუპერ- მონსტრი" , 100 , "ყველა კეთილი საქმის კეთება")
        }

        if level in monsters_data:
            name,power, task= monsters_data[level]
            return cls (name, power, task)
        else:
            return cls ("უცნობი მონსტრი" , 0 , "დავალება არ ააქვს")

    def info(self):
         print (f"მონსტრი: {self.name} | ძალა: {self.power} | მოვალება: {self.task}")

factory = []
for i in range(1,11):

    new_monster = Monster.create_from_level(i)
    factory.append(new_monster)

for monster in factory:
    monster.info()


#================== 3 დავალება ==================

import random

class Slotmachine:
    symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]


    def __init__(self , difficulty_symbols ):
        self.available_symbols = difficulty_symbols


    @staticmethod
    def generate_spin (symbols_pool):
        return[random.choice(symbols_pool) for _ in range (3) ]

    @classmethod
    def from_difficulty (cls, level):
        if level.lower() == "easy":
            return cls(cls.symbols [:3] )
        elif level.lower() == "hard":
            return cls(cls.symbols  )
        else:
            return cls(cls.symbols [:4])



    def play(self):
        result = self.generate_spin (self.available_symbols)
        print (f"შედეგი: { ' | '.join(result) }")

        if result [0] == result[1] == result[2] :
            print ("გილოცავ ! შენ მოიგე !")
        else:
            print("სცადე თავიდან")

print("---მარტივი დონე--- (Easy Mode)")
hard_game = Slotmachine.from_difficulty("hard")
for i in range (3) :
    print(f"ცდა {i+1}:")
    hard_game.play()

#=============== 4 დავალება ===============
import random


class Hero:
    def __init__(self, name, health=100, score=0):
        self.name = name
        # private ატრიბუტები
        self.__health = health
        self.__score = score

    @property

    def health(self):
        return self.__health

    @property
    def score(self):
        return self.__score

    @staticmethod
    def random_event():

        events = [
            ("score", 20, "იპოვეთ საგანძური! +20 ქულა"),
            ("health", -15, "მტერმა დაგჭრათ! -15 სიცოცხლე"),
            ("score", 10, "დავალება შესრულებულია! +10 ქულა"),
            ("health", -25, "ხაფანგში გაებით! -25 სიცოცხლე")
        ]
        return random.choice(events)

    @classmethod
    def from_name(cls, name):
        """ქმნის ჩვეულებრივ გმირს მხოლოდ სახელით"""
        return cls(name)

    def update_stats(self, stat_type, value):
        if stat_type == "health":
            self.__health += value
        elif stat_type == "score":
            self.__score += value


class SuperHero(Hero):
    def __init__(self, name, extra_power, health=150):
        super().__init__(name, health=health)
        self.extra_power = extra_power

    @classmethod
    def from_name(cls, name):
        return cls(name, "უცნობი ძალა")

    def use_power(self):
        print(f"🦸 {self.name} იყენებს ძალას: {self.extra_power}!")


# თამაში დაიწყო=================================

hero = SuperHero.from_name("Python_Warrior")
hero.extra_power = "ფრენა"

print(f"🎮 თამაში იწყება!")
print(f"გმირი: {hero.name}")
print(f"ძალა: {hero.extra_power}")

round_count = 1

while hero.health > 0:
    print(f"\n--- რაუნდი {round_count} ---")

    stat, value, description = Hero.random_event()
    print(description)

    hero.update_stats(stat, value)

    print(f"❤️ სიცოცხლე: {hero.health}")
    print(f"⭐ ქულა: {hero.score}")

    if hero.health <= 0:
        print(f"\n💀 გმირი {hero.name} დამარცხდა!")
        print(f"🏆 საბოლოო ქულა: {hero.score}")
        break

    round_count += 1

#==============5================


