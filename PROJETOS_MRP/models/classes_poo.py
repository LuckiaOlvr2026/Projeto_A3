import data # Importa o seu arquivo data.py para usar a persistência

class Componente:
    def __init__(self, nome, estoque_inicial, lead_time):
        self.nome = nome
        self.estoque = estoque_inicial
        self.lead_time = lead_time
    
    def consumir(self, quantidade, motivo=""):
        """Reduz o estoque e registra no data.py"""
        if quantidade > self.estoque:
            print(f"\033[31mATENÇÃO: Estoque insuficiente de {self.nome}!\033[m")
            return False
        
        self.estoque -= quantidade
        # Usa a função do seu data.py
        data.adicionar_movimentaçao("CONSUMO", self.nome, quantidade, motivo)
        return True
    
    def adicionar(self, quantidade, motivo="Entrada manual"):
        """Aumenta o estoque e registra no data.py"""
        self.estoque += quantidade
        data.adicionar_movimentaçao("ENTRADA", self.nome, quantidade, motivo)
    
    def __str__(self):
        return f"{self.nome}: {self.estoque}un (LT: {self.lead_time}sem)"
    
    def to_dict(self):
        """Prepara os dados para serem salvos pelo data.salvar_estoque()"""
        return {
            "estoque": f"{self.estoque}un", 
            "lead_time": f"{self.lead_time}sem"
        }

class ProdutoAcabado:
    def __init__(self, nome, receita_dict):
        self.nome = nome
        self.receita = receita_dict
    
    def listar_componentes(self):
        print(f"\n📋 BOM - {self.nome}")
        for comp, qtd in self.receita.items():
            print(f"  - {qtd}un {comp}")
    
    def calcular_necessidade_total(self, quantidade_produzir):
        necessidades = {}
        for comp, qtd_unit in self.receita.items():
            necessidades[comp] = quantidade_produzir * qtd_unit
        return necessidades