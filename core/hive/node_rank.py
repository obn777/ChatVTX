class NodeRank:
    """
    Оценка вклада и надежности узла Hive.
    """

    def __init__(self):

        self.contributions = 0
        self.valid_packets = 0
        self.invalid_packets = 0
        self.base_accuracy = 0.5

    def register_contribution(self):
        """
        Узел отправил новый пакет знаний.
        """

        self.contributions += 1

    def register_validation(self, valid=True):
        """
        Проверка пакета другим узлом.
        """

        if valid:
            self.valid_packets += 1
        else:
            self.invalid_packets += 1

    def accuracy(self):
        """
        Текущая точность узла.
        """

        total = self.valid_packets + self.invalid_packets

        if total == 0:
            return self.base_accuracy

        return self.valid_packets / total

    def score(self):
        """
        Итоговый рейтинг узла.
        """

        return self.accuracy() * (1 + self.contributions * 0.01)

    def rank_level(self):
        """
        Категория узла.
        """

        score = self.score()

        if score < 0.5:
            return "novice"

        elif score < 1.0:
            return "researcher"

        else:
            return "expert"
