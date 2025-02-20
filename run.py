import customtkinter as ctk
import customtkinter


# conetando ao banco de dados
import mysql.connector

#FUNÇÃO DE ADICIONAR AO BANCO DE DADOS
def valores(nm, nasc: str, c: str):
    """
    :param nm: Vai retornar o nome
    :param nasc: retorno nascimento
    :param c: CPF
    :return: none
    """
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vitor',
            database='Integrando_py'
        )

        curso = conexao.cursor()

        #comando sql_adicionar seguro com placeholders= %s valores que sao passados depois
        comando = 'INSERT INTO cadastro (nome, nascimento, cpf) VALUES (%s, %s, %s)'
        valores = (nm, nasc, c)

        curso.execute(comando, valores)

        #confirmando a inserção
        conexao.commit()
        print('Dados inseridos com sucesso!')


    except mysql.connector.Error as erro:
        print(f'ERROR ao inserir os dados: {erro}')

    finally:
        curso.close()
        conexao.close()


# FUNÇAO QUE SERA CHAMADA QUANDO O BOTAO FOR PRESSIONADO
def precionar():
    nome = entrada_nome.get() #obtendo o valor do campo nome
    nascimento = entrada_data.get()  # obtendo o valor do campo nascimento
    cpf = entrada_cpf.get()
    if nome and nascimento and cpf:
        valores(nome, nascimento, cpf)
        entrada_nome.delete(0, 'end') #limpa o campo nome
        entrada_data.delete(0, 'end') #limpa o campo data
        entrada_cpf.delete(0, 'end')

    else:
        print('ERROR...PREENCHA AMBOS OS CAMPOS!')


#FUNÇÃO DELETE
def delete(n: str, idn: int):
    """

    :param n: retorn nome
    :param idn:  id banco de dados
    :return: None
    """
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='vitor',
            database='Integrando_py'
        )

        curso = conexao.cursor()

        comando = 'DELETE FROM cadastro WHERE nome = %s AND id = %s'
        valores = (n, str(idn)) # convertendo idn para str

        curso.execute(comando, valores)
        conexao.commit()

        # Verificar se algum dado foi removido
        if curso.rowcount > 0:
            print('Dado removido com sucesso!')
        else:
            print('Nenhum dado encontrado com esse nome e ID.')


    except mysql.connector.Error as erro:
        print(f'ERROR ao remover dados: {erro}')

    finally:
        curso.close()
        conexao.close()

#usar enter
def apertar_enter(event, proximo_campo):
    proximo_campo.focus_set()


#.........CRIANDO JANELA........

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

janela = customtkinter.CTk()
janela.geometry('600x600')

# criar titulo e entrada
titulo = customtkinter.CTkLabel(janela, text='CADASTRO POPULACIONAL', font=('Ariel', 28, 'bold'))
titulo.pack()

nome = customtkinter.CTkLabel(janela, text='Nome', font=('Ariel', 18, 'bold'))
nome.pack(pady=(40, 10))
entrada_nome = customtkinter.CTkEntry(janela, width=300, placeholder_text='Primeiro Nome')
entrada_nome.pack()
entrada_nome.bind("<Return>", lambda event: apertar_enter(event, entrada_data))

data = customtkinter.CTkLabel(janela, text='Data De Nascimento', font=('Ariel', 18, 'bold'))
data.pack(pady=(40, 10))
entrada_data = customtkinter.CTkEntry(janela, width=300, placeholder_text='YYYY-MM-DD')
entrada_data.pack()
entrada_data.bind("<Return>", lambda event: apertar_enter(event, entrada_cpf))

cp = customtkinter.CTkLabel(janela, text='CPF', font=('Ariel', 18, 'bold'))
cp.pack(pady=(40, 10))
entrada_cpf = customtkinter.CTkEntry(janela, width=300, placeholder_text='000.000.000-00')
entrada_cpf.pack()

# BOTÕES
button_add = customtkinter.CTkButton(janela, text='ADICIONAR',font=('Ariel', 14, 'bold'), command=precionar)
button_add.pack(pady=(60, 0))


