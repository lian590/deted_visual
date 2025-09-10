# Sistema de Gestão de Funcionários

Este é um sistema web Flask para gestão de funcionários com funcionalidades de cadastro, login e administração.

## Estrutura do Projeto

```
├── app/
│   ├── __init__.py          # Inicialização da aplicação Flask
│   ├── app.py               # Ponto de entrada da aplicação
│   ├── routes/
│   │   ├── auth_routes.py   # Rotas de autenticação (login, cadastro)
│   │   └── adm.py           # Rotas de administração
│   ├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/           # Templates HTML
│   ├── scripts/             # Scripts utilitários
│   ├── models/              # Modelos de dados
│   └── services/            # Serviços da aplicação
├── tests/                   # Testes automatizados
├── .github/
│   └── workflows/           # Configurações CI/CD
├── config.py                # Configurações da aplicação
├── requirements.txt         # Dependências Python
└── README.md
```

## Funcionalidades

- **Cadastro de Funcionários**: Permite cadastrar novos funcionários com foto
- **Login**: Sistema de autenticação seguro
- **Administração**: Interface para gerenciar professores/funcionários
- **Reconhecimento Facial**: Scripts para reconhecimento facial (em desenvolvimento)

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd deted_visual-front-e-back
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados MySQL:
   - Crie um banco de dados chamado `hell_gate`
   - Execute os scripts SQL para criar as tabelas necessárias

5. Execute a aplicação:
```bash
python -m app.app
```

A aplicação estará disponível em `http://localhost:5000`

## Testes

Para executar os testes:
```bash
pytest tests/
```

## CI/CD

O projeto utiliza GitHub Actions para CI/CD. Os testes são executados automaticamente em cada push e pull request.

## Scripts Utilitários

- `app/scripts/face_recognition.py`: Script para reconhecimento facial
- `app/scripts/database_cleanup.py`: Script para limpeza do banco de dados

## Tecnologias Utilizadas

- **Flask**: Framework web Python
- **MySQL**: Banco de dados
- **OpenCV**: Processamento de imagens
- **Bootstrap**: Framework CSS para interface
- **pytest**: Framework de testes

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.
