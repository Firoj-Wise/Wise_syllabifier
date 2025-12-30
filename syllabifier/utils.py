class StringUtils:
    @staticmethod
    def ordinal_index_of(source, sub_str, n):
        pos = -1
        # We need to find the (n+1)-th occurrence
        for _ in range(n + 1):
            pos = source.find(sub_str, pos + 1)
            if pos == -1:
                return -1
        return pos