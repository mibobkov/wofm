import random
class Monster:
    def __init__(self, name, text, health, mindamage, maxdamage):
        self.maxhealth = health
        self.mindamage = mindamage
        self.maxdamage = maxdamage
        self.text = text
        self.name = name
        self.health = self.maxhealth

    def receive_damage(self, damage):
        self.health -= damage
        self.health = max(0, self.health)

    def get_damage(self):
        return random.randint(self.mindamage, self.maxdamage)
