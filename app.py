eimport streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="GÉNERA | Test di Autovalutazione",
    page_icon="🧭",
    layout="centered"
)

# --- STILE CUSTOM (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
    }
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #D35400; /* Arancio mattone */
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #A04000;
        color: white;
    }
    .profile-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #ecf0f1;
        border-left: 5px solid #2c3e50;
        margin-top: 20px;
    }
    .quote {
        font-style: italic;
        color: #7f8c8d;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI DI SUPPORTO GRAFICO ---

def draw_chart(x_score, y_score):
    """
    Disegna il grafico cartesiano con i 4 quadranti e la posizione dell'utente.
    Range assi: 5 - 20. Centro: 12.5.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Impostazioni Assi
    ax.set_xlim(5, 20)
    ax.set_ylim(5, 20)
    ax.set_xticks([]) # Nascondi numeri
    ax.set_yticks([]) # Nascondi numeri
    
    # Rimuovi bordi esterni standard
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Linee Mediane (Assi Cartesiani)
    ax.axhline(y=12.5, color='#7f8c8d', linestyle='--', linewidth=1)
    ax.axvline(x=12.5, color='#7f8c8d', linestyle='--', linewidth=1)

    # DEFINIZIONE QUADRANTI (Colori pastello)
    # Q1: Alto Destra (Futuro + Faccio) -> VERDE (Cantiere)
    ax.add_patch(patches.Rectangle((12.5, 12.5), 7.5, 7.5, color='#ABEBC6', alpha=0.5))
    # Q2: Alto Sinistra (Passato + Faccio) -> GIALLO (Criceto)
    ax.add_patch(patches.Rectangle((5, 12.5), 7.5, 7.5, color='#F9E79F', alpha=0.5))
    # Q3: Basso Sinistra (Passato + Penso) -> GRIGIO (Museo)
    ax.add_patch(patches.Rectangle((5, 5), 7.5, 7.5, color='#D7DBDD', alpha=0.5))
    # Q4: Basso Destra (Futuro + Penso) -> AZZURRO (Visionario)
    ax.add_patch(patches.Rectangle((12.5, 5), 7.5, 7.5, color='#AED6F1', alpha=0.5))

    # LABEL ASSI
    ax.text(20, 12.3, 'FUTURO', ha='right', va='top', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.text(5, 12.3, 'PASSATO', ha='left', va='top', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.text(12.6, 20, 'FACCIO (Azione)', ha='left', va='top', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.text(12.6, 5, 'PENSO (Riflessione)', ha='left', va='bottom', fontsize=10, fontweight='bold', color='#2c3e50')

    # LABEL QUADRANTI
    ax.text(16.25, 16.25, 'IL CANTIERE\nDELLA CATTEDRALE', ha='center', va='center', fontweight='bold', fontsize=9, color='#145A32')
    ax.text(8.75, 16.25, 'IL CRICETO\nEFFICIENTE', ha='center', va='center', fontweight='bold', fontsize=9, color='#7D6608')
    ax.text(8.75, 8.75, 'IL MUSEO\nDELLE CERE', ha='center', va='center', fontweight='bold', fontsize=9, color='#424949')
    ax.text(16.25, 8.75, 'IL VISIONARIO\nDA DIVANO', ha='center', va='center', fontweight='bold', fontsize=9, color='#154360')

    # POSIZIONAMENTO UTENTE (La Lancetta)
    # Disegniamo un punto rosso con bordo bianco
    ax.scatter(x_score, y_score, color='#E74C3C', s=200, edgecolors='white', linewidth=2, zorder=10)
    
    fig.patch.set_alpha(0) # Sfondo trasparente
    return fig

def get_feedback(x, y):
    """Restituisce titolo e testo del profilo basato sui punteggi."""
    # Soglia centrale = 12.5 (Scala 5-20)
    is_future = x > 12.5
    is_action = y > 12.5

    if is_action and is_future:
        return {
            "title": "IL CANTIERE DELLA CATTEDRALE",
            "desc": "Sei nel quadrante della **Generatività**. Unisci la visione del domani alla capacità di sporcarti le mani oggi. Non ti limiti a sognare o a ripetere gesti vuoti: costruisci valore. Sei colui che pianta alberi sotto la cui ombra non si siederà, ma lo fa comunque.",
            "tip": "Attento al delirio di onnipotenza. Anche le cattedrali hanno bisogno di fondamenta solide: ogni tanto controlla la staticità della struttura."
        }
    elif is_action and not is_future:
        return {
            "title": "IL CRICETO EFFICIENTE",
            "desc": "Sei una macchina da guerra. Lavori tantissimo, sudi, ti impegni. Il problema? **Corri verso il passato**. Sei bravissimo a mantenere in vita procedure e modi di fare che forse non servono più. Grande fatica, poca evoluzione.",
            "tip": "Fermati. Respira. Chiediti 'Perché lo faccio?' prima di 'Come posso farlo più velocemente?'. Alza la testa dal manubrio."
        }
    elif not is_action and is_future:
        return {
            "title": "IL VISIONARIO DA DIVANO",
            "desc": "Hai capito tutto: vedi i trend, intuisci il futuro, hai idee brillanti. Peccato che **restino tutte nella tua testa**. Soffri di 'pensabilità' senza 'possibilitazione'. Il mondo cambia mentre tu perfezioni il piano strategico.",
            "tip": "Come dico nel mio libro: **Fallo!** Prendi l'idea più imperfetta che hai e realizzala entro stasera. Smetti di pianificare, inizia a sbagliare."
        }
    else:
        return {
            "title": "IL MUSEO DELLE CERE",
            "desc": "Sei in una zona di stallo. Il pensiero è rivolto a 'come si stava meglio una volta' e l'azione è paralizzata. È il regno della nostalgia sterile e della resistenza al cambiamento. Qui non cresce nulla.",
            "tip": "Devi rompere l'inerzia. Trova una cosa piccolissima da cambiare domani mattina. Una sola. Non importa se sbagli, l'importante è muovere l'aria."
        }

# --- HEADER E LOGO ---
# Abbiamo allargato la prima colonna (da 1 a 1.5) per dare spazio al logo
col_logo, col_title = st.columns([1.5, 3.5])

with col_logo:
    try:
        # use_container_width=True adatta l'immagine alla larghezza della colonna
        st.image("Logo.png", use_container_width=True)
    except:
        # Fallback testuale
        st.markdown("### 🧬 GÉNERA")
        
with col_title:
    st.title("Navigatore Esistenziale")
    st.markdown("**Test di autovalutazione sulla capacità di affrontare il domani**")

st.markdown("---")

# --- INTRODUZIONE TEORICA ---
with st.expander("Introduzione", expanded=True):
    st.markdown("""
    Benvenuto. Se sei qui, probabilmente senti che il terreno sotto i piedi – quello che chiamavamo "certezze" o in alcuni casi "posto fisso" – sta tremando.
    
    Come racconto spesso nei miei lavori sulla *psicologia delle risorse umane*, l'essere umano di fronte alla novità (o all'imprevisto) si muove su due grandi assi:
    1.  **Il Tempo (Asse X):** Guardiamo nello specchietto retrovisore ciò che sta alle nostre spalle (**Passato**) cercando sicurezza, o piuttosto guardiamo avanti a noi nel parabrezza (**Futuro**) accettando il rischio?
    2.  **L'Energia (Asse Y):** Restiamo nel mondo delle idee (**Penso**) oppure ci attiviamo per trasformare la realtà (**Faccio**)?
    
    Questo strumento vuole provare a descrivere il nostro orientamento. Non è una sentenza, è piuttosto una bussola. Serve a capire dove ultimamente hai piantato la tenda  e, se necessario, a smontarla per spostarti altrove.
    """)

# --- DATI SOCIO ANAGRAFICI ---
st.subheader("1. Chi sei?")
st.caption("Pochi dati per contestualizzare il tuo profilo.")
col1, col2 = st.columns(2)
with col1:
    Genere = st.text_input("Genere", placeholder="Es. Uomo, Donna, Non Binario, Non risponde")
with col2:
    Età = st.text_input("Fascia d'età", placeholder="Es.fino a 20 anni, 21-30 anni, 31-40 anni, 41-50 anni, 51-60 anni, 61-70 anni, più di 70 anni")

# --- IL TEST (ITEMS) ---
st.subheader("2. Il Test")
st.info("Valuta le affermazioni su una scala va da da 1 (Per nulla d'accordo) a 4 (Del tutto d'accordo). Sii onesto, io ti vedo!")

# Definizione Domande
items = [
    # ASSE X: PASSATO vs FUTURO
    {"text": "Di fronte a un cambiamento improvviso, la mia prima reazione è il fastidio per ciò che perdo rispetto al 'solito modo'.", "axis": "X", "reverse": True},
    {"text": "Mi capita spesso di pensare che 'una volta le cose erano più semplici e ordinate'.", "axis": "X", "reverse": True},
    {"text": "L'idea di dover imparare una competenza da zero mi stimola più di quanto mi spaventi.", "axis": "X", "reverse": False},
    {"text": "Preferisco una soluzione imperfetta ma innovativa rispetto a una procedura collaudata ma obsoleta.", "axis": "X", "reverse": False},
    {"text": "Vedo l'imprevisto come un guastafeste che rovina i miei piani, piuttosto che come un'opportunità.", "axis": "X", "reverse": True},

    # ASSE Y: PENSO vs FACCIO
    {"text": "Ho 'nel cassetto' molte idee e progetti che non ho mai provato a realizzare concretamente.", "axis": "Y", "reverse": True},
    {"text": "Di fronte a un problema, mi attivo subito per fare qualcosa, anche se non ho ancora tutte le informazioni.", "axis": "Y", "reverse": False},
    {"text": "Prima di agire ho bisogno di analizzare tutte le possibili conseguenze negative, e questo spesso mi rallenta.", "axis": "Y", "reverse": True},
    {"text": "Credo nella filosofia del 'Fatto è meglio che perfetto'.", "axis": "Y", "reverse": False},
    {"text": "Spesso mi ritrovo a rimuginare su decisioni prese, pensando a cosa avrei potuto fare diversamente.", "axis": "Y", "reverse": True},
]

# Form per la raccolta dati
scores_x = []
scores_y = []

with st.form("test_form"):
    for i, item in enumerate(items):
        st.markdown(f"**{i+1}. {item['text']}**")
        val = st.radio(
            f"Risposta item {i+1}", 
            options=[1, 2, 3, 4], 
            index=None, 
            horizontal=True, 
            label_visibility="collapsed",
            key=f"q{i}"
        )
        st.markdown("---")
        
        if val is not None:
            points = (5 - val) if item['reverse'] else val
            if item['axis'] == "X":
                scores_x.append(points)
            else:
                scores_y.append(points)

    submitted = st.form_submit_button("CALCOLA IL MIO PROFILO")

# --- RESTITUZIONE FEEDBACK ---
if submitted:
    if len(scores_x) + len(scores_y) < 10:
        st.error("⚠️ Per favore, rispondi a tutte le domande per ottenere un profilo accurato.")
    else:
        total_x = sum(scores_x)
        total_y = sum(scores_y)
        
        feedback = get_feedback(total_x, total_y)
        
        st.success("Analisi completata!")
        
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.markdown(f"### {feedback['title']}")
            
            st.markdown(f"""
            <div class="profile-box">
                <p>{feedback['desc']}</p>
                <hr style="border-top: 1px solid #bdc3c7;">
                <p class="quote">💡 <strong>Il consiglio di Gheno:</strong><br>{feedback['tip']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Dettagli Punteggi"):
                st.write(f"Orientamento al Futuro (Asse X): {total_x}/20")
                st.write(f"Orientamento all'Azione (Asse Y): {total_y}/20")

        with res_col2:
            st.caption("La tua posizione nella Matrice:")
            fig = draw_chart(total_x, total_y)
            st.pyplot(fig)

# --- FOOTER ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #95a5a6; font-size: 0.8em;'>
    Developed for <strong>GÉNERA</strong> | Based on the works of Stefano Gheno<br>
    <em>"Non c'è nulla di più pratico di una buona teoria... se poi la applichi."</em>
    </div>
    """, 
    unsafe_allow_html=True
)
