📘 ReStart 50+ — Plataforma de Educação Digital Inclusiva

O ReStart 50+ é uma plataforma criada para promover educação digital acessível, voltada especialmente para pessoas 50+ que desejam aprender novas tecnologias de forma simples, segura e acolhedora.
Desenvolvida em Python + Streamlit, ela reúne cursos introdutórios, avaliações curtas, acompanhamento de progresso e recursos assistivos para tornar o aprendizado mais inclusivo.

🚀 Funcionalidades Principais
🎓 Catálogo de Cursos

📖 Cursos práticos e de curta duração nas áreas:

⭐Inteligência Artificial
⭐Alfabetização em Dados
⭐Marketing Digital
⭐Internet das Coisas (IoT)
⭐Produtividade e Trabalho Remoto
⭐Empreendedorismo Sênior

📚 Cada curso possui:

- Descrição amigável
- Imagem ilustrativa
- Quiz simples para avaliação
- Registro automático do progresso

📝 Avaliações (Quiz)

- Questões de múltipla escolha
- Correção automática
- Registro de tentativas
-Cálculo de nota e histórico do aluno

📈 Dashboard do Aluno

- Progresso geral nos cursos
- Notas médias
- Histórico das últimas tentativas
- Percentual de conclusão da trilha formativa

📬 Contato com Instrutor

Envio de dúvidas diretamente pela plataforma, com:

- Registro de mensagens
- Histórico do aluno

🤖 Chatbot Integrado

Assistente simples para tirar dúvidas sobre:

- Funcionamento da plataforma
- Informações sobre cursos
- Localização de recursos

🧩 Acessibilidade Integrada

Pensado especialmente para o público 50+:

- Aumento e redução do tamanho da fonte
- Modo alto contraste
- Leitura automática (TTS — Text-to-Speech) via navegador
- Botões “🔊 Ouvir” em conteúdos chave
- Interface com cores e espaçamentos confortáveis

🛠️ Tecnologias Utilizadas

- Python 3.10+
- Streamlit (interface e navegação)
- JSON para persistência simples de dados
- HTML/CSS customizados para estilo e acessibilidade
- JavaScript (SpeechSynthesis API) para leitura automática de texto


▶️ Como Executar o Projeto

Clone o repositório

git clone https://github.com/SEU-USUARIO/restart50.git
cd restart50

Crie um ambiente virtual (recomendado)

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Instale as dependências

pip install streamlit

Execute o projeto

streamlit run ReStart50-Web-MVP.py


📦 Armazenamento de Dados

- A plataforma utiliza arquivos JSON locais para simplicidade:
- users.json: informações do usuário e progresso
- contacts.json: mensagens enviadas pelo formulário
- images/: possível armazenamento futuro de uploads
- O login é simples, baseado em nome e e-mail.


🤝 Desenvolvedores

Guilherme Aragão
Manoela Oliveira 
Matheus Silva 
Paula Carregal 
Pedro Santiago 

