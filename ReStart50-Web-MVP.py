# O projeto ReStart 50+ surge como uma proposta de educação digital inclusiva e acessível
import streamlit as st
import os
import json
import uuid
import time
from datetime import datetime
from random import choice
import html as html_lib

# ------------------- Configuração -------------------
st.set_page_config(
    page_title="ReStart 50+",
    layout="wide",
    page_icon="🎓"
)

# ------------------- Auxiliares -------------------
def safe_rerun():
    """Try modern rerun, fallback to experimental if needed."""
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ------------------- Diretórios / Dados -------------------
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")
IMAGES_DIR = os.path.join(DATA_DIR, "images")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

USERS_DB = load_json(USERS_FILE)
CONTACTS_DB = load_json(CONTACTS_FILE)

# ------------------- Acessibilidade -------------------
st.session_state.setdefault("font_size", 18)
st.session_state.setdefault("high_contrast", False)
st.session_state.setdefault("auto_read_chat", False)
st.session_state.setdefault("voice_pref", "female")
st.session_state.setdefault("user", None)
st.session_state.setdefault("chat_history", [])

# ------------------- Sidebar -------------------
st.sidebar.markdown("<div style='padding:8px;'><b>Acessibilidade</b></div>", unsafe_allow_html=True)
col_a, col_b = st.sidebar.columns([1,1])
if col_a.button("🅰️ Aumentar Fonte"):
    st.session_state.font_size = min(28, st.session_state.font_size + 2)
    safe_rerun()
if col_b.button("🔤 Diminuir Fonte"):
    st.session_state.font_size = max(12, st.session_state.font_size - 2)
    safe_rerun()

col_c, col_d = st.sidebar.columns([1,1])
if col_c.button("🔄 Reset Fonte"):
    st.session_state.font_size = 18
    safe_rerun()
if col_d.button("🎨 Alto Contraste"):
    st.session_state.high_contrast = not st.session_state.high_contrast
    safe_rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🔊 Ativar/Desativar leitura automática do chat"):
    st.session_state.auto_read_chat = not st.session_state.auto_read_chat
    safe_rerun()

# Vozes de preferencia
vp = st.sidebar.selectbox("Voz preferida (navegador):", options=["Mulher", "Homem", "Padrão"], index=0)
st.session_state.voice_pref = vp

st.sidebar.markdown("---")

# ------------------- CSS -------------------
if st.session_state.high_contrast:
    ROOT_VARS = {
        "--bg": "#000000",
        "--card": "#111111",
        "--accent": "#FFD166",
        "--muted": "#FFFFFF"
    }
else:
    ROOT_VARS = {
        "--bg": "#f7fbfd",
        "--card": "#ffffff",
        "--accent": "#4EC0F0",
        "--muted": "#1b5899"
    }

