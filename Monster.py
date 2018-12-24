import random
class Monster:
    def __init__(self, name, text, health, mindamage, maxdamage, gold, exp):
        self.gold = gold
        self.exp = exp
        self.maxhealth = health
        self.mindamage = mindamage
        self.maxdamage = maxdamage
        self.text = text
        self.name = name
        self.health = self.maxhealth

    def get_gold(self):
        return random.randint(self.gold*0.5, self.gold*1.5)

    def get_exp(self):
        return random.randint(self.exp*0.5, self.exp*1.5)

    def receive_damage(self, damage):
        self.health -= damage
        self.health = max(0, self.health)

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)
