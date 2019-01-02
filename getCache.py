from Redit import Redit
from syncDatabase.setting.config import REDIS_KEY, REDIS_NAME

for item in REDIS_KEY:
    re = Redit(item)
    # print REDIS_NAME[0]
    print re.get_data(name = REDIS_NAME[0])
    # print  re.get_all()