css_template = f"""
<style>
    :root {{
        --bg: {ROOT_VARS['--bg']};
        --card: {ROOT_VARS['--card']};
        --accent: {ROOT_VARS['--accent']};
        --muted: {ROOT_VARS['--muted']};
        --radius: 12px;
        --font-size: {st.session_state.font_size}px;
    }}
    html, body, [data-testid='stAppViewContainer'] {{
        background: var(--bg);
        color: var(--muted);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        font-size: var(--font-size);
    }}
    .main-title {{ font-size: calc(var(--font-size) * 1.8); font-weight:700; color:var(--accent); margin-bottom:6px; }}
    .subtitle {{ font-size: calc(var(--font-size) * 1.0); color:var(--accent); margin-bottom:10px; }}
    .card {{
        background: var(--card);
        padding: 18px;
        border-radius: var(--radius);
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        margin-bottom: 14px;
        color: var(--muted);
    }}
    .course-title {{ font-size: calc(var(--font-size) * 1.1); font-weight:700; color:var(--accent); }}
    .muted {{ color:var(--muted); font-size: calc(var(--font-size) * 0.95); }}
    .stButton>button {{
        background-color: var(--accent);
        color: #000000;
        border-radius: 10px;
        padding: 8px 12px;
        font-size: calc(var(--font-size) * 0.95);
        border: none;
    }}
    .stButton>button:hover {{ filter: brightness(0.95); }}
    .big-input input, .big-input textarea {{
        font-size: calc(var(--font-size) * 1.05) !important;
        color: var(--muted) !important;
    }}
    .chat-bubble {{
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        display: block;
        max-width: 90%;
    }}
    .user {{
        background: var(--accent);
        color: #000000;
        text-align: right;
        margin-left: auto;
    }}
    .bot {{
        background: #E0F7FA;
        color: #000;
        text-align: left;
    }}
    div[role="radiogroup"] label p,
    div[data-testid="stMarkdownContainer"] p,
    .stRadio > label,
    .stTextInput > label,
    .stSelectbox > label,
    .stNumberInput > label {{
        color: var(--muted) !important;
        font-weight: 600;
        font-size: calc(var(--font-size) * 1.0);
    }}
    .stRadio > div {{
        background-color: var(--card);
        border-radius: 10px;
        padding: 6px 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .listen-btn {{
        display:inline-block;
        margin-left:8px;
        padding:6px 10px;
        border-radius:8px;
        background: var(--accent);
        color: #000;
        font-weight:600;
        text-decoration:none;
    }}
    .footer {{ font-size: calc(var(--font-size) * 0.85); color: var(--muted); text-align:center; margin-top:20px; }}
</style>
"""
st.markdown(css_template, unsafe_allow_html=True)

# ------------------- JS  -------------------
speech_js = """
<script>
window.ReStart50_speech = window.ReStart50_speech || (function(){
    let voices = [];
    function loadVoices(){ voices = window.speechSynthesis.getVoices(); }
    loadVoices();
    if (typeof speechSynthesis !== 'undefined'){
        window.speechSynthesis.onvoiceschanged = loadVoices;
    }
    function pickVoice(pref){
        if (!voices || voices.length === 0) return null;
        pref = (pref||'female').toLowerCase();
        if (pref === 'female'){
            for (let v of voices){
                let n = v.name.toLowerCase();
                if (n.includes('female') || n.includes('woman') || n.includes('zira') || n.includes('sara') || n.includes('victoria') || n.includes('maria')) return v;
            }
            for (let v of voices){ if (v.lang && v.lang.toLowerCase().startsWith('pt')) return v; }
        }
        return voices[0] || null;
    }
    function speak(text, pref){
        if (!text) return;
        const utter = new SpeechSynthesisUtterance(text);
        const v = pickVoice(pref);
        if (v) utter.voice = v;
        utter.lang = 'pt-BR';
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utter);
    }
    return { speak: speak };
})();
</script>
"""
st.components.v1.html(speech_js, height=0)

def render_listen_button(text, key_suffix):
    """Render a safe 'Ouvir' link using json escapes for JS-safe strings."""
    if not text:
        return
    # escape for HTML then produce a JS-safe string via json.dumps
    safe_html = html_lib.escape(text).replace("\n", " ")
    safe_js_string = json.dumps(safe_html)  # includes surrounding double quotes and escapes
    voice_js = json.dumps(st.session_state.get("voice_pref", "female"))
    # build html: note safe_js_string already has quotes
    html = f'<a class="listen-btn" href="javascript:void(0)" onclick="window.ReStart50_speech.speak({safe_js_string}, {voice_js})">🔊 Ouvir</a>'
    # render component without passing key (newer streamlit forbids key)
    st.components.v1.html(html, height=38)

