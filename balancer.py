from math import gcd
from fractions import Fraction as fr
from colorama import Fore, init
init()
# New Version :
#   - known bugs fixed
#   - no need to install numpy anymore

# ================ Solve The System ================ #


class equation:
    def __init__(self, facts, ans):
        self.facts = facts
        self.ans = ans

    def change(self, value):
        for q in range(len(self.facts)):
            self.facts[q] *= value
        self.ans *= value


def check_sys(sys):
    if all([len(sys) == len(x.facts) for x in sys]):
        return True
    return False


def one_var(sys):
    if not check_sys(sys):
        raise Exception(f'check failed ! sys : {sys}')
    if len(sys) != 1:
        raise Exception(f'len(sys) = {len(sys)}')
    return fr(sys[0].ans, sys[0].facts[0])


def simplicate(sys):
    for eq in sys[1:]:
        eq.change(fr(sys[0].facts[-1], eq.facts[-1]))


def system(a, b):
    return [equation(a[c], b[c]) for c in range(len(b))]


def one_less(sys):
    new = []
    c = 1
    for eq in sys[1:]:
        last = sys[c-1]
        n = []
        o = 0
        for x in eq.facts:
            n.append(last.facts[o]-x)
            o += 1
        new.append(equation(n[:-1], last.ans-eq.ans))
        c += 1
    return new


def solve(sys):
    slvd = []
    ts = range(len(sys))
    for _ in ts:
        main = sys
        while not len(main) == 1:
            if all([x.facts[-1] != 0 for x in main]):
                simplicate(main)
            else:
                for eq in main:
                    if not eq.facts[-1] == 0:
                        eq.change(0)
            main = one_less(main)
        slvd.append(one_var(main))
        sys = [equation(x.facts[1:], x.ans-x.facts[0]*slvd[-1])
               for x in sys[:-1]]
    return slvd
# ================================================== #


class compound:
    suitables = set()
    unsuitables = set()
    all_elements = set()
    all_compounds = list()
    all_depends = list()
    includings = dict()

    def __init__(self, comp, _factor=1, side=None):
        compound.all_compounds.append(self)
        self.comp = comp
        self._factor = _factor
        self.elements = decompose(comp)
        self.side = side
        for element in self.elements:
            compound.all_elements.add(element)
        if self not in all_inside(compound.all_depends):
            compound.all_depends.append([self])

    def __repr__(self):
        return f'{self.factor}{self.comp}'

    def element_factor(self, element):
        return self.factor*self.elements.count(element)

    @classmethod
    def absolute(cls):
        for cmp in cls.all_compounds:
            cmp._factor = abs(cmp.factor)

    @classmethod
    def simplicate(cls):
        c = m_lcm([y.denominator for y in [
                  x.factor for x in cls.all_compounds]])
        d = m_gcd([y.numerator for y in [x.factor for x in cls.all_compounds]])
        for x in compound.all_compounds:
            x._factor = int(x._factor*fr(c, d))

    @classmethod
    def check(cls, print_it=True):
        not_balanced = []
        for element in cls.all_elements:
            if not sum([x.element_factor(element) for x in compound.all_compounds
                        if x.side == 'reagents']) == sum([x.element_factor(element)
                                                          for x in compound.all_compounds if x.side == 'products']):
                not_balanced.append(element)
        if len(not_balanced) > 0:
            if print_it:
                print(Fore.RED+'not balanced compounds :\r\t\t\t\t',
                      not_balanced, Fore.LIGHTWHITE_EX)
            return False
        if print_it:
            print(Fore.LIGHTBLUE_EX+'correct balancing : ' +
                  Fore.GREEN+'True'+Fore.RESET)
        return True

    @classmethod
    def find_suitable_elements(cls):
        reagents = [x for x in compound.all_compounds if x.side == 'reagents']
        products = [x for x in compound.all_compounds if x.side == 'products']
        for element in cls.all_elements:
            def func(side):
                counter = 0
                for cp in side:
                    if element in cp.elements:
                        counter += 1
                if counter == 1:
                    return element
            if func(reagents) and func(products):
                cls.suitables.add(element)

    @classmethod
    def find_unsuitable_elements(cls):
        cls.unsuitables.update(
            {x for x in cls.all_elements if x not in cls.suitables})

    @classmethod
    def update_includings(cls):
        for element in cls.all_elements:
            cls.includings.update(
                {element: [x for x in cls.all_compounds if element in x.elements]})

    @property
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, value):
        x = self._factor
        for comp in self.depends:
            comp._factor *= fr(value, x)

    @property
    def depends(self):
        for cmps in compound.all_depends:
            if self in cmps:
                return cmps

    @depends.setter
    def depends(self, value):
        p = self.depends+value.depends
        try:
            compound.all_depends.remove(self.depends)
            compound.all_depends.remove(value.depends)
        except ValueError:
            pass
        compound.all_depends.append(list(set(p)))

    @classmethod
    def clear(cls):
        cls.suitables = set()
        cls.unsuitables = set()
        cls.all_elements = set()
        cls.all_compounds = list()
        cls.all_depends = list()
        cls.includings = dict()


