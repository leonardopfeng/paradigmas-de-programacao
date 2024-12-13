import subprocess
import matplotlib.pyplot as plt
import re
import os

# Parâmetros de teste
k_pontos = [64, 128, 256]
grau_pol = [10, 1000]
resultados_file = "resultados_teste.txt"
grupos = ["FLOPS_DP", "ENERGY", "L3CACHE"]
data_dir = "Resultados"

# Certifique-se de criar o diretório para armazenar os arquivos
os.makedirs(data_dir, exist_ok=True)

# Função para executar comando com LIKWID
def executar_comando(k, g, group):
    comando = f"./gera_entrada {k} {g} | likwid-perfctr -C 3 -g {group} -m ./ajustePol"
    try:
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar comando: {e}"

# Função para processar os resultados
def processar_arquivos(data_dir, grupos):
    dados = {grupo: {"tamanhos": [], "valores": []} for grupo in grupos}

    for grupo in grupos:
        for arquivo in os.listdir(data_dir):
            if arquivo.startswith(grupo) and arquivo.endswith(".txt"):
                tamanho = int(re.search(r"_(\d+)\.txt", arquivo).group(1))
                with open(os.path.join(data_dir, arquivo), "r") as f:
                    conteudo = f.read()
                    # Extração do valor da métrica
                    if grupo == "FLOPS_DP":
                        match = re.search(r"DP MFLOP/s\s+\|\s+([\d\.e\+\-]+)", conteudo)
                    elif grupo == "ENERGY":
                        match = re.search(r"Energy \[J\]\s+\|\s+([\d\.e\+\-]+)", conteudo)
                    elif grupo == "L3CACHE":
                        match = re.search(r"L3 miss ratio\s+\|\s+([\d\.e\+\-]+)", conteudo)
                    else:
                        match = None

                    if match:
                        valor = float(match.group(1))
                        dados[grupo]["tamanhos"].append(tamanho)
                        dados[grupo]["valores"].append(valor)
    return dados

# Função para gerar gráficos
def gerar_graficos(dados):
    for grupo, valores in dados.items():
        plt.figure(figsize=(10, 6))
        plt.plot(valores["tamanhos"], valores["valores"], marker="o", label=grupo)
        plt.title(f"Métrica: {grupo}")
        plt.xlabel("Tamanho da Matriz")
        plt.ylabel(grupo)
        plt.grid(True)
        plt.legend()
        plt.savefig(f"{grupo}_grafico.png")
        plt.close()

# Executa os testes e salva os resultados
with open(resultados_file, "w") as arquivo_resultados:
    for g in grau_pol:
        for k in k_pontos:
            for group in grupos:
                arquivo_resultados.write(f"Testando Kpontos={k}, GrauPol={g}, Grupo={group}\n")
            
                resultado = executar_comando(k, g, group)
                
                # Salvar resultados individuais em arquivos separados
                resultado_file = os.path.join(data_dir, f"{group}_{k}.txt")
                with open(resultado_file, "w") as f:
                    f.write(resultado)
                
                arquivo_resultados.write(f"Resultado:\n{resultado}\n")
                arquivo_resultados.write("=" * 40 + "\n")

# Processa os arquivos gerados para obter dados
dados_processados = processar_arquivos(data_dir, grupos)

# Gera gráficos a partir dos dados processados
gerar_graficos(dados_processados)

print("Testes concluídos. Resultados e gráficos gerados.")
