import streamlit as st
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
            "title": "IL CANTIERE DELLA CATTEDRALE 🏗️",
            "desc": "Sei nel quadrante della **Generatività**. Unisci la visione del domani alla capacità di sporcarti le mani oggi. Non ti limiti a sognare o a ripetere gesti vuoti: costruisci valore. Sei colui che pianta alberi sotto la cui ombra non si siederà, ma lo fa comunque.",
            "tip": "Attento al delirio di onnipotenza. Anche le cattedrali hanno bisogno di fondamenta solide: ogni tanto controlla la staticità della struttura."
        }
    elif is_action and not is_future:
