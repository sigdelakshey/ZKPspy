class PedersenCommitment:
    def __init__(self, p, g, h):
        self.p = p
        self.g = g
        self.h = h

    def generate_commitment(self, m, r):
        commitment = (pow(self.g, m, self.p) * pow(self.h, r, self.p)) % self.p
        return commitment
    
    def generate_simcommitment(self, m, r, commit, c):
        commitment = (pow(self.g, m, self.p) * pow(self.h, r, self.p)  * pow(commit, -c, self.p)) % self.p
        return commitment

    def verify_commitment(self, C, m, r):
        return C == self.generate_commitment(m, r)
