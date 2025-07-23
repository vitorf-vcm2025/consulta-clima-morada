📍 Ferramenta de Consulta de Clima e Morada
Uma aplicação de desktop simples e útil, construída com Python e CustomTkinter, que permite aos utilizadores obterem a morada completa e a previsão do tempo atual para qualquer localidade no Brasil a partir de um CEP.

Este projeto foi desenvolvido para demonstrar a capacidade de consumir e integrar múltiplas APIs de serviços web numa única interface gráfica.

🎬 Demons![demosntração](https://github.com/user-attachments/assets/4a07cccd-fb1e-40c4-b2e3-e7a566647e36)
tração


✨ Funcionalidades Principais
Interface Intuitiva: Uma janela limpa e fácil de usar, construída com CustomTkinter.

Consulta de CEP:

O utilizador insere um CEP de 8 dígitos.

A aplicação comunica com a API ViaCEP para obter os dados da morada (logradouro, bairro, cidade e UF).

Consulta de Clima:

Utilizando a cidade obtida a partir do CEP, a aplicação faz um segundo pedido à API OpenWeatherMap.

Exibe a temperatura atual (em graus Celsius) e a descrição do tempo (ex: "Céu limpo").

Validação e Feedback: A aplicação valida a entrada do CEP e fornece feedback claro ao utilizador em caso de erros (CEP inválido, chave de API incorreta, cidade não encontrada, etc.).

Ícone Personalizado: A aplicação tem um ícone personalizado para uma aparência mais profissional.

🛠️ Tecnologias Utilizadas
Linguagem: Python

Interface Gráfica (GUI): CustomTkinter

Comunicação com APIs (HTTP Requests): Biblioteca requests

APIs Externas:

ViaCEP para dados de morada.

OpenWeatherMap para dados de clima.

Manipulação de Ícones: Biblioteca Pillow (PIL)

🚀 Como Executar
Clone este repositório.

Instale as dependências necessárias:

pip install customtkinter requests Pillow

Importante: Obtenha uma chave de API gratuita no site da OpenWeatherMap.

No ficheiro app.py, substitua "SUA_CHAVE_DE_API_AQUI" pela sua chave.

Execute o script principal:

python app.py