def all_inside(b):
    a = b.copy()
    res = []
    while not len(a) == 0:
        k = len(a)
        for x in range(k):
            x = a[x]
            if type(x) != list:
                res.append(x)
            else:
                for y in x:
                    a.append(y)
        a = a[k:]
    return res


def decompose(cpound):
    if cpound.count('(') != cpound.count(')'):
        raise NameError('invalid compounds!')
    if not any([x.isalpha() for x in cpound]):
        raise NameError('invalid compounds!')
    return_object = []
    cpound = cpound[::-1]
    limit = 0
    while not cpound == '':
        if limit == 1000:
            raise NameError(
                'not able to decompose your compounds!(check the limit in ".py" file)')
        a = 0
        while cpound[a].isdigit():
            a += 1
        if cpound[a] == ')':
            ending_para = len(cpound)-cpound[::-1].find('(')-1
            return_object.append(cpound[:ending_para+1])
            cpound = cpound[ending_para+1:]
        elif cpound[a].islower():
            return_object.append(cpound[:a+2])
            cpound = cpound[a+2:]
        elif cpound[a].isupper():
            return_object.append(cpound[:a+1])
            cpound = cpound[a+1:]
        limit += 1
    i = 0
    for comp in return_object:
        if comp[0].isdigit():
            a = 0
            while comp[a].isdigit():
                a += 1
            for _ in range(int(comp[:a][::-1])):
                return_object.insert(i, comp[a:])
            return_object.remove(comp)
        i += 1
    i = 0
    return_object = [x[::-1] for x in return_object]
    for comp in return_object:
        if comp[0] == '(':
            z = decompose(comp[1:-1])
            for x in z:
                return_object.insert(i, x)
            return_object.remove(comp)
        i += 1
    return return_object


def m_lcm(b):
    def lcm(a, b):
        return int(a*b/gcd(a, b))
    while not len(b) == 1:
        for i in range(len(b)):
            if not i in (0, len(b)):
                b[i] = lcm(b[i], b[i-1])
        b.pop(0)
    return b[0]


def m_gcd(b):
    while not len(b) == 1:
        for i in range(len(b)):
            if not i in (0, len(b)):
                b[i] = gcd(b[i], b[i-1])
        b.pop(0)
    return b[0]


def translate_input(reagents, products):
    for x in reagents, products:
        side = ['reagents', 'products'][x in products]
        x = x.replace(' ', '')
        x = x.split('+')
        x = [compound(y, side=side) for y in x]
        yield x


def show_result(reagents, products):
    for x in reagents:
        print(Fore.RED+str(x.factor), Fore.LIGHTWHITE_EX+str(x.comp), end='')
        if x == reagents[-1]:
            print(Fore.CYAN+' = ', end='')
        else:
            print(Fore.CYAN+' + ', end='')
    for x in products:
        print(Fore.RED+str(x.factor), Fore.LIGHTWHITE_EX+str(x.comp), end='')
        if x != products[-1]:
            print(Fore.CYAN+' + ', end='')
    print()


