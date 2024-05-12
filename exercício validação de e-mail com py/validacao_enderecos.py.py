import re
import csv

# Caminho do arquivo CSV com a lista de endereços
arquivo_csv_entrada = "arquivos-de-entrada.csv"

# Caminho do arquivo CSV para gravar os resultados da validação
arquivo_csv_saida = "arquivos-de-validacao.csv"

# Expressão regular para validar endereços
regex_endereco = r"""
    ^                    # Inicia no início da string
    (?P<logradouro>  .+?)  # Captura o logradouro (um ou mais caracteres)
    ,?\s+                # Espaço opcional e vírgula
    (?P<numero>       \d+) # Captura o número (somente dígitos)
    (?:\s+-\s+)?       # Hífen opcional com espaços
    (?P<complemento>   .+?) # Captura o complemento (um ou mais caracteres)
    (?:\s*,?\s+)?       # Vírgula e espaço opcionais
    (?P<bairro>        .+?) # Captura o bairro (um ou mais caracteres)
    (?:\s*,?\s+)?       # Vírgula e espaço opcionais
    (?P<cidade>        .+?) # Captura a cidade (um ou mais caracteres)
    (?:\s*,?\s+)?       # Vírgula e espaço opcionais
    (?P<estado>       [A-Z]{2}) # Captura o estado (duas letras maiúsculas)
    \s+(?P<cep>        \d{8}) # Espaço e CEP (8 dígitos)
    $                    # Termina no final da string
""", re.VERBOSE

# Abre os arquivos CSV em modo leitura e escrita
with open(arquivo_csv_entrada, "r", encoding="utf-8") as csv_entrada:
    with open(arquivo_csv_saida, "w", encoding="utf-8") as csv_saida:
        # Cria o objeto leitor de CSV
        leitor_csv = csv.reader(csv_entrada)

        # Cria o objeto escritor de CSV
        escritor_csv = csv.writer(csv_saida)

        # Escreve a primeira linha do arquivo de saída (cabeçalho)
        escritor_csv.writerow(["Logradouro", "Número", "Complemento", "Bairro", "Cidade", "Estado", "CEP", "Resultado", "Correção"])

        # Itera pelas linhas do arquivo de entrada (cada linha é um endereço)
        for linha in leitor_csv:
            # Extrai os campos do endereço
            logradouro = linha[0]
            numero = linha[1]
            complemento = linha[2]
            bairro = linha[3]
            cidade = linha[4]
            estado = linha[5]
            cep = linha[6]

            # Aplica a expressão regular para validar o endereço
            match = re.search(regex_endereco, linha[0:7])

            # Verifica se o endereço é válido
            if match:
                # Extrai os grupos da expressão regular (campos do endereço)
                dados_endereco = match.groupdict()

                # Formata o endereço para a saída
                endereco_formatado = f"{dados_endereco['logradouro']}, {dados_endereco['numero']}{dados_endereco['complemento'] if dados_endereco['complemento'] else ''} - {dados_endereco['bairro']}, {dados_endereco['cidade']}/{dados_endereco['estado']}, {dados_endereco['cep']}"

                # Grava o endereço válido no arquivo de saída
                escritor_csv.writerow([dados_endereco['logradouro'], dados_endereco['numero'], dados_endereco['complemento'], dados_endereco['bairro'], dados_endereco['cidade'], dados_endereco['estado'], dados_endereco['cep'], "Válido", ""])
            else:
                # Grava o endereço inválido no arquivo de saída
                escritor_csv.writerow([logradouro, numero, complemento, bairro, cidade, estado, cep, "Inválido", ""])
