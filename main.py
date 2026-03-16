from logic.cooldown import Cooldown
from gestures.export import Gestures

gest_class = Gestures()
gestures = gest_class.get_all()

cooldown = Cooldown()
print(cooldown.static)
print(gestures)