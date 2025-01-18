from src.imports import *

class BsOption:
    def __init__(self, S, K, T, rc, sigma, q=0):
        self.S = S
        self.K = K
        self.T = T
        self.rc = rc
        self.sigma = sigma
        self.q = q
        
    @staticmethod
    def N(x):
        return norm.cdf(x)
    
    @property
    def params(self):
        return {'S': self.S, 
                'K': self.K, 
                'T': self.T, 
                'rc':self.rc,
                'q':self.q,
                'sigma':self.sigma}
    
    def d1(self):
        return (np.log(self.S/self.K) + (-self.q + self.sigma**2/2)*self.T) \
                                / (self.sigma*np.sqrt(self.T))
    
    def d2(self):
        return self.d1() - self.sigma*np.sqrt(self.T)

    def delta_call(self):
        return norm.cdf(self.d1(), 0.0, 1.0)
    
    def _call_value(self):
        return self.S*np.exp(-self.q*self.T)*self.N(self.d1()) - \
                    self.K* self.N(self.d2()) + self.rc/2
                    
    def _put_value(self):
        return self.K * self.N(-self.d2()) -\
                self.S*np.exp(-self.q*self.T)*self.N(-self.d1()) - self.rc/2
    
    def price(self, type_ = 'C'):
        if type_ == 'C':
            return self._call_value()
        if type_ == 'P':
            return self._put_value() 
        if type_ == 'B':
            return  {'call': self._call_value(), 'put': self._put_value()}
        else:
            raise ValueError('Unrecognized type')