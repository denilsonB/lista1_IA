#Denilson Bulhões da Rosa Silva
#José Arthur Lopes
class Expressao: #classe para representar a exporessão, ex: A = SIM

    def __init__(self, var, opr, val):
        self.var = var
        self.opr = opr
        self.val = val

    def __str__(self):
        return self.var

    def variavel(self):
        if self.val == True:
            return self.var
        return "~" + self.var
    
    def valor(self):
        if self.val == True:
            return "SIM"
        else:
            return "NÃO"

    def comparar(self,outra_expressao):
        if(self.var == outra_expressao.var) :
            return True
        else:
            return False
    def comparar_exatidao(self,outra_expressao):
        if(self.var == outra_expressao.var) and (self.opr == outra_expressao.opr) and (self.val == outra_expressao.val):
            return True
        else:
            return False
base_de_regras = []
base_de_fatos = []
objetivo = Expressao("","",True)

def recebe_regras(qtd):
    print("as expressões separadas por &\n ex: A & B\n negações com o simbolo de ~ ex: ~A")
    for i in range(qtd):
        print("digite o(s) precedente(s) da {} regra".format(i + 1))
        antecedente = input("").split("&")
        expressoes_antecedentes = []

        for var in antecedente:# constroi os antecedentes
            var = var.strip()
            exp = Expressao(var, "=", True)
            if var[0] == '~':
                exp.var = var[1:]
                exp.val = False
            expressoes_antecedentes.append(exp)

        print("digite o(s) consequente(s) da {} regra".format(i + 1))
        consequente = input("").split("&")

        expressoes_consequentes = []

        for var in consequente:# constroi os consequentes
            var = var.strip()
            exp = Expressao(var, "=", True)
            if var[0] == '~':
                exp.var = var[1:]
                exp.val = False
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
        if var[0] == '~':
            exp.var = var[1:]
            exp.val = False
            modus_tollens(exp)
        base_de_fatos.append(exp)

def e_fato(elemento):
    for exp in base_de_fatos:
        if exp.comparar(elemento):
            return True
    return False

def remove_regra_da_base(uma_regra):
    for i in range(len(base_de_regras)):
        if uma_regra == base_de_regras[i]:
            base_de_regras.pop(i)
            break

def valida_regra(uma_regra):
    fatos_antecedentes = '&'.join(exp.var for exp in uma_regra[0])
    exp = Expressao(fatos_antecedentes,"=",True)    
    if e_fato(exp):
        return True
    
    premissas = 0
    for antecedente in uma_regra[0]:
        if e_fato(antecedente) :
            premissas+=1
            if premissas == len(uma_regra[0]):
                fatos_antecedentes = '&'.join(exp.var for exp in uma_regra[0])
                exp = Expressao(fatos_antecedentes,"=",True)
                if e_fato(exp) == False:
                    base_de_fatos.append(exp)
                return True
    return False

def modus_tollens(um_fato):# ta errado, diz que é sim msm sem ser por algum motivo, deve ser culpa daqui
    #percorre a base de regras
    #verifico se meu fato é o consequente de alguma
    #nego o antecedente e o adiciono na base de regras
    for i in range(len(base_de_regras)):
        fatos_antecedentes = '&'.join(exp.var for exp in base_de_regras[i][1])
        exp = Expressao(fatos_antecedentes,"=",False)        
        if um_fato.comparar_exatidao(exp):
            fatos_antecedentes = '&'.join(exp.var for exp in base_de_regras[i][0])
            exp = Expressao(fatos_antecedentes,"=",False)
            if e_fato(exp) == False:
                base_de_fatos.append(exp)

def silogismo_hipotetico():
    for i in range(len(base_de_regras)):
        consequente = base_de_regras[i][1][0]
        for j in range(len(base_de_regras)):
            if(len(base_de_regras[j][0]) > 1 ):
                continue
            fato_antecedente = base_de_regras[j][0][0]
            if (consequente.comparar_exatidao(fato_antecedente)):
                antecedente_regra = base_de_regras[i][0]
                consequente_regra = base_de_regras[j][1]
                regra = []
                regra.append(antecedente_regra)
                regra.append(consequente_regra)
                base_de_regras.append(regra)

def estabelecer_um_fato(meta):
    if e_fato(meta) :
        return True
    #base_de_regras.sort(key=lambda e: len(e[0]))
    copia_das_regras = base_de_regras.copy()
    executar_um_ciclo(copia_das_regras)

def executar_um_ciclo(as_regras):
    if len(as_regras) == 0:
        return False

    uma_regra = as_regras.pop(0)
    if valida_regra(uma_regra):
        if objetivo.comparar_exatidao(uma_regra[1][0]):
            base_de_fatos.append(objetivo)
            return True
        if (e_fato(uma_regra[1][0]) == False):#verifica se o consequente não está na base de fatos
                base_de_fatos.append(uma_regra[1][0])
                if(uma_regra[1][0].val == False):
                    modus_tollens(uma_regra[1][0])
                
        remove_regra_da_base(uma_regra)
        executar_um_ciclo(base_de_regras)
        return
    executar_um_ciclo(as_regras)

def valida_objetivo():
    for exp in base_de_fatos:
        if objetivo.comparar_exatidao(exp):
            return True
    return False

def mostar_fatos():
    print("\nEsta é a base de fatos:")
    for i in base_de_fatos:
         print("fato ",i)

def mostar_regras(base_original):
    print("\nEstá é a base de regras:")
    for i in range(len(base_original)):
        fatos_antecedentes = '&'.join(exp.var for exp in base_original[i][0])
        fato_consequente = base_original[i][1][0]
        if base_original[i][0][0].val == False:
            fatos_antecedentes = '~' + fatos_antecedentes
        if fato_consequente.val == False:
            fato_consequente.var = '~' + fato_consequente.var
        print(fatos_antecedentes,"-->",base_original[i][1][0].var)
def refazer_base(base_original):
    for regra in base_original:
        base_de_regras.append(regra)

def main():
    print("Sistema baseados em conhecimento.\nResolvedor de sentenças no formato SE expressão ENTÃO expressão")
    
    qtd_de_regras = int(input("Digite a quantidade de regras: "))
    recebe_regras(qtd_de_regras)
    
    silogismo_hipotetico()
    base_original = base_de_regras.copy()

    qtd_de_fatos = int(input("Digite a quantidade de fatos: "))
    recebe_fatos(qtd_de_fatos)
    
    obj = input("Digite o que deseja provar: ")
    objetivo.var = obj 
    objetivo.opr = "="
    objetivo.val = True
    if obj[0] == '~':
        objetivo.var = obj[1:]
        objetivo.val = False
    
    estabelecer_um_fato(objetivo)
    if valida_objetivo == False:
        refazer_base(base_original)
        estabelecer_um_fato
    mostar_regras(base_original)
    mostar_fatos()
    if valida_objetivo():
        print("\nEstá provado",objetivo)
    else:
        print("\nÉ falso que ",objetivo)
main()
