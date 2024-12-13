
# EP-03 

Trabalho que consiste em otimizar um código responsável por realizar um ajuste de curvas.
O objetivo é comparar a eficiência da solução otimizada, para a não otimizada, por meio de gráficos gerados com base nas informações dadas pelo LIKWID.


## Grupos testados no LIKWID

- FLOPS_DP (FLOPS_DP e AVX_FLOPS)
- ENERGY
- L3CACHE (Taxa de Cache Miss na L3)




## Otimizações

- COMPUTAÇÃO DAS POTÊNCIAS DE X
    - Código original: 
        - Calcula as potências repetidamente dentro de loops, usando a função não eficiente `pow()`;
    - Código otimizado: 
        - Pré-calcula as potências que vão ser necessárias dentro de uma matriz `potenciasX`, fazendo apenas o reaproveitamento dessa matriz dentro dos loops; 
        - Faz melhor aproveitamento da memória, já que precisa apenas recuperar os valores das potências já presentes em `potenciasX`, não sendo necessário recalcular as potências toda iteração;

- LOOP UNROLL
    - Código original
        - Itera elemento por elemento para cálcular as somas para `A` e `b`
    - Código otimizado;
        - Implementa loop unrolling de fator 4, melhorando o tempo e recursos consumidos ao se realizar o loop;
        - Explora melhor o `pipeline`;


- IMPLEMENTAÇÂO DE P 
    - Código original:
        - Recalcula as potências de X em cada termo;
    - Código otimizado:
        - Usa o `Método de Horner`, mais eficiente para avaliar polinômios, evitando multiplicações redundantes;
        - Diminui a complexidade do cálculo de `O(n²)` para `O(n)`;


## Resultados dos testes

Testes realizados com N máximo sendo 10⁵;
Os resultados podem ser visualizados, conforme a saída gerada pelo likwid, tanto em `v1_with_likwid/Resultados/`, quanto em `v2_with_likwid/Resultados/`

- DP FLOPS
    - `V2` usa menos `FLOPS`, fazendo cálculos mais eficientes, e em menos tempo, uma vez que usa menos operações de ponto flutuante para realizar a mesma tarefa que `V1`;
![image](https://github.com/user-attachments/assets/a9dfb73c-6350-4feb-8527-c7f5b547fd28)


- L3CACHE
    - Ambas seguem o mesmo padrão para valores relativamente pequenos `(10000)`, mas é nítido que a `V2` faz um melhor uso da `CACHE`, uma vez que tem menos quantidade de `CACHE MISS`;
    - Apesar de o uso do `Loop Unrolling` ajudar na questão de overhead do loop, e nos FLOPS, pode acabar resultando em um acesso não sequencial das informações, além de aumentar a pressão sobre a CACHE, que aumenta o número de operações por loop. Neste caso, o problema pode ser visto quando o valor de N é muito grande `(5*10⁴ e 10⁵)`;
![image](https://github.com/user-attachments/assets/10e614e2-0399-412b-b763-f420a2654caa)


- ENERGY
    - Ambas as versões seguem um padrão exponencial para os valores de `ENERGY`, quanto maior a entrada, maior o gasto energético para o cálculo. Apesar desse fato, a V2 faz um gasto consideralvemente menor;
    - Apesar de no gŕafico parecer que o valor de `ENERGY` é `0` para N's até `10³`, isso não é verdadeiro. O que ocorre é que a escala do gráfico, por ter valores muito altos no eixo y, faz com que valores pequenos de gasto energético `(1-200)`, aparentem ser `0`;
![image](https://github.com/user-attachments/assets/061f4f01-580c-4af3-92d2-c12b674b6bc7)


- AVX FLOPS
    - O `Loop Unrolling` pode ter afetado a CACHE, assim como explicado para L3CACHE, o que pode ter influenciado em como as instruções `AVX` são otimizadas no processador;
    - Apesar do `Overhead do Loop` ter diminuído com as implementações de otimização, para valores muito grandes, pode ter afetado a eficácia das instruções `AVX`, o que faz com que os ganhos de desempenho da `V2` não sejam evidentes ao se analisar este parâmetro;
![image](https://github.com/user-attachments/assets/61dcff6c-62de-4c4e-b3c2-d729f8d3b781)

    

## Rodando os testes

Se quiser rodar o código com os arquivos `.o` já fornecidos, siga os passos a seguir:

Acesse o diretório padrão, e rode o script.py

```bash
:~/lp24/ $ python3 script.py
```


Caso queria recompilar o projeto, siga os passos a seguir:

Acesse os diretórios `v1_with_likwid/` e `v2_with_likwid/`, e exclua os arquivos.o (make purge), então compile novamente (make)

```bash
:~/lp24/v1_with_likwid $ make purge
:~/lp24/v1_with_likwid $ make
:~/lp24/v2_with_likwid $ make purge
:~/lp24/v2_with_likwid $ make
:~/lp24/ $ python3 script.py
```


## Autor

- Leonardo Pfeng - 20244470