def main(reaction):
    try:
        if reaction == 'q':
            quit()
        elif reaction == '':
            return
        for x in ("--->", "-->", "->", "===>", "==>", "=>", "=", "→"):
            reaction = reaction.replace(x, '=')
        reagents, products = translate_input(*reaction.split('='))
        compound.find_suitable_elements()
        compound.find_unsuitable_elements()
        compound.update_includings()
        for suitable in compound.suitables:
            a, b = compound.includings[suitable]
            b.factor *= fr(a.element_factor(suitable),
                           b.element_factor(suitable))
            a.depends = b
        for cm in (x for x in compound.all_compounds if all(y in (compound.all_elements-compound.suitables) for y in x.elements)):
            for suitables_element in set(cm.elements):
                cm.factor = fr((sum([x.element_factor(suitables_element) for x in compound.all_compounds if x.side != cm.side]) - sum(
                    [x.element_factor(suitables_element) for x in compound.all_compounds if x.side == cm.side and not x == cm])), cm.elements.count(suitables_element))
        if not compound.check(False):
            mains = []
            for x in compound.all_depends:
                x = list(x)
                d = [reaction.find(l.comp) for l in x]
                main = x[d.index(min(d))]
                mains.append(main)
            factors = []
            answers = []
            for main in mains:
                main.factor = 1
            while len(compound.unsuitables) > len(compound.all_depends):
                compound.unsuitables.pop()
            for unsuitable in compound.unsuitables:
                f = []
                answers.append(fr(sum(
                    [-x.element_factor(unsuitable) if x in reagents else x.element_factor(unsuitable)for x in mains[0].depends])))
                for i in mains[1:]:
                    f.append(fr(sum([x.element_factor(
                        unsuitable) if x in reagents else -x.element_factor(unsuitable) for x in i.depends])))
                factors.append(f)
            answer = [fr(x).limit_denominator()
                        for x in solve(system(factors, answers))]
            for main in mains[1:]:
                main.factor = answer[mains.index(main)-1]
        compound.check()
        compound.absolute()
        compound.simplicate()
        show_result(reagents, products)
        compound.clear()
    except KeyboardInterrupt:
        quit()
    except Exception as err:
        compound.clear()
        print(
            Fore.RED + f'an error has occured !!! (Error Message : {err})\nplease check the reaction and try again ...'+Fore.RESET)


reactions = [
    'Ba(OH)2 + HCl = BaCl2 + H2O',
    'Cu +  HNO3 = Cu(NO3)2 + NO + H2O',
    'H2SO4 + HI = H2S + I2 + H2O',
    'Ba3N2 +  H2O =  Ba(OH)2 +  NH3',
    'CaCl2 +  Na3PO4 = Ca3(PO4)2 +  NaCl',
    'FeS + O2 = Fe2O3 + SO2',
    'PCl5 +  H2O = H3PO4 + HCl',
    'As + NaOH =  Na3AsO3 + H2',
    'Hg(OH)2 + H3PO4 = Hg3(PO4)2 + H2O',
    'HClO4 + P4O10 = H3PO4 + Cl2O7',
    'CO + H2 = C8H18 + H2O',
    'KClO3 + P4 = P4O10 + KCl',  #
    'SnO2 + H2 = Sn + H2O',
    'KOH + H3PO4 = K3PO4 + H2O',
    'KNO3 + H2CO3 = K2CO3 +  HNO3',
    'Na3PO4 + HCl = NaCl + H3PO4',
    'TiCl4 + H2O = TiO2 + HCl',
    'C2H6O + O2 = CO2 + H2O',
    'Fe + HC2H3O2 = Fe(C2H3O2)3 + H2',
    'NH3 + O2 = NO + H2O',
    'B2Br6 + HNO3 = B(NO3)3 + HBr',
    'Ba(OH)2 + HCl = BaCl2 + H2O',
    'C5H12 + O2 = CO2 + H2O',
    'Ca(OH)2 + H3PO4 = Ca3(PO4)2 + H2O',
    'CO2 + H2O = C6H12O6 + O2 ',
    'SiCl4 + H2O = H4SiO4 + HCl',
    'Al + HCl = AlCl3 + H2',
    'Na2CO3 + HCl = NaCl + H2O + CO2',
    'C7H6O2 + O2 = CO2 + H2O',
    'Fe2(SO4)3 + KOH = K2SO4 + Fe(OH)3',
    'KClO3 = KClO4 + KCl',
    'Al2(SO4)3 + Ca(OH)2 = Al(OH)3 + CaSO4',
    'H2SO4 + HI = H2S + I2 + H2O',  #
    'H2C2O4 + NaOH = Na2C2O4 + H2O',
    'Cu + HNO3 = Cu(NO3)2 + NO + H2O'
]


if __name__ == '__main__':
    print(
        Fore.RED+'[*] you can split reaction by \
"=" / "=>" / "==>" / "===>" / "→" / "->" / "-->" / "--->" (spaces are not \
necessary)\nenter "q" to exit\n'+Fore.YELLOW +
        '[*] example : Hg(OH)2 + H3PO4 = Hg3(PO4)2 + H2O\n' +
        Fore.GREEN + '[*] if you want to see some more examples, enter "test"')
    while 1:
        print(Fore.CYAN+'reaction : ' +
              Fore.YELLOW, end='')
        reaction = input()
        if reaction.upper() == 'TEST':
            for reaction in reactions:
                print(Fore.LIGHTBLUE_EX+'reaction : ' +
                      Fore.LIGHTWHITE_EX+reaction)
                main(reaction)
                print(Fore.YELLOW+'------------'+Fore.RESET)
        else:
            main(reaction)
        print(Fore.RED+'(q=>exit)')
