# Reconhecimento Facial - Projeto Panorama

Um sistema de reconhecimento facial desenvolvido em Python, utilizando técnicas modernas de visão computacional e aprendizado de máquina.

## 📋 Descrição

Este projeto implementa um sistema de reconhecimento facial que pode ser utilizado para identificar e verificar pessoas em imagens e vídeos. O sistema utiliza bibliotecas modernas de processamento de imagem e deep learning para garantir alta precisão no reconhecimento.

## 🚀 Funcionalidades

- Detecção facial em imagens e vídeos
- Reconhecimento e identificação de faces
- Interface web para visualização e gerenciamento
- Armazenamento de dados em banco de dados
- Sistema de treinamento para novos rostos

## 💻 Tecnologias Utilizadas

- Python (54.6%)
- HTML (45.4%)
- Bibliotecas principais:
  - OpenCV para processamento de imagem
  - dlib para detecção facial
  - Flask para interface web
  - MySQL para banco de dados

## 📁 Estrutura do Projeto
reconhecimento_facial-projeto-panorama/
├── **pycache**/
├── database/
├── lib/
├── templates/
├── db.py
├── detection.py
├── eigen.py
├── main.py
├── requirements.txt
├── training.py
└── views.py


## 🛠️ Instalação

1. Clone o repositório:
git clone https://github.com/betolara1/reconhecimento_facial-projeto-panorama.git


2. Instale as dependências:

pip install -r requirements.txt


3. Configure o banco de dados:
db.py


4. Execute o aplicativo:
python main.py


## 🔧 Configuração

1. Certifique-se de ter Python 3.7+ instalado
2. Configure as variáveis de ambiente necessárias
3. Prepare o conjunto de dados para treinamento
4. Execute o script de treinamento antes do primeiro uso


## 📚 Como Usar

1. Inicie o servidor web executando `main.py`
2. Acesse a interface web através do navegador
3. Faça o cadastro do usuario e captura seu rosto clicando em cadastrar
4. Abrir pagina de login, onde será realizado a verificação do rosto cadastrado
5. Clicar em 'gerar relatório' para gerar um relatório com o nome e a data em que foi feito o check-in 



## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ✒️ Autor

- **Roberto Lara** - [betolara1](https://github.com/betolara1)
