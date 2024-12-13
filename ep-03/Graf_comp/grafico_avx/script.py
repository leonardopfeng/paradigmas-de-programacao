import subprocess
import matplotlib.pyplot as plt
import re
import os

# Parâmetros de teste
k_pontos_n1 = [64, 128, 200, 256, 512, 600]  # K para N1 (grau 10)
k_pontos_n2 = [64, 128, 200, 256, 512]  # K para N2 (grau 1000)
grau_pol = [10, 1000]  # Valores de grau (também representando os valores de N)
grupos = ["FLOPS_DP", "ENERGY", "L3CACHE"]

# Submétricas dentro de FLOPS_DP
submetricas_flops = ["DP FLOPS", "AVX DP FLOPS"]

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

def processar_arquivos(data_dir, grupos):
    dados = {grupo: {} for grupo in grupos}  # Armazena os valores

    # Adiciona submétricas de FLOPS_DP
    dados["FLOPS_DP"] = {sub: {} for sub in submetricas_flops}

    for grupo in grupos:
        for subdir, _, files in os.walk(data_dir):
            for arquivo in files:
                if arquivo.startswith(grupo) and arquivo.endswith(".txt"):
                    match = re.search(r"_N(\d+)_K(\d+)\.txt", arquivo)
                    if not match:
                        continue  # Ignora arquivos com nomes inesperados
                    n = int(match.group(1))  # Captura N
                    k = int(match.group(2))  # Captura K
                    
                    with open(os.path.join(subdir, arquivo), "r") as f:
                        conteudo = f.read()

                        if grupo == "FLOPS_DP":
                            # Extrai valores para DP MFLOP/s e AVX DP MFLOP/s de todas as regiões
                            dp_matches = re.findall(r"DP MFLOP/s\s+\|\s+([\d\.e\+\-]+)", conteudo)
                            avx_matches = re.findall(r"AVX DP MFLOP/s\s+\|\s+([\d\.e\+\-]+)", conteudo)

                            # Converte valores em float e soma os encontrados
                            dp_total = sum(float(dp) for dp in dp_matches)
                            avx_total = sum(float(avx) for avx in avx_matches)

                            if k not in dados[grupo]["DP FLOPS"]:
                                dados[grupo]["DP FLOPS"][k] = dp_total
                            else:
                                dados[grupo]["DP FLOPS"][k] += dp_total

                            if k not in dados[grupo]["AVX DP FLOPS"]:
                                dados[grupo]["AVX DP FLOPS"][k] = avx_total
                            else:
                                dados[grupo]["AVX DP FLOPS"][k] += avx_total
                        elif grupo == "ENERGY":
                            # Extrai valores de energia de todas as regiões
                            energy_matches = re.findall(r"Energy \[J\]\s+\|\s+([\d\.e\+\-]+)", conteudo)
                            energy_total = sum(float(energy) for energy in energy_matches)

                            if k not in dados[grupo]:
                                dados[grupo][k] = energy_total
                            else:
                                dados[grupo][k] += energy_total
                        elif grupo == "L3CACHE":
                            # Extrai valores de L3 miss ratio de todas as regiões
                            l3_matches = re.findall(r"L3 miss ratio\s+\|\s+([\d\.e\+\-]+)", conteudo)
                            l3_total = sum(float(l3) for l3 in l3_matches)

                            if k not in dados[grupo]:
                                dados[grupo][k] = l3_total
                            else:
                                dados[grupo][k] += l3_total
    return dados

# Função para gerar gráficos
def gerar_grafico(dados_por_versao, grupos):
    os.makedirs("Graficos", exist_ok=True)

    for grupo in grupos:
        submetricas = submetricas_flops if grupo == "FLOPS_DP" else [grupo]

        for sub in submetricas:
            plt.figure(figsize=(10, 6))
            for version, dados in dados_por_versao.items():
                dados_sub = dados[grupo].get(sub, {}) if grupo == "FLOPS_DP" else dados[grupo]
                dados_grau_10 = {k: v for k, v in dados_sub.items() if k in k_pontos_n1}
                dados_grau_1000 = {k: v for k, v in dados_sub.items() if k in k_pontos_n2}

                tamanhos_10, valores_10 = zip(*sorted(dados_grau_10.items())) if dados_grau_10 else ([], [])
                tamanhos_1000, valores_1000 = zip(*sorted(dados_grau_1000.items())) if dados_grau_1000 else ([], [])

                plt.plot(tamanhos_10, valores_10, label=f"{version} + Grau 10", marker="o", linestyle="-")
                plt.plot(tamanhos_1000, valores_1000, label=f"{version} + Grau 1000", marker="x", linestyle="--")

            plt.title(f"Comparação de Métrica: {sub} - Grau 10 e Grau 1000")
            plt.xlabel("Tamanho da Matriz (escala logarítmica)")
            plt.ylabel(sub)
            plt.xscale("log")
            plt.grid(True)
            plt.legend()
            plt.savefig(os.path.join("Graficos", f"{sub.replace(' ', '_')}.png"))
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
