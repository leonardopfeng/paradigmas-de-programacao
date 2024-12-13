#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <fenv.h>
#include <math.h>
#include <stdint.h>

#include "likwid.h"
#include "utils.h"

/////////////////////////////////////////////////////////////////////////////////////
//   AJUSTE DE CURVAS
/////////////////////////////////////////////////////////////////////////////////////


void montaSL(double **A, double *b, int n, long long int p, double *x, double *y) {
    double **potenciasX = (double **)malloc(p * sizeof(double *));
    for(long long int k = 0; k < p; ++k){
        potenciasX[k] = (double *)malloc((2 * n - 1) * sizeof(double));
        potenciasX[k][0] = 1.0;

        // Desenrolamento do loop para calcular potências de x[k]
        for (int exp = 1; exp < 2 * n - 1 - 3; exp += 4) {
            potenciasX[k][exp] = potenciasX[k][exp - 1] * x[k];
            potenciasX[k][exp + 1] = potenciasX[k][exp] * x[k];
            potenciasX[k][exp + 2] = potenciasX[k][exp + 1] * x[k];
            potenciasX[k][exp + 3] = potenciasX[k][exp + 2] * x[k];
        }

        // Loop para o restante (caso o número de potências não seja múltiplo de 4)
        for (int exp = 2 * n - 1 - (2 * n - 1) % 4; exp < 2 * n - 1; ++exp) {
            potenciasX[k][exp] = potenciasX[k][exp - 1] * x[k];
        }
    }

    // Preenchimento da matriz A
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            A[i][j] = 0.0;
            for (long long int k = 0; k < p; ++k) {
                A[i][j] += potenciasX[k][i + j];
            }
        }

    // Preenchimento do vetor b
    for (int i = 0; i < n; ++i) {
        b[i] = 0.0;
        for (long long int k = 0; k < p; ++k)
            b[i] += potenciasX[k][i] * y[k];
    }
}
void eliminacaoGauss(double **A, double *b, int n) {
    for (int i = 0; i < n; ++i) {
        int iMax = i;
        for (int k = i + 1; k < n; ++k) {
            if (fabs(A[k][i]) > fabs(A[iMax][i])) {
                iMax = k;
            }
        }

        // Troca de linhas se necessário
        if (iMax != i) {
            double *tmp = A[i];
            A[i] = A[iMax];
            A[iMax] = tmp;

            double aux = b[i];
            b[i] = b[iMax];
            b[iMax] = aux;
        }

        // Eliminação Gaussiana
        double pivot = A[i][i];
        for (int k = i + 1; k < n; ++k) {
            double m = A[k][i] / pivot;
            A[k][i] = 0.0;  // Elemento já zerado
            for (int j = i + 1; j < n; ++j) {
                A[k][j] -= A[i][j] * m;
            }
            b[k] -= b[i] * m;
        }
    }
}

void retrossubs(double **A, double *b, double *x, int n) {
    for (int i = n - 1; i >= 0; --i) {
        double soma = 0.0;
        for (int j = i + 1; j < n; ++j) {
            soma += A[i][j] * x[j];
        }
        x[i] = (b[i] - soma) / A[i][i];
    }
}

double P(double x, int N, double *alpha) {
    double Px = alpha[N];
    for (int i = N - 1; i >= 0; --i) {
        Px = Px * x + alpha[i];
    }
    return Px;
}

int main() {

  int N, n;
  long long int K, p;

  scanf("%d %lld", &N, &K);

  p = K;   // quantidade de pontos
  n = N+1; // tamanho do SL (grau N + 1)

  double *x = (double *) malloc(sizeof(double)*p);
  double *y = (double *) malloc(sizeof(double)*p);

  // ler numeros
  for (long long int i = 0; i < p; ++i)
    scanf("%lf %lf", x+i, y+i);

  double **A = (double **) malloc(sizeof(double *)*n);
  for (int i = 0; i < n; ++i)
    A[i] = (double *) malloc(sizeof(double)*n);
  
  double *b = (double *) malloc(sizeof(double)*n);
  double *alpha = (double *) malloc(sizeof(double)*n); // coeficientes ajuste

    LIKWID_MARKER_INIT;
    LIKWID_MARKER_START("MIN_QUAD");

  // (A) Gera SL
  double tSL = timestamp();
  montaSL(A, b, n, p, x, y);
  tSL = timestamp() - tSL;
    
    LIKWID_MARKER_STOP("MIN_QUAD");

    LIKWID_MARKER_START("GAUSS");

  // (B) Resolve SL
  double tEG = timestamp();
  eliminacaoGauss(A, b, n); 
  retrossubs(A, b, alpha, n); 
  tEG = timestamp() - tEG;

    LIKWID_MARKER_STOP("GAUSS");
    LIKWID_MARKER_CLOSE;

  printf("\n");

  // Imprime coeficientes
  for (int i = 0; i < n; ++i)
    printf("%1.15e ", alpha[i]);
  puts("");

  // Imprime resíduos
  for (long long int i = 0; i < p; ++i)
    printf("%1.15e ", fabs(y[i] - P(x[i],N,alpha)) );
  puts("");

  // Imprime os tempos
  printf("Quantidade de pontos: %lld Tempo para montar o sistema linear: %1.10e; Tempo para resolver o sistema linear %1.10e\n", K, tSL, tEG);

  return 0;
}
