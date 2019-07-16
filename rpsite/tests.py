from django.test import TestCase, override_settings, Client
from django.conf import settings
from .utils import verify, test_privkey, test_pubkey, hashing
from Crypto.Util import number
import random
import gmpy2
from hashlib import sha256

# Create your tests here.
class VeryfyTest(TestCase):
    fixtures = ['data.json']

    def gen_credentials(self, pubkey, uk, course_no):
        q = pubkey['n'] // test_privkey
        s = random.randrange(1<<8196)
        e = number.getPrime(2050)
        d = int(gmpy2.invert(e, (test_privkey-1)*(q-1)))
        tmp = gmpy2.powmod(pubkey['a'], uk, pubkey['n']) * \
            gmpy2.powmod(pubkey['b'], s, pubkey['n']) * \
            pubkey['c'] % pubkey['n']
        v = gmpy2.powmod(tmp, d, pubkey['n'])
        left = gmpy2.powmod(v, e, pubkey['n'])
        right = tmp
        self.assertEqual(left, right)
        # the signiture is (e, v, s)
        grnym = int(sha256(str(course_no).encode()).hexdigest(), 16) % 731499577
        grnym = gmpy2.powmod(grnym, settings.RNYM_PARAM['exp'], settings.RNYM_PARAM['gamma'])
        params = {}
        priv = {}
        # generate randoms
        for i in ['s', 'e', 'w', 'z', 'x']:
            priv['r'+i] = random.randrange(1<<32)
        for i in range(1, 20):
            priv['r{}'.format(i)] = random.randrange(1<<32)
        priv['w'] = random.randrange(1<<32)
        priv['r'] = random.randrange(1<<32)
        priv['r_'] = priv['rz'] - e * priv['rw']
        # calc Cs
        params['Cs'] = gmpy2.powmod(pubkey['g'], s, pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['rs'], pubkey['n']) % pubkey['n']
        params['Ce'] = gmpy2.powmod(pubkey['g'], e, pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['re'], pubkey['n']) % pubkey['n']
        params['Cv'] = v * gmpy2.powmod(pubkey['g'], priv['w'], pubkey['n']) % pubkey['n']
        params['Cw'] = gmpy2.powmod(pubkey['g'], priv['w'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['rw'], pubkey['n']) % pubkey['n']
        priv['z'] = e * priv['w']
        params['C'] = gmpy2.powmod(params['Cv'], e, pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r'], pubkey['n']) % pubkey['n']
        params['Cx'] = gmpy2.powmod(pubkey['g'], uk, pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['rx'], pubkey['n']) % pubkey['n']
        params['Cz'] = gmpy2.powmod(pubkey['g'], priv['z'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['rz'], pubkey['n']) % pubkey['n']
        # calc ys
        params['y1'] = gmpy2.powmod(params['Cv'], priv['r1'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r2'], pubkey['n']) % pubkey['n']
        params['y2'] = gmpy2.powmod(pubkey['g'], priv['r1'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r3'], pubkey['n']) % pubkey['n']
        params['y3'] = gmpy2.powmod(pubkey['a'], priv['r4'], pubkey['n']) * gmpy2.powmod(pubkey['b'], priv['r5'], pubkey['n']) * \
            gmpy2.powmod(pubkey['g'], priv['r6'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r7'], pubkey['n']) % pubkey['n']
        params['y4'] = gmpy2.powmod(pubkey['g'], priv['r4'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r8'], pubkey['n']) % pubkey['n']
        params['y5'] = gmpy2.powmod(pubkey['g'], priv['r5'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r9'], pubkey['n']) % pubkey['n']
        params['y6'] = gmpy2.powmod(pubkey['g'], priv['r10'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r11'], pubkey['n']) % pubkey['n']
        params['y7'] = gmpy2.powmod(pubkey['g'], priv['r6'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r12'], pubkey['n']) % pubkey['n']
        params['y8'] = gmpy2.powmod(params['Cv'], priv['r10'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r7'], pubkey['n']) % pubkey['n']
        params['y9'] = gmpy2.powmod(pubkey['g'], priv['r13'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r14'], pubkey['n']) % pubkey['n']
        params['y10'] = gmpy2.powmod(pubkey['g'], priv['r15'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r16'], pubkey['n']) % pubkey['n']
        params['y11'] = gmpy2.powmod(pubkey['g'], priv['r17'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r18'], pubkey['n']) % pubkey['n']
        params['y12'] = gmpy2.powmod(params['Cw'], priv['r17'], pubkey['n']) * gmpy2.powmod(pubkey['h'], priv['r19'], pubkey['n']) % pubkey['n']
        params['y13'] = gmpy2.powmod(grnym, priv['r4'], settings.RNYM_PARAM['gamma'])
        # clac x
        params['x'] = hashing(
            params['C'], params['Cv'], params['Ce'],
            params['Cs'], params['Cx'], params['Cz'],
            params['Cw'], pubkey['g'], pubkey['h']
        )
        # clac z
        for i, j in enumerate((
            e, priv['r'], priv['re'], uk, s,
            priv['z'], priv['r'], priv['rx'], priv['rs'], e,
            priv['re'], priv['rz'], priv['z'], priv['rz'], priv['w'],
            priv['rw'], e, priv['re'], priv['r_']
            )):
            params['z{}'.format(i+1)] = priv['r{}'.format(i+1)] + params['x'] * j
        # clac rnym
        params['rnym'] = gmpy2.powmod(grnym, uk, settings.RNYM_PARAM['gamma'])
        rtval = {i: int(params[i]) for i in params}
        return rtval

    def test_verify_function(self):
        course_no = '2018-2019-2-231'
        params = self.gen_credentials(test_pubkey, 1223333, course_no)
        # vrfy
        self.assertEqual(verify(test_pubkey, str(course_no), **params), True)
        
    @override_settings(PUBKEY_TESTING=True)
    def test_init_api(self):
        client = Client()
        r = client.get('/api/v1/init?classno=666&semester=2018-2019-2')
        self.assertEqual(r.status_code, 200)

    @override_settings(PUBKEY_TESTING=True)
    def test_sign_api(self):
        course_no = '2018-2019-2-231'
        params = self.gen_credentials(test_pubkey, 1223333, course_no)
        self.assertEqual(verify(test_pubkey, course_no, **params), True)
        client = Client()
        r = client.post(
                '/api/v1/auth?classno=666&course_no={}'.format(course_no),
                {'credentials': params}, 
                content_type='application/json'
            )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'accept')