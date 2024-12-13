import subprocess
import matplotlib.pyplot as plt
import re
import os

# Parâmetros de teste
k_pontos_n1 = [64, 128, 200, 256]  # K para N1 (grau 10)
k_pontos_n2 = [64, 128, 200]  # K para N2 (grau 1000)
grau_pol = [10, 1000]  # Valores de grau (também representando os valores de N)
grupos = ["FLOPS_DP", "ENERGY", "L3CACHE"]

# Diretórios das versões
versoes = {
    "v1_with_likwid": "./v1_with_likwid/",
    "v2_with_likwid": "./v2_with_likwid/"
}

# Função para executar comando com LIKWID
def executar_comando(k, g, group, version_dir, data_dir_grau, n):
    comando = f"./gera_entrada {k} {g} | likwid-perfctr -C 3 -g {group} -m ./ajustePol"
    try:
        print(f"Executando ({version_dir}): K={k}, Grau={g}, Grupo={group}, N={n}")
        resultado = subprocess.run(
            comando,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=version_dir  # Define o diretório da versão
        )
        resultado_file = os.path.join(data_dir_grau, f"{group}_N{n}_K{k}.txt")
        with open(resultado_file, "w") as f:
            f.write(resultado.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando para K={k}, Grau={g}, Grupo={group}, N={n} na versão {version_dir}: {e}")
        return None

# Função para processar os resultados
def processar_arquivos(data_dir, grupos):
    dados = {grupo: {} for grupo in grupos}  # Usa dicionários para armazenar o maior valor por K

    for grupo in grupos:
        for subdir, _, files in os.walk(data_dir):
            for arquivo in files:
                if arquivo.startswith(grupo) and arquivo.endswith(".txt"):
                    match = re.search(r"_N(\d+)_K(\d+)\.txt", arquivo)
                    n = int(match.group(1))  # Captura N
                    k = int(match.group(2))  # Captura K
                    
                    with open(os.path.join(subdir, arquivo), "r") as f:
                        conteudo = f.read()
                        
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
                            # Atualiza com o maior valor encontrado para o mesmo K
                            if k not in dados[grupo] or valor > dados[grupo][k]:
                                dados[grupo][k] = valor
    return dados

# Função para gerar gráficos
def gerar_grafico(dados_por_versao, grupos):
    os.makedirs("Graficos", exist_ok=True)

    for grupo in grupos:
        plt.figure(figsize=(10, 6))

        for version, dados in dados_por_versao.items():
            # Grau 10
            dados_grau_10 = {k: v for k, v in dados[grupo].items() if k in k_pontos_n1}
            tamanhos_10, valores_10 = zip(*sorted(dados_grau_10.items())) if dados_grau_10 else ([], [])
            plt.plot(tamanhos_10, valores_10, label=f"{version} + Grau 10", marker="o", linestyle="-")

            # Grau 1000
            dados_grau_1000 = {k: v for k, v in dados[grupo].items() if k in k_pontos_n2}
            tamanhos_1000, valores_1000 = zip(*sorted(dados_grau_1000.items())) if dados_grau_1000 else ([], [])
            plt.plot(tamanhos_1000, valores_1000, label=f"{version} + Grau 1000", marker="x", linestyle="--")

        plt.title(f"Comparação de Métrica: {grupo} - Grau 10 e Grau 1000")
        plt.xlabel("Tamanho da Matriz (escala logarítmica)")
        plt.ylabel(grupo)
        plt.xscale("log")
        plt.grid(True)
        plt.legend()
        plt.savefig(os.path.join("Graficos", f"{grupo}.png"))
        plt.close()

# Executa os testes e processa os resultados
dados_por_versao = {version: {grupo: {} for grupo in grupos} for version in versoes}

for version, version_dir in versoes.items():
    for n in grau_pol:
        data_dir_grau = os.path.join(version_dir, "Resultados", f"grau_{n}")
        os.makedirs(data_dir_grau, exist_ok=True)

        k_pontos = k_pontos_n1 if n == 10 else k_pontos_n2
        for k in k_pontos:
            for group in grupos:
                executar_comando(k, n, group, version_dir, data_dir_grau, n)

        dados_por_versao[version] = processar_arquivos(os.path.join(version_dir, "Resultados"), grupos)

# Gera gráficos
gerar_grafico(dados_por_versao, grupos)

print("Testes concluídos. Gráficos gerados no diretório 'Graficos'.")