# ------------------- Dados dos Cursos -------------------
COURSES = [
    {
        "id": "c_ai_basics",
        "title": "IA Essencial para Iniciantes",
        "category": "IA",
        "level": "Iniciante",
        "hours": 6,
        "description": "Conceitos práticos de IA, exemplos do dia a dia e como usar assistentes de forma segura.",
        "image": "https://images.unsplash.com/photo-1737644467636-6b0053476bb2?q=80&w=1972&auto=format&fit=crop",
        "quiz": [
            {"q": "O que significa IA?", "choices": ["Internet Avançada","Inteligência Artificial","Informação Automatizada"], "answer": 1},
            {"q": "Assistentes de IA ajudam em:", "choices": ["Enviar e-mails","Cozinhar sem instruções","Voar"], "answer": 0},
            {"q": "Uma prática segura é:", "choices": ["Compartilhar senhas","Usar senhas fortes","Ignorar atualizações"], "answer": 1}
        ]
    },
    {
        "id": "c_data_literacy",
        "title": "Alfabetização de Dados",
        "category": "Dados",
        "level": "Iniciante",
        "hours": 8,
        "description": "Aprenda a interpretar números, gráficos e tomar decisões com base em dados simples.",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1115&auto=format&fit=crop",
        "quiz": [
            {"q": "Um gráfico de barras mostra:", "choices": ["Comparação entre categorias","Mudança ao longo do tempo","Mapa"], "answer": 0},
            {"q": "Média aritmética é uma forma de:", "choices": ["Função estética","Medida de tendência central","Tipo de gráfico"], "answer": 1}
        ]
    },
    {
        "id": "c_digital_marketing",
        "title": "Marketing Digital Prático",
        "category": "Marketing",
        "level": "Intermediário",
        "hours": 10,
        "description": "Ferramentas básicas para divulgação online: redes sociais, conteúdo e relações com clientes.",
        "image": "https://media.istockphoto.com/id/1207549263/pt/foto/it-developer-paperwork-on-board.jpg?s=1024x1024&w=is&k=20&c=zVmaraZVU3Uzsr3JX_fcAtv1AjaPE76YG2x5bh501lQ=",
        "quiz": [
            {"q": "O que é SEO?", "choices": ["Otimização para mecanismos de busca","Rede social nova","Software de edição"], "answer": 0},
            {"q": "Postagens constantes ajudam:", "choices": ["Engajamento","Ignorar público","Diminuir alcance"], "answer": 0}
        ]
    },
    {
        "id": "c_iot_home",
        "title": "IoT para o Lar e Saúde",
        "category": "IoT",
        "level": "Iniciante",
        "hours": 5,
        "description": "Como usar dispositivos conectados com segurança para conforto e monitoramento de saúde.",
        "image": "https://plus.unsplash.com/premium_photo-1688678097473-2ce11d23e30c?q=80&w=970&auto=format&fit=crop",
        "quiz": [
            {"q": "IoT refere-se a:", "choices": ["Internet das Coisas","Interface on Time","Intelligent online Tools"], "answer": 0},
            {"q": "Dispositivo IoT precisa:", "choices": ["Estar conectado","Ser caro","Ter impressora"], "answer": 0}
        ]
    },
    {
        "id": "c_remotework",
        "title": "Trabalho Remoto e Ferramentas",
        "category": "Produtividade",
        "level": "Iniciante",
        "hours": 6,
        "description": "Boas práticas para trabalhar online, segurança, comunicação e gestão do tempo.",
        "image": "https://media.istockphoto.com/id/1395293365/pt/foto/computer-laptop-with-white-screen-coffee-cup-and-supplies-on-wooden-table.jpg?s=1024x1024&w=is&k=20&c=19rmGF13cHeI1QPNHTklKUW6udP9IeXeE0AlUxv-91A=",
        "quiz": [
            {"q": "Uma boa prática em home office é:", "choices": ["Ignorar horários","Ter rotina","Nunca pausar"], "answer": 1},
            {"q": "Ferramentas para reunião online incluem:", "choices": ["Editor de imagens","Plataformas de videoconferência","Televisão"], "answer": 1}
        ]
    },
    {
        "id": "c_senior_entrepreneur",
        "title": "Empreendedorismo Sênior",
        "category": "Empreendedorismo",
        "level": "Intermediário",
        "hours": 8,
        "description": "Como transformar ideias em pequenos negócios e projetos com baixo investimento inicial.",
        "image": "https://plus.unsplash.com/premium_photo-1661281203773-833d30e370ee?q=80&w=1170&auto=format&fit=crop",
        "quiz": [
            {"q": "Plano de negócios ajuda a:", "choices": ["Organizar ideias","Esconder falhas","Substituir produto"], "answer": 0},
        ]
    }
]

