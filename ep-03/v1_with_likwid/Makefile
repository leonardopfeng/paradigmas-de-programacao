# Diretórios e variáveis
LIKWID_HOME=/home/soft/likwid
CFLAGS=-O3 -mavx -march=native -lm -I${LIKWID_HOME}/include -DLIKWID_PERFMON
LFLAGS=-L${LIKWID_HOME}/lib -llikwid

# PROGRAMA
PROG = ajustePol gera_entrada

# Compilador
CC     = gcc

# Lista de arquivos para distribuição.
# LEMBRE-SE DE ACRESCENTAR OS ARQUIVOS ADICIONAIS SOLICITADOS NO ENUNCIADO DO TRABALHO
DISTFILES = *.c *.h LEIAME* Makefile 
DISTDIR = `basename ${PWD}`

.PHONY: all clean purge dist

# Regra para compilar todos os programas
all: $(PROG)

# Regras para compilar cada programa
ajustePol: ajustePol.o utils.o
	$(CC) -o $@ $^ $(CFLAGS) $(LFLAGS)

gera_entrada: gera_entrada.o utils.o
	$(CC) -o $@ $^ $(CFLAGS) $(LFLAGS)

# Regras para arquivos objetos, com dependência explícita de utils.h
ajustePol.o: ajustePol.c utils.h
	$(CC) $(CFLAGS) -c $<

gera_entrada.o: gera_entrada.c utils.h
	$(CC) $(CFLAGS) -c $<

utils.o: utils.c utils.h
	$(CC) $(CFLAGS) -c $<

# Regra genérica (opcional, usada para outros casos)
%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	@echo "Limpando sujeira ..."
	@rm -f *~ *.bak core *.o

purge: clean
	@echo "Limpando tudo ..."
	@rm -f $(PROG) a.out $(DISTDIR) $(DISTDIR).tar

dist: purge
	@echo "Gerando arquivo de distribuição ($(DISTDIR).tar) ..."
	@ln -s . $(DISTDIR)
	@tar -cvf $(DISTDIR).tar $(addprefix ./$(DISTDIR)/, $(DISTFILES))
	@rm -f $(DISTDIR)
