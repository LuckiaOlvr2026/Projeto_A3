# cronograma.py
import plano_mestre

arquivo = "estoque.txt"

def carregar_ordens_compra():
    """Lê as ordens de compra tratadas do arquivo texto"""
    ordens = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return ordens
    
    lendo_ordens = False
    for linha in linhas:
        linha = linha.strip()
        
        # Pega a exata marcação que você usou no data.py
        if linha == "===== ORDENS COMPRA =====":
            lendo_ordens = True
            continue
        elif linha.startswith("====="):
            if lendo_ordens:
                break
        
        if lendo_ordens and linha:
            partes = linha.split("|")
            
            # Tratando os dados: "Rodinhas|40un|3sem"
            componente = partes[0]
            quantidade = int(partes[1].replace("un", "").strip())
            semana = int(partes[2].replace("sem", "").strip())
            
            ordens.append({
                "componente": componente,
                "quantidade": quantidade,
                "semana": semana
            })
            
    return ordens

def exibir_cronograma():
    """Desenha a tabela usando as funções do seu plano_mestre"""
    ordens = carregar_ordens_compra()
    
    plano_mestre.separação()
    print("\033[34mCRONOGRAMA DE COMPRAS\033[m".center(58)) # Centralizado contando com os códigos de cor
    plano_mestre.separação()

    if not ordens:
        print("\nNenhuma ordem de compra registrada ainda!\n")
        return
    
    # Agrupa os itens por componente e semana
    matriz = {}
    for ordem in ordens:
        comp = ordem['componente']
        semana = ordem['semana']
        qtd = ordem['quantidade']
        
        if comp not in matriz:
            matriz[comp] = [0] * 8 # Matriz para 8 semanas
        
        if 1 <= semana <= 8:
            matriz[comp][semana - 1] += qtd
    
    # Imprimindo o cabeçalho
    print(f"{'Componente':<15} | ", end="")
    for s in range(1, 9):
        print(f"S{s:<4} | ", end="")
    print("\n" + "-" * 75)
    
    # Imprimindo o corpo da matriz
    for componente, semanas in sorted(matriz.items()):
        print(f"{componente:<15} | ", end="")
        for qtd in semanas:
            if qtd > 0:
                print(f"{qtd:<4} | ", end="")
            else:
                print(f"{'--':<4} | ", end="")
        print()
    
    print("-" * 75)
    print("Legenda: -- = Sem necessidade de compra na semana")