def get_course(course_id):
    for c in COURSES:
        if c["id"] == course_id:
            return c
    return None

# ------------------- Login -------------------
def create_user(name, email):
    user_id = str(uuid.uuid4())
    USERS_DB[user_id] = {
        "id": user_id,
        "name": name,
        "email": email,
        "joined": datetime.utcnow().isoformat(),
        "progress": {},
    }
    save_json(USERS_FILE, USERS_DB)
    return USERS_DB[user_id]

def find_user_by_email(email):
    for uid, u in USERS_DB.items():
        if u.get("email") and u["email"].lower() == email.lower():
            return u
    return None

# ------------------- Login e Informações  -------------------
st.sidebar.markdown("<div class='card'><h3>ReStart 50+</h3><p class='muted'>Você traz a sabedoria da vida. Nós trazemos o futuro.</p></div>", unsafe_allow_html=True)

if st.session_state.user:
    st.sidebar.markdown(f"**Logado como:** {st.session_state.user.get('name')}  \n{st.session_state.user.get('email')}", unsafe_allow_html=True)
    if st.sidebar.button("Sair"):
        st.session_state.user = None
        st.success("Desconectado com sucesso.")
else:
    st.sidebar.markdown("### 🔐 Entrar / Criar conta")
    with st.sidebar.form("login_form", clear_on_submit=False):
        name_input = st.text_input("Nome", value="", placeholder="Seu nome completo")
        email_input = st.text_input("E-mail", value="", placeholder="seu@exemplo.com")
        submitted = st.form_submit_button("Entrar / Criar conta")
        if submitted:
            if not email_input.strip():
                st.sidebar.error("Por favor, preencha o e-mail.")
            else:
                user = find_user_by_email(email_input.strip())
                if user:
                    st.session_state.user = user
                    st.sidebar.success(f"Bem-vindo(a) de volta, {user.get('name')}!")
                else:
                    u = create_user(name_input.strip() or "Visitante", email_input.strip())
                    st.session_state.user = u
                    st.sidebar.success(f"Conta criada. Olá, {u.get('name')}!")

st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação rápida")
st.sidebar.write("- Use o menu principal para mover-se entre telas.")
st.sidebar.markdown("---")

# ------------------- Cabeçalho -------------------
st.markdown("<div class='main-title'>🎓 ReStart 50+</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Cursos acessíveis e práticos — aprenda no seu ritmo.</div>", unsafe_allow_html=True)

# ------------------- Páginas  -------------------
page = st.sidebar.radio("📚 Menu", ["Início", "Cursos", "Avaliações", "Meu Progresso", "Contato com Instrutor", "Chatbot"])

# ---------- Início----------
if page == "Início":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Bem-vindo(a) à ReStart 50+")
    intro_text = ("Plataforma pensada para facilitar o aprendizado, com conteúdos práticos, curtos e claros. "
                  "Destaques: cursos sobre IA, Dados, IoT, Marketing Digital e Empreendedorismo; avaliações curtas; "
                  "contato com instrutores.")
    st.write(intro_text)
    render_listen_button(intro_text, "intro")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Cursos ----------
elif page == "Cursos":
    st.header("🎓 Cursos — Profissões do Futuro")
    cols = st.columns(2)
    for i, course in enumerate(COURSES):
        with cols[i % 2]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            img_html = f'<img src="{course["image"]}" alt="Capa do curso {html_lib.escape(course["title"])}" style="width:100%;border-radius:8px;"/>'
            st.components.v1.html(img_html, height=220)
            st.markdown(f"<div class='course-title'>{course['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted'>{course['level']} • {course['hours']}h</div>", unsafe_allow_html=True)
            st.write(course["description"])
            render_listen_button(course["description"], f"course_desc_{course['id']}")
            enroll_col1, enroll_col2 = st.columns([1,1])
            if st.session_state.user:
                if enroll_col1.button("Iniciar curso", key=f"start_{course['id']}"):
                    uid = st.session_state.user["id"]
                    USERS_DB.setdefault(uid, st.session_state.user)
                    USERS_DB[uid].setdefault("progress", {})
                    USERS_DB[uid]["progress"].setdefault(course["id"], {"completed": False, "score": None, "attempts": []})
                    save_json(USERS_FILE, USERS_DB)
                    st.success(f"Curso '{course['title']}' iniciado. Vá para 'Avaliações' para fazer o quiz quando finalizar o estudo.")
            else:
                enroll_col1.info("Faça login para iniciar")

            if enroll_col2.button("Fazer avaliação (quiz)", key=f"quiz_{course['id']}"):
                st.session_state["quiz_course"] = course["id"]
                safe_rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ---------- Avaliações ----------
