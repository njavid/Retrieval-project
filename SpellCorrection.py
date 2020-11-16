class SpellCorrection:

    def __init__(self, main_index, bi_index):
        self.main_index = main_index
        self.bi_index = bi_index

    @staticmethod
    def edit_distance(a, b):
        dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i in range(len(a) + 1):
            dp[i][0] = i
        for j in range(len(b) + 1):
            dp[0][j] = j

        for i in range(len(a) + 1):
            dp[i][0] = i
            for j in range(len(b) + 1):
                dp[i][j] = i + j
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 1][j - 1])
                dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + 1)
                dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)
                dp[i][j] = min(dp[i][j], dp[i][j - 1] + 1)
        return dp[len(a)][len(b)]

    def check_spell(self, word):
        return word in self.main_index.index

    def get_jaccard_volunteers(self, word):
        bi_words = [word[i:i + 2] for i in range(len(word) - 1)]
        volunteers1 = set([])
        volunteers2 = set([])

        for i in range(len(bi_words)):
            volunteers1 = volunteers1.union(set(self.bi_index.get_posting_list(bi_words[i]).keys()))
            for j in range(i + 1, len(bi_words)):
                l1 = self.bi_index.get_posting_list(bi_words[i]).keys()
                l2 = self.bi_index.get_posting_list(bi_words[j]).keys()
                volunteers2 = volunteers2.union(set(l1).intersection(set(l2)))
        volunteers1 = sorted(volunteers1, key=lambda v: (1 / (len(v) - 1 + len(word) - 1 - 1)))[:10]
        volunteers2 = sorted(volunteers2, key=lambda v: (2 / (len(v) - 1 + len(word) - 1 - 2)))[:10]
        return volunteers1 + volunteers2

    def correct_spelling(self, word):
        if self.check_spell(word):
            return word
        volunteers = self.get_jaccard_volunteers(word)
        return min(volunteers, key=lambda v: self.edit_distance(v, word))
