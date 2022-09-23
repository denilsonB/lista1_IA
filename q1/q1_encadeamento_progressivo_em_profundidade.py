#Array base de regras
#Array fatos
#var objetivo
#percorrer e resolver
#classe de expressoes e sentencas
# for em base_de_regras[x][1]
# procuro o objetivo
# pego a regra
# repito
#pensar em como expandir o exeplo 3
#quero provar pagamento
#mudar os fatos
class Expressao: #classe para representar a exporessão, ex: A = SIM

    def __init__(self, var, opr, val):
        self.var = var
        self.opr = opr
        self.val = val

    def __str__(self):
        return self.var + " " + self.opr + " " + self.valor()

    def valor(self):
        if self.val == True:
            return "SIM"
        else:
            return "NÃO"

    def comparar(self,outra_expressao):
        if((self.var == outra_expressao.var) and (self.opr == outra_expressao.opr) and (self.val == outra_expressao.val)):
            return True
        else:
            return False

base_de_regras = []
base_de_fatos = []
objetivo = Expressao("","",True)

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

def e_fato(elemento):
    for exp in base_de_fatos:
        if exp.comparar(elemento):
            return True
    return False

def remove_regra_da_base(uma_regra):
    for i in range(len(base_de_regras)):
        if uma_regra == base_de_regras[0]:
            base_de_regras.pop(i)
            break

def estabelecer_um_fato(meta):
    if e_fato(meta) :
        return True
    copia_das_regras = base_de_regras.copy()
    executar_um_ciclo(copia_das_regras)

def executar_um_ciclo(as_regras):
    if len(as_regras) == 0:
        return False
    uma_regra = as_regras.pop(0)
    
    premissas = 0
    for antecedente in uma_regra[0]:

        if e_fato(antecedente) :
            premissas+=1
            if premissas == len(uma_regra[0]):
                if objetivo.comparar(uma_regra[1][0]):
                    base_de_fatos.append(objetivo)
                    return True
                if (e_fato(uma_regra[1][0]) == False):#verifica se o consequente já está na base de fatos
                    base_de_fatos.append(uma_regra[1][0])
                remove_regra_da_base(uma_regra)
                executar_um_ciclo(base_de_regras)
                return
    executar_um_ciclo(as_regras)

def printar():
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
    estabelecer_um_fato(objetivo)
    printar()
    if e_fato(objetivo):
        print("\nEstá provado que ",objetivo)
    else:
        print("\nÉ falso que ",objetivo)
main()