elif page == "Avaliações":
    st.header("📝 Avaliações por Curso")
    selected = st.selectbox("Escolha um curso para avaliar", options=[(c["id"], c["title"]) for c in COURSES], format_func=lambda t: t[1])
    course = get_course(selected[0])
    if not course:
        st.info("Selecione um curso.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### {course['title']}")
        st.write(course["description"])
        render_listen_button(course["description"], f"quiz_course_desc_{course['id']}")
        st.write("Responda ao pequeno questionário (rápido). As notas serão salvas no seu perfil e exibidas no Dashboard.")

        if not st.session_state.user:
            st.info("Faça login para responder a avaliação e salvar sua nota.")
        else:
            answers = []
            with st.form(f"quiz_form_{course['id']}"):
                for idx, q in enumerate(course.get("quiz", [])):
                    question_text = f"**{idx+1}. {q['q']}**"
                    st.markdown(question_text)
                    render_listen_button(q['q'], f"quiz_q_{course['id']}_{idx}")
                    choice_idx = st.radio("", options=list(range(len(q["choices"]))),
                                          format_func=lambda x, q=q: q["choices"][x],
                                          key=f"q_{course['id']}_{idx}")
                    answers.append(choice_idx)
                submitted = st.form_submit_button("Enviar respostas")
                if submitted:
                    score = 0
                    total = len(course.get("quiz", []))
                    for idx, q in enumerate(course.get("quiz", [])):
                        if answers[idx] == q["answer"]:
                            score += 1
                    percent = int((score / total) * 100) if total else 0
                    uid = st.session_state.user["id"]
                    USERS_DB.setdefault(uid, st.session_state.user)
                    USERS_DB[uid].setdefault("progress", {})
                    USERS_DB[uid]["progress"].setdefault(course["id"], {"completed": False, "score": None, "attempts": []})
                    attempt = {"ts": datetime.utcnow().isoformat(), "score": percent, "raw": score}
                    USERS_DB[uid]["progress"][course["id"]]["attempts"].append(attempt)
                    USERS_DB[uid]["progress"][course["id"]]["score"] = percent
                    USERS_DB[uid]["progress"][course["id"]]["completed"] = True
                    save_json(USERS_FILE, USERS_DB)
                    msg = f"Avaliação enviada! Você obteve {score}/{total} ({percent}%). A nota foi salva no seu perfil."
                    st.success(msg)
                    render_listen_button(msg, f"quiz_result_{course['id']}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Meu Progresso ----------
elif page == "Meu Progresso":
    st.header("📈 Meu Progresso e Notas")
    if not st.session_state.user:
        st.info("Faça login para ver seu progresso.")
    else:
        uid = st.session_state.user["id"]
        user = USERS_DB.get(uid, st.session_state.user)
        progress = user.get("progress", {})
        total_courses = len(COURSES)
        completed_count = sum(1 for c in COURSES if progress.get(c["id"], {}).get("completed"))
        percent_completion = int((completed_count / total_courses) * 100) if total_courses else 0
        scores = [progress[c["id"]]["score"] for c in COURSES if progress.get(c["id"]) and progress[c["id"]].get("score") is not None]
        avg_score = int(sum(scores) / len(scores)) if scores else None

        st.markdown('<div class="card">', unsafe_allow_html=True)
        summary_text = f"Olá, {user.get('name')} — você concluiu {completed_count} de {total_courses} cursos. Progresso: {percent_completion}%."
        st.subheader(summary_text)
        render_listen_button(summary_text, "progress_summary")
        st.progress(percent_completion)
        if avg_score is not None:
            st.write(f"• Nota média: **{avg_score}%**")
        else:
            st.write("• Nota média: — (nenhuma avaliação concluída ainda)")

        st.markdown("### Detalhamento por curso")
        for c in COURSES:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{c['title']}** — {c['level']} • {c['hours']}h")
            p = progress.get(c["id"], {})
            status = "✅ Concluído" if p.get("completed") else "⏳ Pendente"
            score_text = f"{p.get('score')}%" if p.get("score") is not None else "—"
            st.write(f"Status: **{status}** | Nota: **{score_text}**")
            attempts = p.get("attempts", [])
            if attempts:
                st.write("Tentativas:")
                for a in attempts[-3:][::-1]:
                    ts = a.get("ts", "")
                    scr = a.get("score", "")
                    st.write(f"- {ts.split('T')[0]} — {scr}%")
            else:
                st.write("Nenhuma tentativa registrada.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Contato ----------
elif page == "Contato com Instrutor":
    st.header("📬 Contato com Instrutor")
    st.write("Envie sua dúvida ao instrutor.")
    with st.form("contact_form"):
        name = st.text_input("Seu nome", value=(st.session_state.user.get("name") if st.session_state.user else ""))
        email = st.text_input("Seu e-mail", value=(st.session_state.user.get("email") if st.session_state.user else ""))
        course_choice = st.selectbox("Sobre qual curso?", options=["Geral"] + [c["title"] for c in COURSES])
        message = st.text_area("Sua dúvida / mensagem", height=140)
        send = st.form_submit_button("Enviar mensagem")
        if send:
            if not message.strip():
                st.warning("Escreva sua dúvida antes de enviar.")
            else:
                msg_id = str(uuid.uuid4())
                CONTACTS_DB[msg_id] = {
                    "id": msg_id,
                    "name": name or "Anônimo",
                    "email": email or "",
                    "course": course_choice,
                    "message": message,
                    "ts": datetime.utcnow().isoformat(),
                    "status": "novo"
                }
                save_json(CONTACTS_FILE, CONTACTS_DB)
                conf = "Mensagem enviada! O instrutor será notificado (simulação)."
                st.success(conf)
                render_listen_button(conf, f"contact_sent_{msg_id}")

    if st.session_state.user:
        st.markdown("### Suas mensagens recentes")
        user_email = st.session_state.user.get("email")
        user_messages = [m for m in CONTACTS_DB.values() if m.get("email") == user_email]
        if user_messages:
            for m in sorted(user_messages, key=lambda x: x["ts"], reverse=True)[:5]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(f"**Curso:** {m.get('course')} — {m.get('ts').split('T')[0]}")
                st.write(m.get("message"))
                st.write(f"Status: {m.get('status')}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Nenhuma mensagem enviada por você.")

# ---------- CHATBOT ----------
elif page == "Chatbot":
    st.header("🤖 Assistente ReStart")
    st.write("Pergunte algo sobre cursos, avaliações ou como usar a plataforma")
    user_msg = st.text_input("Digite sua dúvida aqui", key="chat_input_big")
    if st.button("Enviar pergunta"):
        if user_msg and user_msg.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_msg, "ts": datetime.utcnow().isoformat()})
            txt = user_msg.lower()
            if any(k in txt for k in ["ia", "inteligência", "inteligencia"]):
                reply = "IA = Inteligência Artificial. Exemplos práticos: assistentes de escrita, classificadores simples. Veja o curso 'IA Essencial para Iniciantes'."
            elif any(k in txt for k in ["iot", "internet das coisas", "coisas"]):
                reply = "IoT = dispositivos conectados. No curso 'IoT para o Lar e Saúde' mostramos exemplos práticos."
            elif any(k in txt for k in ["quiz", "avaliação", "nota"]):
                reply = "As avaliações ficam em 'Avaliações'. Ao enviar as respostas, a nota será salva em seu perfil e aparecerá em 'Meu Progresso'."
            elif any(k in txt for k in ["contato", "instrutor", "duvida"]):
                reply = "Use a página 'Contato com Instrutor' para enviar uma mensagem diretamente ao instrutor."
            else:
                found = []
                for c in COURSES:
                    if any(w in txt for w in c["title"].lower().split()) or any(w in txt for w in c["description"].lower().split()):
                        found.append(c["title"])
                if found:
                    reply = f"Encontrei cursos relacionados: {', '.join(found[:3])}. Deseja que eu direcione você até 'Cursos'?"
                else:
                    reply = choice([
                        "Boa pergunta — tente perguntar 'O que é IA?' ou 'Como vejo minhas notas?'.",
                        "Posso sugerir um curso se você disser uma palavra-chave (ex.: 'dados', 'IoT', 'marketing')."
                    ])
            st.session_state.chat_history.append({"role": "bot", "text": reply, "ts": datetime.utcnow().isoformat()})
            if st.session_state.auto_read_chat:
                # safe-quote reply for JS
                safe_reply_js = json.dumps(html_lib.escape(reply).replace("\n", " "))
                voice_js = json.dumps(st.session_state.voice_pref)
                js = f"<script>window.ReStart50_speech.speak({safe_reply_js}, {voice_js});</script>"
                st.components.v1.html(js, height=0)

    for msg in st.session_state.chat_history[-30:]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-bubble user'><b>Você:</b> {html_lib.escape(msg['text'])}</div>", unsafe_allow_html=True)
            render_listen_button(msg['text'], f"chat_user_{abs(hash(msg['text'])) % 100000}")
        else:
            st.markdown(f"<div class='chat-bubble bot'><b>Assistente:</b> {html_lib.escape(msg['text'])}</div>", unsafe_allow_html=True)
            render_listen_button(msg['text'], f"chat_bot_{abs(hash(msg['text'])) % 100000}")

    if st.button("Limpar conversa"):
        st.session_state.chat_history = []
        st.success("Conversa limpa.")

# ------------------- Rodapé -------------------
st.sidebar.markdown("---")
if st.session_state.user:
    uid = st.session_state.user["id"]
    user_data = USERS_DB.get(uid, st.session_state.user)
    if st.sidebar.button("Exportar meu progresso (JSON)"):
        st.sidebar.download_button("Baixar JSON", data=json.dumps(user_data, ensure_ascii=False, indent=2), file_name=f"restart50_{uid}.json")

#st.sidebar.markdown("O futuro pertence a quem nunca para de aprender.")
# Salvar banco de dados
save_json(USERS_FILE, USERS_DB)
save_json(CONTACTS_FILE, CONTACTS_DB)
