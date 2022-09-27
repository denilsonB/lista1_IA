class Expressao: #classe para representar a exporessão, ex: A = SIM

    def __init__(self, var, opr, val):
        self.var = var
        self.opr = opr
        self.val = val
    
    def __str__(self):
        return self.var

    def comparar(self,outra_expressao):
        if (self.var == outra_expressao.var) and (self.opr == outra_expressao.opr) and (self.val==outra_expressao.val):
            return True
        return False

base_de_regras = []
base_de_fatos = []
objetivo = Expressao("","",True)
conclusao = Expressao("","=",True)

def atribui_conclusao(exp):
    conclusao.var = exp.var 
    conclusao.opr = exp.opr 
    conclusao.val = exp.val

def recebe_regras(qtd):
    print("as expressões separadas por &\n ex: A & B")
    for i in range(qtd):
        print("digite o(s) precedente(s) da {} regra".format(i + 1))
        antecedente = input("").split("&")

        expressoes_antecedentes = []

        for var in antecedente:# constroi os antecedentes
            var = var.strip()
            exp = Expressao(var, "=", True)
            expressoes_antecedentes.append(exp)

        print("digite o(s) consequente(s) da {} regra".format(i + 1))
        consequente = input("").split("&")

        expressoes_consequentes = []

        for var in consequente:# constroi os consequentes
            var = var.strip()
            exp = Expressao(var, "=", True)
            expressoes_consequentes.append(exp)

        regra = []
        regra.append(expressoes_antecedentes)
        regra.append(expressoes_consequentes)
        base_de_regras.append(regra)

def recebe_fatos(qtd):
    for i in range(qtd):
        print("Digite o {} fato ".format(i+1))
        var = input("")
        exp = Expressao(var, "=", True)
        base_de_fatos.append(exp)

def e_fato(meta):
    for exp in base_de_fatos:
        if exp.comparar(meta):
            return True
    return False

def estabelecer_um_fato(meta):
    if e_fato(meta):
        return True 
    copia_das_regras = base_de_regras.copy()
    return estabelecer1(copia_das_regras)

def estabelecer1(as_regras):
    if len(as_regras) == 0:
        return False
    uma_regra = as_regras.pop(0)
    for i in range(len(uma_regra[1])):
        if(uma_regra[1][i].comparar(conclusao)):
            if estabelecer2(uma_regra):
                return True
            
    estabelecer1(as_regras)

def estabelecer2(uma_regra):
    os_objetivos = uma_regra[0]
    consequentes = uma_regra[1]
    
    estabelecer_conj_fatos(os_objetivos,consequentes)


def estabelecer_conj_fatos(as_metas,consequentes):
    if len(as_metas) == 0:
        for exp in consequentes:
            if (e_fato(exp)) == False:
                base_de_fatos.append(exp)
        return True
    uma_meta = as_metas.pop(0)
    atribui_conclusao(uma_meta)
    estabelecer_um_fato(uma_meta)
    if e_fato(uma_meta) == False:
        atribui_conclusao(objetivo)
        return False
    estabelecer_conj_fatos(as_metas,consequentes)

def mostar_fatos():
    print("\nEsta é a base de fatos:")
    for i in base_de_fatos:
         print("fato ",i)

def main():
    print("Sistema baseados em conhecimento.\nResolvedor de sentenças no formato SE expressão ENTÃO expressão")
    
    qtd_de_regras = int(input("Digite a quantidade de regras: "))
    recebe_regras(qtd_de_regras)
    

    qtd_de_fatos = int(input("Digite a quantidade de fatos: "))
    recebe_fatos(qtd_de_fatos)
    
    obj = input("Digite o que deseja provar: ")
    objetivo.var = obj 
    objetivo.opr = "="
    objetivo.val = True
    atribui_conclusao(objetivo)
    
    estabelecer_um_fato(objetivo)

    mostar_fatos() 
    if (e_fato(objetivo)):
        print("Esta provado que",objetivo)
    else:
        print("Falso")
main()