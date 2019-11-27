from ntru.Poly import PolyRingModP


PARAMETER_SETS = {
    "ees401ep2": {
        "N": 401,
        "p": 3,
        "q": 2048,
        "e": 11,
        "df1": 8,
        "df2": 8,
        "df3": 6,
        "dg": 133,
        "dr1": 8,
        "dr2": 8,
        "dr3": 6
    },
    "ees439ep1": {
        "N": 439,
        "p": 3,
        "q": 2048,
        "e": 11,
        "df1": 9,
        "df2": 8,
        "df3": 5,
        "dg": 146,
        "dr1": 9,
        "dr2": 8,
        "dr3": 5
    },
    "ees743ep1": {
        "N": 743,
        "p": 3,
        "q": 2048,
        "e": 11,
        "df1": 11,
        "df2": 11,
        "df3": 15,
        "dg": 247,
        "dr1": 11,
        "dr2": 11,
        "dr3": 15
    }
}

class PubKey:

    def __init__(self, parameter):
        self.__dict__.update(**parameter)
        self._generate_key()

    def _generate_key(self):
        self._generate_f()
        self._generate_inverse()
        self._generate_g()
        self._generate_h()
        self._generate_r_R()


    def _generate_f(self):
        self.f1 = PolyRingModP(self.N, self.q)
        self.f2 = PolyRingModP(self.N, self.q)
        self.f3 = PolyRingModP(self.N, self.q)
        self.f1.random_poly(self.df1)
        self.f2.random_poly(self.df2)
        self.f3.random_poly(self.df3)
        self.F = PolyRingModP.product_mul(self.f1, self.f2, self.f3)
        self.f = 1 + self.p * self.F

    def _generate_inverse(self):
        f_coefs = PolyRingModP.remove_right_zeros(self.f.coefs)
        inv_coefs = PolyRingModP.inverse_mod_p_e(self.N, 2, f_coefs, self.e)
        self.inv_f = PolyRingModP(self.N, self.q, inv_coefs)
        assert self.inv_f is not None

    def _generate_g(self):
        self.g = PolyRingModP(self.N, self.q)
        self.g.random_poly_shuffle(self.dg)

    def _generate_h(self):
        self.h = self.p * self.inv_f * self.g % self.q

    def _generate_r_R(self):
        self.r1 = PolyRingModP(self.N, self.q)
        self.r2 = PolyRingModP(self.N, self.q)
        self.r3 = PolyRingModP(self.N, self.q)
        self.r1.random_poly(self.df1)
        self.r2.random_poly(self.df2)
        self.r3.random_poly(self.df3)
        self.r = PolyRingModP.product_mul(self.r1, self.r2, self.r3)
        self.R = self.h * self.r % self.q

if __name__ == '__main__':
    key = PubKey(PARAMETER_SETS.get("ees401ep2"))
    print(1)