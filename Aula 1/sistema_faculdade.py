"""
Sistema de Gestão de Alunos

"""

# Dicionário para armazenar os alunos (-chave: matrícula)
alunos = {}

# Contadores para cada curso
contadores = {
    "GES": 0,  # Engenharia de Software
    "GEC": 0,  # Engenharia de Computação
    "GET": 0,  # Engenharia de Telecomunicações
    "GEP": 0,  # Engenharia de Produção
    "ADS": 0,  # Análise e Desenvolvimento de Sistemas
    "SI": 0,   # Sistemas de Informação
}

# Mapeamento de códigos de curso para nomes completos
nomes_cursos = {
    "GES": "Engenharia de Software",
    "GEC": "Engenharia de Computação",
    "GET": "Engenharia de Telecomunicações",
    "GEP": "Engenharia de Produção",
    "ADS": "Análise e Desenvolvimento de Sistemas",
    "SI": "Sistemas de Informação",
}


def gerar_matricula(curso):
    """Gera uma matrícula automática baseada no curso."""
    contadores[curso] += 1
    return f"{curso}{contadores[curso]}"


def validar_curso(curso):
    """Valida se o curso existe."""
    return curso.upper() in contadores


def criar_aluno():
    """Cria um novo aluno (Create)."""
    print("\n" + "=" * 40)
    print("         CADASTRAR NOVO ALUNO")
    print("=" * 40)
    
    # Solicita o nome
    nome = input("Nome do aluno: ").strip()
    while not nome:
        print("Erro: O nome não pode estar vazio.")
        nome = input("Nome do aluno: ").strip()
    
    # Solicita o curso
    print("\nCursos disponíveis:")
    for codigo, nome_curso in nomes_cursos.items():
        print(f"  {codigo} - {nome_curso}")
    
    curso = input("Código do curso: ").strip().upper()
    while not validar_curso(curso):
        print("Erro: Curso inválido. Escolha um dos códigos listados.")
        print("\nCursos disponíveis:")
        for codigo, nome_curso in nomes_cursos.items():
            print(f"  {codigo} - {nome_curso}")
        curso = input("Código do curso: ").strip().upper()
    
    # Gera a matrícula automaticamente
    matricula = gerar_matricula(curso)
    
    # Cria o aluno
    alunos[matricula] = {
        "nome": nome,
        "curso": curso,
        "nome_curso": nomes_cursos[curso]
    }
    
    print(f"\n✓ Aluno cadastrado com sucesso!")
    print(f"  Matrícula: {matricula}")
    print(f"  Nome: {nome}")
    print(f"  Curso: {nomes_cursos[curso]}")


def listar_alunos():
    """Lista todos os alunos (Read)."""
    print("\n" + "=" * 40)
    print("         LISTA DE ALUNOS CADASTRADOS")
    print("=" * 40)
    
    if not alunos:
        print("\nNenhum aluno cadastrado.")
        return
    
    print(f"\n{'Matrícula':<12} {'Nome':<35} {'Curso':<30}")
    print("-" * 77)
    
    for matricula, dados in sorted(alunos.items()):
        nome = dados["nome"][:33] + "..." if len(dados["nome"]) > 35 else dados["nome"]
        curso = f"{dados['curso']} - {nomes_cursos[dados['curso']]}"[:28] + "..." if len(f"{dados['curso']} - {nomes_cursos[dados['curso']]}") > 30 else f"{dados['curso']} - {nomes_cursos[dados['curso']]}"
        print(f"{matricula:<12} {nome:<35} {curso:<30}")
    
    print(f"\nTotal de alunos: {len(alunos)}")


def buscar_aluno():
    """Busca um aluno específico (Read)."""
    print("\n" + "=" * 40)
    print("           BUSCAR ALUNO")
    print("=" * 40)
    
    if not alunos:
        print("\nNenhum aluno cadastrado.")
        return
    
    print("\n1. Buscar por matrícula")
    print("2. Buscar por nome")
    print("3. Buscar por curso")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "1":
        matricula = input("Digite a matrícula: ").strip().upper()
        if matricula in alunos:
            exibir_aluno(alunos[matricula], matricula)
        else:
            print(f"\nErro: Aluno com matrícula {matricula} não encontrado.")
    
    elif opcao == "2":
        nome_busca = input("Digite o nome (ou parte do nome): ").strip().lower()
        resultados = [(m, a) for m, a in alunos.items() if nome_busca in a["nome"].lower()]
        if resultados:
            print(f"\n{len(resultados)} aluno(s) encontrado(s):")
            for matricula, dados in resultados:
                exibir_aluno(dados, matricula)
        else:
            print("\nNenhum aluno encontrado com esse nome.")
    
    elif opcao == "3":
        print("\nCursos disponíveis:")
        for codigo, nome_curso in nomes_cursos.items():
            print(f"  {codigo} - {nome_curso}")
        curso_busca = input("Digite o código do curso: ").strip().upper()
        if curso_busca in contadores:
            resultados = [(m, a) for m, a in alunos.items() if a["curso"] == curso_busca]
            if resultados:
                print(f"\n{len(resultados)} aluno(s) do curso {nomes_cursos[curso_busca]}:")
                for matricula, dados in resultados:
                    exibir_aluno(dados, matricula)
            else:
                print(f"\nNenhum aluno encontrado no curso {nomes_cursos[curso_busca]}.")
        else:
            print("\nErro: Curso inválido.")
    
    else:
        print("\nErro: Opção inválida.")


