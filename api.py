from asyncio.windows_events import NULL
import requests
import json
import psycopg2

#busca na api o a partir do cnpj solicitado retornando os dados
# CNPJ
# NOME
# CIDADE
# ESTADO
def buscar_dados_por_cnpj(cnpj):
    request = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpj}")
    return_request = json.loads(request.content)
    return return_request


#Faz a conexão com o banco de dados
def conecta_db():
    try:
        con = psycopg2.connect(host='localhost', 
                            database='sensedia',
                            user='postgres', 
                            password='sensedia')
        print("Conexão Feita com sucesso")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Não foi Possivel conectar ao banco")        
        return 1
    return con

#Faz as consultas sql retornando em uma lista
def consultar_db(sql):
    con = conecta_db()
    if(con != 1):
        cur = con.cursor()
        cur.execute(sql)
        recset = cur.fetchall()
        registros = []
        for rec in recset:
            registros.append(rec)
        cur.close()
        con.close()    
        return registros
    else :
        print("Não foi possivel fazer a conexão com o banco para procurar dados!")
        return 1

# Inserir dados a partir de uma SQL passada 
def inserir_db(sql):
    con = conecta_db()
    if(con != 1):
        cur = con.cursor()    
        try:
            cur.execute(sql)
            con.commit()
            print("Inserido com sucesso")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Não foi possivel fazer o insert")
            con.rollback()
            cur.close()
            return 1
        cur.close()
        con.close()
    else: 
        print("Não foi possivel fazer a conexão com o banco para inserir dados!")
        return 1

#Classe main em python lembrando que só da pra rodar 3 vezes o código por minuto se não a api não retorna dados
if __name__ == '__main__':
    digita_cnpj = input("Digite um cnpj para busca: ")
    #validação de cnpj
    while len(digita_cnpj) < 14:
        digita_cnpj = input("Por favor digite um cnpj válido para busca: ")

    produto_busca_request = buscar_dados_por_cnpj(digita_cnpj)

    print(f"{produto_busca_request['cnpj']}")
    print(f"{produto_busca_request['nome']}")
    print(f"{produto_busca_request['municipio']}")
    print(f"{produto_busca_request['uf']}")
    print(f"{produto_busca_request['cep']}")

    sql = """
    SELECT * FROM cad_cnpj WHERE cnpj = '%s'
    """% (produto_busca_request[0])
    
    cons_cnpj = consultar_db(sql)
    
    if(cons_cnpj != 1):
        if(len(cons_cnpj) <= 0):   
            sql = """
            INSERT into cad_cnpj(cnpj, nome_cliente, cidade, estado,cep) 
            values('%s','%s','%s', '%s','%s');
            """ % (produto_busca_request[0], produto_busca_request[1], produto_busca_request[2], produto_busca_request[3], produto_busca_request[4])
            inserir_db(sql)
            cons_cnpj = consultar_db('select * from cad_cnpj;')
            print(cons_cnpj)
        else :
            print('CNPJ já tá cadastrado no banco!')
            cons_cnpj = consultar_db('select * from cad_cnpj;')
            print(cons_cnpj)
    else:
        print("Programa encerrado não tem conexão com o banco!")

