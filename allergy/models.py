from django.db import models
from users.models import User

# Create your models here.
class Allergy(models.Model):
    egg = models.BooleanField(default=False)        # 1. 난류
    milk = models.BooleanField(default=False)       # 2. 우유
    buckwheat = models.BooleanField(default=False)  # 3. 메밀
    peanut = models.BooleanField(default=False)     # 4. 땅콩
    bean = models.BooleanField(default=False)       # 5. 대두
    wheat = models.BooleanField(default=False)      # 6. 밀
    mackerel = models.BooleanField(default=False)   # 7. 고등어
    crab = models.BooleanField(default=False)       # 8. 게
    shrimp = models.BooleanField(default=False)     # 9. 새우
    pork = models.BooleanField(default=False)       # 10. 돼지고기
    peach = models.BooleanField(default=False)      # 11. 복숭아
    tomato = models.BooleanField(default=False)     # 12. 토마토
    sulfite = models.BooleanField(default=False)    # 13. 아황산염
    walnut = models.BooleanField(default=False)     # 14. 호두
    chicken = models.BooleanField(default=False)    # 15. 닭고기
    beef = models.BooleanField(default=False)       # 16. 쇠고기
    squid = models.BooleanField(default=False)      # 17. 오징어
    shellfish = models.BooleanField(default=False)  # 18. 조개류
    pineNut = models.BooleanField(default=False)    # 19. 잣

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="allergy")