def exibir_aluno(dados, matricula):
    """Exibe os dados de um aluno."""
    print(f"\n--- Aluno {matricula} ---")
    print(f"  Nome: {dados['nome']}")
    print(f"  Curso: {dados['curso']} - {dados['nome_curso']}")


def atualizar_aluno():
    """Atualiza os dados de um aluno (Update)."""
    print("\n" + "=" * 40)
    print("         ATUALIZAR ALUNO")
    print("=" * 40)
    
    if not alunos:
        print("\nNenhum aluno cadastrado.")
        return
    
    matricula = input("Digite a matrícula do aluno: ").strip().upper()
    
    if matricula not in alunos:
        print(f"\nErro: Aluno com matrícula {matricula} não encontrado.")
        return
    
    aluno = alunos[matricula]
    print(f"\nAluno atual:")
    exibir_aluno(aluno, matricula)
    
    print("\nO que deseja alterar?")
    print("1. Nome")
    print("2. Curso")
    print("3. Cancelar")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "1":
        novo_nome = input("Novo nome: ").strip()
        while not novo_nome:
            print("Erro: O nome não pode estar vazio.")
            novo_nome = input("Novo nome: ").strip()
        aluno["nome"] = novo_nome
        print("\n✓ Nome atualizado com sucesso!")
    
    elif opcao == "2":
        print("\nCursos disponíveis:")
        for codigo, nome_curso in nomes_cursos.items():
            print(f"  {codigo} - {nome_curso}")
        
        novo_curso = input("Novo código do curso: ").strip().upper()
        while not validar_curso(novo_curso):
            print("Erro: Curso inválido. Escolha um dos códigos listados.")
            novo_curso = input("Novo código do curso: ").strip().upper()
        
        # Atualiza o curso e gera nova matrícula
        # Remove a matrícula antiga e cria uma nova
        del alunos[matricula]
        
        nova_matricula = gerar_matricula(novo_curso)
        aluno["curso"] = novo_curso
        aluno["nome_curso"] = nomes_cursos[novo_curso]
        alunos[nova_matricula] = aluno
        
        print(f"\n✓ Curso atualizado com sucesso!")
        print(f"  Nova matrícula: {nova_matricula}")
    
    elif opcao == "3":
        print("\nOperação cancelada.")
        return
    
    else:
        print("\nErro: Opção inválida.")
        return


def excluir_aluno():
    """Exclui um aluno (Delete)."""
    print("\n" + "=" * 40)
    print("           EXCLUIR ALUNO")
    print("=" * 40)
    
    if not alunos:
        print("\nNenhum aluno cadastrado.")
        return
    
    matricula = input("Digite a matrícula do aluno: ").strip().upper()
    
    if matricula not in alunos:
        print(f"\nErro: Aluno com matrícula {matricula} não encontrado.")
        return
    
    aluno = alunos[matricula]
    print(f"\nAluno a ser excluído:")
    exibir_aluno(aluno, matricula)
    
    confirmacao = input("\nTem certeza que deseja excluir? (S/N): ").strip().upper()
    
    if confirmacao == "S":
        del alunos[matricula]
        print("\n✓ Aluno excluído com sucesso!")
    else:
        print("\nOperação cancelada.")


def mostrar_menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 50)
    print("      SISTEMA DE GESTÃO DE ALUNOS - FACULDADE")
    print("=" * 50)
    print("\n1. Cadastrar novo aluno")
    print("2. Listar todos os alunos")
    print("3. Buscar aluno")
    print("4. Atualizar dados do aluno")
    print("5. Excluir aluno")
    print("6. Sair do sistema")
    print("\n" + "-" * 50)


def main():
    """Função principal do sistema."""
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            criar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            buscar_aluno()
        elif opcao == "4":
            atualizar_aluno()
        elif opcao == "5":
            excluir_aluno()
        elif opcao == "6":
            print("\n" + "=" * 40)
            print("   Obrigado por usar o sistema!")
            print("            Até logo!")
            print("=" * 40 + "\n")
            break
        else:
            print("\nErro: Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()