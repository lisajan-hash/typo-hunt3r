class SimpleFuzzer:
    def __init__(self, domain):
        self.domain = domain

    def _addition(self):
        """Generate variations by adding a character at different positions."""
        result = set()
        for i in range(len(self.domain) + 1):
            for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
                result.add(self.domain[:i] + char + self.domain[i:])
        return result

    def _omission(self):
        """Generate variations by omitting characters."""
        return {self.domain[:i] + self.domain[i+1:] for i in range(len(self.domain))}

    def _transposition(self):
        """Generate variations by swapping adjacent characters."""
        return {self.domain[:i] + self.domain[i+1] + self.domain[i] + self.domain[i+2:]
                for i in range(len(self.domain) - 1)}

    def generate_permutations(self):
        """Combine all permutation techniques."""
        permutations = set()
        permutations.update(self._addition())
        permutations.update(self._omission())
        permutations.update(self._transposition())
        permutations.add(self.domain)
        return permutations