# >>>>>>> OUTRA JANELA SECUNDARIA <<<<<<<<
def janela2():
    janela_secundaria = ctk.CTkToplevel(janela)
    janela_secundaria.geometry('400x400')
    titulo2 = customtkinter.CTkLabel(janela_secundaria, text='REMOVER', font=('Ariel', 24, 'bold'), text_color='Red')
    titulo2.pack()

    nome2 = customtkinter.CTkLabel(janela_secundaria, text='Nome', font=('Ariel', 18, 'bold'))
    nome2.pack(pady=(40, 10))
    entrada_nome2 = customtkinter.CTkEntry(janela_secundaria, width=200, placeholder_text='Primeiro Nome')
    entrada_nome2.pack()
    entrada_nome2.bind("<Return>", lambda event: apertar_enter(event, entrada_id2))

    id2 = customtkinter.CTkLabel(janela_secundaria, text='ID [Banco De Dados]', font=('Ariel', 18, 'bold'))
    id2.pack(pady=(40, 10))
    entrada_id2 = customtkinter.CTkEntry(janela_secundaria, width=200, placeholder_text='ID[Nùmero]')
    entrada_id2.pack()

    # >>>>>>>>>>>ADICIONAR COMANDOS<<<<<<<<<
    def precionar2():
        nome = entrada_nome2.get()
        id = entrada_id2.get()
        if nome and id:
            delete(nome, id)
            entrada_nome2.delete(0, 'end')
            entrada_id2.delete(0, 'end')
        else:
            print('PREENCHA AMBOS OS CAMPOS!!')

        # BOTÃO PARA REMOVER
    button_remov2 = customtkinter.CTkButton(janela_secundaria,text='REMOVER', font=('Ariel', 14, 'bold'), fg_color='Red', command=precionar2)
    button_remov2.pack(pady=40)


#BOTÃO REMOVER janela 1
button_remov = customtkinter.CTkButton(janela, text='REMOVER', font=('Ariel', 14, 'bold'), fg_color='Red', command=janela2)
button_remov.pack(pady=20)

#Janela >>>>> 3 <<<<<
def janela3():
    # função buscar
    def buscar():
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='vitor',
                database='Integrando_py'
            )

            curso = conexao.cursor()

            comando = 'SELECT id, nome, nascimento, cpf FROM cadastro'
            curso.execute(comando)
            resultado = curso.fetchall()

            # limpando caixa de texto
            caixa_texto.delete('1.0', 'end')
            #exibindo dados
            for id, nome, nascimento, cpf in resultado:
                caixa_texto.insert('end', f'ID: {id} | Nome: {nome} | Nascimento: {nascimento} | CPF: {cpf}\n')

            curso.fetchall()
            conexao.close()

        except mysql.connector.Error as erro:
            caixa_texto.insert('end', f'ERROR. Ao buscar dados: {erro}')


    janela_terc = ctk.CTkToplevel(janela)
    janela_terc.geometry('600x600')
    titulo3 = customtkinter.CTkLabel(janela_terc, text='BANCO DE DADOS', font=('Ariel', 24, 'bold'))
    titulo3.pack()

    caixa_texto = customtkinter.CTkTextbox(janela_terc, width=500)
    caixa_texto.pack(pady=20)

    #busca automatica
    def busca_da_aut():
        buscar()
        janela.after(500, busca_da_aut)

    busca_da_aut()

    def pesq(event=None):
        nome_entrada = entrada_pesquisar.get().strip()

        if not nome_entrada:
            caixa_texto2.delete('1.0', 'end')
            caixa_texto2.insert('end', 'Digite um nome para pesquisar.')
            return

        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='vitor',
                database='Integrando_py'
            )

            curso = conexao.cursor()

            comando = 'SELECT id, nome, nascimento, cpf FROM cadastro WHERE nome LIKE %s'
            parametro = (f"%{nome_entrada}%", )
            curso.execute(comando, parametro)
            dados = curso.fetchall()

            # limpando caixa de texto
            caixa_texto2.delete('1.0', 'end')
            # exibindo dados
            if dados:
                for id, nome, nascimento, cpf in dados:
                    caixa_texto2.insert('end', f'ID: {id} | Nome: {nome} | Nascimento: {nascimento} | CPF: {cpf}\n')

            else:
                caixa_texto2.insert('end', 'Nenhum resultado encontrado!')

            curso.fetchall()
            conexao.close()

        except mysql.connector.Error as erro:
            caixa_texto2.insert('end', f'ERROR. Ao buscar dados: {erro}')

    entrada_pesquisar = customtkinter.CTkEntry(janela_terc, width=300, placeholder_text='Primeiro Nome')
    entrada_pesquisar.pack(pady=(40, 10))

    #apertar enter
    entrada_pesquisar.bind("<Return>", pesq)

    button_pesquisar = customtkinter.CTkButton(janela_terc, text='Pesquisar', font=('Ariel', 14, 'bold'), command=pesq)
    button_pesquisar.pack()

    caixa_texto2 = customtkinter.CTkTextbox(janela_terc, width=500, height=100)
    caixa_texto2.pack(pady=(20, 10))


button_viz = customtkinter.CTkButton(janela, text='VIZUALIZAR', font=('Ariel', 14, 'bold'), command=janela3)
button_viz.pack()

#rodar janela
janela.mainloop()
