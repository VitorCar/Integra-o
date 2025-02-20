# conetando ao banco de dados
import mysql.connector
cont = 0

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vitor',
    database='Integrando_py'
)

curso = conexao.cursor()

comando = 'SELECT * FROM cadastro'
curso.execute(comando)
resultado = curso.fetchall()
for r in resultado:
    cont += 1
print(cont)
print(resultado)





curso.close()
conexao.close()