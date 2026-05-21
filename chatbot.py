import streamlit as st
import time
import os
import re
import wikipedia

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ISAS SCHOOL CHATBOT — Indian School Al Seeb
# NO API KEY NEEDED — works 100% offline!
# Run:  py -m streamlit run chatbot.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCHOOL_DATA = {

    "hello": {
        "keywords": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste", "salam", "hii", "hola"],
        "short": "Hello! 👋 Welcome to the ISAS School Chatbot — ask me anything about Indian School Al Seeb!",
        "detail": """Try asking about:
• Admission procedure
• Contact information
• School staff & teachers
• Academics & curriculum
• Latest circulars
• Sports achievements
• Documents needed
• Fees, uniform, transport

Just type your question below!""",
        "images": [],
    },

    "general": {
        "keywords": ["isas", "about isas", "about the school", "general", "tell me about", "indian school", "about indian"],
        "short": "ISAS is a CBSE-affiliated Indian school in Seeb, Muscat, Oman — established in 2002.",
        "detail": """**Indian School Al Seeb (ISAS)**
• **Board:** CBSE (Central Board of Secondary Education), India
• **Established:** 2002 — now celebrating its Silver Jubilee (25 years)
• **Location:** PO Box 2445, PC 111, Seeb, Sultanate of Oman
• **Classes:** KG I to Class XII
• **Website:** https://www.indianschoolseeb.com
• **Online Platform (ISOVLE):** https://seeb.isovle.net/
• **YouTube:** https://www.youtube.com/channel/UCtRnPwQQaR9TR4dl9j_Z5nQ""",
        "images": [],
    },

    "contact": {
        "keywords": ["contact", "phone", "email", "call", "reach", "number", "address", "location", "where"],
        "short": "Phone: +968 24451424 | Email: info@indianschoolseeb.com | Seeb, Muscat, Oman.",
        "detail": """• **Phone:** +968 24451424 | +968 24451353
• **General Email:** info@indianschoolseeb.com
• **Principal Email:** principal@indianschoolseeb.com
• **Address:** PO Box 2445, PC 111, Seeb, Sultanate of Oman
• **Website:** https://www.indianschoolseeb.com""",
        "images": [],
    },

    "admission": {
        "keywords": ["admission", "admit", "enroll", "enrol", "register", "registration", "join", "apply", "application", "new student"],
        "short": "Register online at indianschoolsoman.com (20 Jan – 20 Feb 2026). Processing fee: OMR 15.",
        "detail": """**9-Step Admission Procedure:**
1. Online Registration at www.indianschoolsoman.com
2. BOD (Board of Directors) Allotment
3. Intimation from school via SMS/Email
4. Submit all required documents at ISAS
5. Document verification
6. Principal's approval
7. GR Number / Section allotment
8. Fee payment
9. Admission confirmation via email

• **Processing Fee:** OMR 15 (non-refundable)
• **Registration:** 20th Jan – 20th Feb 2026
• **Apply:** https://indianschoolsoman.com/our-services/admission-2026-27/
• Primarily for Indian Nationals; others need Embassy NOC""",
        "images": [],
    },

    "documents_kg1": {
        "keywords": ["document kg1", "documents kg 1", "kg1", "kg i", "kindergarten 1", "papers kg1", "documents for kg1", "kg 1"],
        "short": "KG I needs: Birth cert, passport copies, resident card, health card, photo.",
        "detail": """**Documents for KG I:**
• Birth Certificate (child)
• Passport copy — first, last & visa page (child + parent)
• Resident card copy (child + parent)
• Health card / Immunization card
• Passport-size photo of child
• NOC from Embassy *(other nationalities only)*
• Undertaking form *(other nationalities only)*""",
        "images": [],
    },

    "documents_kg2": {
        "keywords": ["document kg2", "documents kg 2", "kg2", "kg ii", "kindergarten 2", "papers kg2"],
        "short": "KG II needs everything for KG I + Transfer Certificate (TC) and previous report card.",
        "detail": """**Documents for KG II:**
All KG I documents PLUS:
• Original Transfer/Leaving Certificate (TC) from previous school
• Mark sheet / Report card of previous class""",
        "images": [],
    },

    "documents": {
        "keywords": ["document", "papers", "required", "need to bring", "tc", "transfer certificate", "what do i need"],
        "short": "Classes I to IX need: Birth cert, passport, resident card, TC, report card, photo.",
        "detail": """**Documents for Classes I to IX:**
• Birth Certificate (child)
• Passport copy — first, last & visa page (child + parent)
• Resident card copy (child + parent)
• Original Transfer/Leaving Certificate (TC)
• Mark sheet / Report card of previous class
• Passport-size photo
• NOC + Undertaking form *(other nationalities only)*

*Ask "documents for KG I" or "documents for KG II" for kindergarten specifics.*""",
        "images": [],
    },

    "fees": {
        "keywords": ["fee", "fees", "cost", "price", "payment", "pay", "money", "how much", "tuition", "charges"],
        "short": "Admission processing fee is OMR 15. Full fee structure: indianschoolseeb.com/fee-structure/",
        "detail": """• **Admission Processing Fee:** OMR 15 (non-refundable)
• Full fee structure is available on the school website as images
• **View fees:** https://www.indianschoolseeb.com/fee-structure/
• Contact for specific queries: +968 24451424 | info@indianschoolseeb.com""",
        "images": [],
    },

    "uniform": {
        "keywords": ["uniform", "dress", "dress code", "what to wear", "clothes", "school uniform", "wear", "students wear"],
        "short": "Students must wear the official ISAS uniform. Details at indianschoolseeb.com/uniform/",
        "detail": """• Students must wear the official ISAS school uniform
• Uniform details and images: https://www.indianschoolseeb.com/uniform/
• Info is provided during admission
• Contact: +968 24451424 | info@indianschoolseeb.com""",
        "images": [],
    },

    "transport": {
        "keywords": ["bus", "transport", "pick up", "drop", "travel", "van", "ride", "school bus"],
        "short": "ISAS provides bus transport across Muscat. Details: indianschoolseeb.com/transport/",
        "detail": """• School bus routes cover various areas across Muscat
• For routes and transport fees: https://www.indianschoolseeb.com/transport/
• Contact: +968 24451424 | info@indianschoolseeb.com""",
        "images": [],
    },

    "timing": {
        "keywords": ["timing", "time", "schedule", "hours", "when", "open", "start", "end", "clock"],
        "short": "School hours: approximately 7:00 AM to 1:30 PM.",
        "detail": """• School hours: 7:00 AM – 1:30 PM (approx.)
• Follows the CBSE academic calendar
• Timings may vary for KG and senior sections
• Contact: +968 24451424 for exact timings""",
        "images": [],
    },

    "academics": {
        "keywords": ["academic", "curriculum", "cbse", "syllabus", "subjects", "which board", "board", "structure", "stream", "classes offered", "classes"],
        "short": "CBSE curriculum, KG I through Class XII (Science, Commerce, Humanities).",
        "detail": """**Academic Structure (CBSE Curriculum):**
• **Kindergarten:** KG I, KG II, KG III
• **Primary:** Class I to V
• **Middle School:** Class VI to VIII
• **Secondary:** Class IX to X (CBSE Board Exams)
• **Senior Secondary:** Class XI to XII (CBSE Board Exams)

Streams in XI-XII: Science, Commerce, Humanities""",
        "images": [],
    },

    "exam": {
        "keywords": ["exam", "test", "assessment", "marks", "result", "grade", "report card", "board exam"],
        "short": "CBSE pattern — internal assessments for I to VIII, Board exams for X and XII.",
        "detail": """• **Classes I to VIII:** Internal school assessments
• **Class X:** CBSE Board Examinations
• **Class XII:** CBSE Board Examinations
• Regular unit tests and periodic assessments
• Report cards after each term
• Schedules: https://www.indianschoolseeb.com/latest-circulars/""",
        "images": [],
    },

    "principal": {
        "keywords": ["principal", "principal message", "head of school", "leader", "alex", "joseph"],
        "short": "The Principal is Mr. Alex C Joseph.",
        "detail": """**Principal: Mr. Alex C Joseph**

*"Welcome to Indian School Al Seeb where dreams unfold into reality!
Every child is a possible winner. What matters is not what we teach but how we inspire them to learn."*

• **Email:** principal@indianschoolseeb.com
• **Phone:** +968 24451424""",
        "images": [],
    },

    "teachers": {
        "keywords": ["teacher", "teachers", "subject teacher", "teaching staff", "who teaches", "faculty"],
        "short": "Key teachers: Mrs Annapurna (Math), Mrs Nisha (Chem), Mr Madhusoodanan (Physics), Mrs Shamla (Eng), Mrs Shelmi (CS).",
        "detail": """**Subject Teachers:**
• **Mathematics:** Mrs Annapurna
• **Chemistry:** Mrs Nisha
• **Physics:** Mr Madhusoodanan
• **English:** Mrs Shamla
• **Computer Science:** Mrs Shelmi

**Principal:** Mr. Alex C Joseph
Full details: https://www.indianschoolseeb.com/staff/""",
        "images": [],
    },

    "math": {
        "keywords": ["math", "maths", "mathematics", "annapurna", "math teacher", "teaches math"],
        "short": "Mathematics is taught by Mrs Annapurna.",
        "detail": """• **Subject:** Mathematics
• **Teacher:** Mrs Annapurna
• ISAS follows the CBSE Mathematics curriculum from Class I to XII""",
        "images": [],
    },

    "chemistry": {
        "keywords": ["chemistry", "chem", "nisha", "chemistry teacher", "teaches chemistry"],
        "short": "Chemistry is taught by Mrs Nisha.",
        "detail": """• **Subject:** Chemistry
• **Teacher:** Mrs Nisha
• Chemistry is offered as part of the Science stream in Classes XI-XII""",
        "images": [],
    },

    "physics": {
        "keywords": ["physics", "madhusoodanan", "physics teacher", "teaches physics"],
        "short": "Physics is taught by Mr Madhusoodanan.",
        "detail": """• **Subject:** Physics
• **Teacher:** Mr Madhusoodanan
• Physics is offered as part of the Science stream in Classes XI-XII""",
        "images": [],
    },

    "english": {
        "keywords": ["english", "shamla", "english teacher", "teaches english"],
        "short": "English is taught by Mrs Shamla.",
        "detail": """• **Subject:** English
• **Teacher:** Mrs Shamla
• English is a core subject across all classes (KG I to XII)""",
        "images": [],
    },

    "cs": {
        "keywords": ["computer science", "cs", "coding", "programming", "shelmi", "teaches computer", "cs teacher"],
        "short": "Computer Science is taught by Mrs Shelmi.",
        "detail": """• **Subject:** Computer Science
• **Teacher:** Mrs Shelmi
• CS is offered in senior classes as part of the CBSE curriculum""",
        "images": [],
    },

    "management": {
        "keywords": ["management", "smc", "committee", "president", "treasurer", "who runs"],
        "short": "SMC President: Mr. Susanth Sukumaran. Principal: Mr. Alex C Joseph.",
        "detail": """**School Management Committee (SMC):**
• **President:** Mr. Susanth Sukumaran — 99852515 — president@indianschoolseeb.com
• **Vice President:** Mr. Mohammed Abdul Jabbar Jameel — 95659024
• **Treasurer:** Mr. Moidu Achar Kandiyil — 97825027
• **Head of Purchase:** Mr. Syed Ilyas Ahmed Hussaini — 90635557
• **Head of Sports & HSE:** Mr. Siddeque Thevar Thodi — 96585252
• **Head of Academics:** Mr. Muneer Thaze Purayil — 98661560
• **Head of Staff Welfare:** Dr. Farea Azmi — 79272768
• **Head of IT:** Mr. Ramaswamy — 93219984""",
        "images": [],
    },

    "staff": {
        "keywords": ["staff", "admin staff", "administration", "office staff", "employee", "who works", "non-teaching", "operations manager", "manager"],
        "short": "ISAS has 20+ admin staff and 5 key subject teachers. Principal: Mr. Alex C Joseph.",
        "detail": """**Principal:** Mr. Alex C Joseph

**Subject Teachers:**
• Mrs Annapurna — Mathematics
• Mrs Nisha — Chemistry
• Mr Madhusoodanan — Physics
• Mrs Shamla — English
• Mrs Shelmi — Computer Science

**Administration Staff:**
• Anilkumar Nair — Operations Manager (MBA, 20+ yrs)
• Sriram Natarajan — Budget Planner & Analyst (20+ yrs)
• Fahad Hassan — Staff (B.Sc CS, 20+ yrs)
• Huda Y. N. Alkhusaibi — HR (14 yrs school + 6 yrs banking)
• Wilson Syprian Pereira — Staff (17.5 yrs)
• Liju Chandy — Staff / Finance (M.Com, 14.5 yrs)
• Babu Marangattil Thomas — Staff / Procurement (26 yrs)
• Gokul Gopinath — Staff / Electronics & IT (16 yrs)
• Geenamol Anish — First Aid / Nurse (17 yrs)
• Aamal Salim Al Badaai — IT (BCA, 8 yrs)

Full details: https://www.indianschoolseeb.com/staff/""",
        "images": [],
    },

    "sports": {
        "keywords": ["sport", "sports", "game", "cricket", "hockey", "chess", "football", "badminton", "table tennis", "tournament", "athletics", "achievement", "award", "winner", "champion", "trophy"],
        "short": "CBSE National Winners 2025: Hockey, Cricket & Chess teams!",
        "detail": """**CBSE National Champions (2025):**
• Hockey Team — CBSE National Champions
• Cricket Team — CBSE National Champions
• Chess Team — CBSE National Champions

**More Achievements (2025-2026):**
• Under-19 Boys Cricket — Silver Medal, CBSE Nationals, Noida
• Under-17 Girls Cricket — Bronze, CBSE Nationals, Bhopal
• Under-14 Boys Hockey — Bronze, CBSE Nationals, Bhopal
• Velavaa Ragavesh — Gold Medal, 69th SGFI National Chess Championship

**Upcoming:** Inter House Badminton Tournament, CBSE Oman Cluster Table Tennis 2026

**Head of Sports:** Mr. Siddeque Thevar Thodi — 96585252""",
        "images": [],
    },

    "silver_jubilee": {
        "keywords": ["silver jubilee", "25 years", "anniversary", "celebration", "founded", "established", "history", "alumni"],
        "short": "ISAS celebrates its Silver Jubilee (25 years) — established 2002!",
        "detail": """**Silver Jubilee — 25 Years of ISAS!**
• Established in 2002 in Seeb, Muscat
• Silver Jubilee celebration: 25 April 2026
• First Alumni gathering "Alumni Rendezvous" hosted
• ISAS Alumni Association instituted
More: https://www.indianschoolseeb.com/silver_jubilee/""",
        "images": [],
    },

    "circulars": {
        "keywords": ["circular", "notice", "announcement", "latest", "news", "update", "event"],
        "short": "Latest circulars include parent orientations, CBSE accommodations, and book sales (April 2026).",
        "detail": """**Latest Circulars (April 2026):**
• 28 Apr — Class IX: Accommodations & Exemptions by CBSE
• 21 Apr — Classes VI-VIII: Parent Orientation Programme
• 22 Apr — Classes IX-XII: Parent Orientation Programme
• 23 Apr — Classes I-V: National Technology Day Competitions
• 28 Apr — Class KG III: Book Sale

View all: https://www.indianschoolseeb.com/latest-circulars/""",
        "images": [],
    },

    "isovle": {
        "keywords": ["isovle", "online learning", "e-learning", "virtual", "online class", "online platform", "virtual learning"],
        "short": "ISOVLE is the online learning platform — access at seeb.isovle.net",
        "detail": """• **Platform:** ISOVLE (Indian School Online Virtual Learning Environment)
• **Access:** https://seeb.isovle.net/
• Login credentials are provided by the school
• IT support: Mr. Ramaswamy — 93219984 — smc.it@indianschoolseeb.com""",
        "images": [],
    },

    "website": {
        "keywords": ["website", "site", "link", "url", "portal", "school website", "web address"],
        "short": "Main site: indianschoolseeb.com | ISOVLE: seeb.isovle.net",
        "detail": """• **Main Website:** https://www.indianschoolseeb.com
• **ISOVLE (Online Learning):** https://seeb.isovle.net/
• **Admission Portal:** https://indianschoolsoman.com/our-services/admission-2026-27/
• **Circulars:** https://www.indianschoolseeb.com/latest-circulars/
• **Fee Structure:** https://www.indianschoolseeb.com/fee-structure/
• **YouTube:** https://www.youtube.com/channel/UCtRnPwQQaR9TR4dl9j_Z5nQ""",
        "images": [],
    },

    "health": {
        "keywords": ["health", "nurse", "first aid", "infirmary", "medical", "sick", "doctor", "school nurse"],
        "short": "ISAS has a dedicated infirmary with trained first-aid staff.",
        "detail": """**Health & First Aid:**
• **Geenamol Anish** — First Aid / Nurse (17 yrs experience)
• **Zawan Abdullah Al Wahibi** — Infirmary Assistant (since 2004)
• **Fatihya Abdu Rahman Al Zarafi** — Nurse Assistant""",
        "images": [],
    },

    "it": {
        "keywords": ["it", "computer", "tech", "technology", "wifi", "internet", "login", "password"],
        "short": "IT Head: Mr. Ramaswamy — 93219984 | smc.it@indianschoolseeb.com",
        "detail": """**IT Support:**
• **Head of IT (SMC):** Mr. Ramaswamy — 93219984 — smc.it@indianschoolseeb.com
• **IT Staff:** Mrs. Aamal Salim Al Badaai (BCA, 8 yrs)
• **IT Staff:** Mr. Gokul Gopinath (M.Tech Applied Electronics, 16 yrs)""",
        "images": [],
    },

    "reaction": {
        "keywords": ["nice", "cool", "great", "awesome", "wow", "good", "okay", "ok", "oh", "interesting", "amazing", "perfect", "wonderful", "excellent", "fantastic", "super", "neat", "love it", "thats great", "got it", "understood", "i see", "alright", "sure", "really", "oh ok", "hmm", "hm", "ohh", "ahhh", "noice"],
        "short": "Glad you think so! Feel free to ask me anything else about ISAS!",
        "detail": """**Here are some more things you can ask:**
• Admissions & documents
• Contact info & school timings
• Staff & teachers
• Sports achievements
• Fees, uniform, transport
• Latest circulars & events

Just type your question!""",
        "images": [],
    },

    "thank": {
        "keywords": ["thank", "thanks", "thank you", "bye", "goodbye", "see you", "ok thanks"],
        "short": "You're welcome! Feel free to ask anytime.",
        "detail": """• **Website:** https://www.indianschoolseeb.com
• **Phone:** +968 24451424
• **Email:** info@indianschoolseeb.com

Have a great day!""",
        "images": [],
    },
}


# ──────────────────────────────────────────────
# FIX 1: import re moved to top (see line 4)
# ──────────────────────────────────────────────

def clean_for_wiki(question):
    """Strip question phrasing to extract a clean Wikipedia topic title."""
    q = question.strip()
    prefixes = [
        r'^what is (a |an |the )?',
        r'^what are (the )?',
        r'^who is (a |an |the )?',
        r'^tell me about (a |an |the )?',
        r'^explain (a |an |the )?',
        r'^describe (a |an |the )?',
        r'^how does (a |an |the )?',
        r'^where is (a |an |the )?',
        r'^define (a |an |the )?',
    ]
    for pattern in prefixes:
        q = re.sub(pattern, '', q, flags=re.IGNORECASE)
    return q.rstrip('?!.,').strip().title()


def find_answer(question):
    q = question.lower().strip()

    # Step 1: Search the school knowledge base
    best_match = None
    best_score = 0
    for topic, data in SCHOOL_DATA.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in q:
                score += len(keyword)
        if score > best_score:
            best_score = score
            best_match = data

    if best_match:
        return best_match

    # Step 2: Wikipedia fallback (FIX 3: increased summary from 600 → 800 chars)
    try:
        wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='ISASSchoolChatbot/1.0 (https://www.indianschoolseeb.com)'
        )
        wiki_query = clean_for_wiki(question)
        page = wiki.page(wiki_query)
        if page.exists():
            return {
                "short": f"Here's what Wikipedia says about **{page.title}**:",
                "detail": (
                    page.summary[:800]
                    + f"...\n\n[Read more on Wikipedia](https://en.wikipedia.org/wiki/{page.title.replace(' ', '_')})"
                ),
                "images": []
            }
    except Exception:
        pass

    # Step 3: Nothing found
    return {
        "short": "Sorry, I couldn't find an answer to that.",
        "detail": """Try asking about school topics like:
• Admissions & documents
• Contact info & timings
• Staff & teachers
• Sports achievements
• Fees, uniform, transport
• Latest circulars

Or contact the school: **+968 24451424** | **info@indianschoolseeb.com**""",
        "images": []
    }


# ──────────────────────────────────────────────
# FIX 2: No expander — detail shown directly
# ──────────────────────────────────────────────
def display_answer(answer_data):
    st.markdown(answer_data["short"])
    if answer_data.get("detail"):
        st.markdown(answer_data["detail"])
    if answer_data.get("images"):
        with st.expander("Photos"):
            for img_path in answer_data["images"]:
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)


# st.set_page_config must be the very first Streamlit call
st.set_page_config(page_title="ISAS School Chatbot", page_icon="🎓", layout="centered")

# ──────────────────────────────────────────────
# FIX 3: Dark neon purple/black theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

html, body { background: #060010 !important; }
.stApp {
    background: linear-gradient(135deg, #060010 0%, #0d0025 55%, #08001a 100%) !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(150,0,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(150,0,255,0.035) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none; z-index: 0;
}

/* ── HEADER ── */
.main-header { text-align: center; padding: 2.2rem 0 1.2rem; position: relative; z-index: 1; }
.main-header h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.4rem !important; font-weight: 900 !important;
    color: #e040fb !important;
    text-shadow: 0 0 18px #bf00ff, 0 0 40px #8000ff, 0 0 70px #5000bb !important;
    letter-spacing: 0.06em !important; margin-bottom: 0 !important;
}
.school-badge {
    display: inline-block;
    background: rgba(150,0,255,0.1);
    border: 1px solid rgba(150,0,255,0.45);
    border-radius: 20px; padding: 7px 20px;
    font-size: 0.85rem; color: #cc80ff !important;
    font-family: 'Rajdhani', sans-serif;
    margin-top: 0.8rem;
    box-shadow: 0 0 18px rgba(150,0,255,0.18), inset 0 0 10px rgba(150,0,255,0.05);
    letter-spacing: 0.1em; text-transform: uppercase;
}

/* ── CHAT MESSAGES ── */
div[data-testid="stChatMessage"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.08rem !important;
    background: rgba(18,0,38,0.75) !important;
    border: 1px solid rgba(150,0,255,0.22) !important;
    border-radius: 14px !important;
    box-shadow: 0 0 24px rgba(150,0,255,0.07) !important;
    backdrop-filter: blur(12px) !important;
    margin-bottom: 0.75rem !important;
    position: relative; z-index: 1;
}
div[data-testid="stChatMessage"] p { color: #ead5ff !important; line-height: 1.65 !important; }

/* ── TEXT ── */
.stMarkdown p  { color: #ead5ff !important; font-family: 'Rajdhani', sans-serif !important; line-height: 1.65 !important; }
.stMarkdown li { color: #ead5ff !important; font-family: 'Rajdhani', sans-serif !important; }
.stMarkdown strong { color: #f4c0ff !important; text-shadow: 0 0 8px rgba(210,0,255,0.35) !important; }
.stMarkdown h3 { color: #d580ff !important; font-family: 'Orbitron', monospace !important; font-size: 0.95rem !important; letter-spacing: 0.08em !important; }
.stMarkdown a  { color: #a855f7 !important; text-decoration: none !important; }
.stMarkdown a:hover { color: #e040fb !important; text-shadow: 0 0 10px rgba(224,64,251,0.5) !important; }
h3 {
    color: #cc80ff !important; font-family: 'Orbitron', monospace !important;
    font-size: 0.92rem !important; font-weight: 600 !important;
    letter-spacing: 0.1em !important; text-shadow: 0 0 12px rgba(150,0,255,0.35) !important;
}

/* ── DIVIDER ── */
hr { border-color: rgba(150,0,255,0.28) !important; box-shadow: 0 0 8px rgba(150,0,255,0.15); margin: 1rem 0 !important; }

/* ── BUTTONS ── */
div[data-testid="stButton"] button {
    border-radius: 9px !important;
    border: 1px solid rgba(150,0,255,0.38) !important;
    background: rgba(18,0,38,0.6) !important;
    color: #cc80ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important; font-weight: 500 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 0 10px rgba(150,0,255,0.08) !important;
}
div[data-testid="stButton"] button:hover {
    border-color: #bf00ff !important;
    background: rgba(150,0,255,0.14) !important;
    box-shadow: 0 0 22px rgba(150,0,255,0.38), inset 0 0 10px rgba(150,0,255,0.08) !important;
    color: #f0c0ff !important;
}

/* ── CHAT INPUT ── */
div[data-testid="stChatInput"] textarea {
    background: rgba(18,0,38,0.8) !important;
    border: 1px solid rgba(150,0,255,0.38) !important;
    border-radius: 12px !important;
    color: #ead5ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    box-shadow: 0 0 14px rgba(150,0,255,0.12) !important;
}
div[data-testid="stChatInput"] textarea:focus {
    border-color: #bf00ff !important;
    box-shadow: 0 0 28px rgba(150,0,255,0.38) !important;
}
div[data-testid="stChatInput"] textarea::placeholder { color: #7a4fa0 !important; }

/* ── FOOTER ── */
.stCaption p { color: #6b3b8a !important; font-family: 'Rajdhani', sans-serif !important; letter-spacing: 0.05em !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #060010; }
::-webkit-scrollbar-thumb { background: rgba(150,0,255,0.35); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(150,0,255,0.65); }
</style>
""", unsafe_allow_html=True)

# ── FIX 4: Header with dark-theme subtitle colour ──
st.markdown("""
<div class="main-header">
    <h1>&#127891; ISAS School Chatbot</h1>
    <h2 style="font-family: 'Rajdhani', sans-serif; font-size: 1.25rem; color: #9d60cc; font-weight: 400; margin-top: 0.5rem; letter-spacing: 0.07em;">
        INDIAN SCHOOL AL SEEB &mdash; ASK ME ANYTHING
    </h2>
    <div class="school-badge">CBSE Affiliated &bull; Seeb, Muscat, Oman &bull; Est. 2002</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── Quick-question buttons (only shown before first message) ──
if not st.session_state.messages:
    st.markdown("### Try asking:")
    cols = st.columns(2)
    quick_qs = [
        "What is the admission procedure?",
        "How can I contact the school?",
        "Who are the admin staff?",
        "What are the sports achievements?",
        "What documents do I need?",
        "What are the school timings?",
    ]
    for i, q in enumerate(quick_qs):
        with cols[i % 2]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.pending_question = q
                st.rerun()

# ── Handle quick-button click ──
if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    answer_data = find_answer(q)
    st.session_state.messages.append({"role": "user", "content": q})
    st.session_state.messages.append({"role": "assistant", "content": answer_data})
    st.rerun()

# ── Render chat history ──
for msg in st.session_state.messages:
    avatar = "🎓" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant" and isinstance(msg["content"], dict):
            display_answer(msg["content"])
        else:
            st.markdown(msg["content"])

# ── Handle typed input ──
user_input = st.chat_input("Ask about admissions, contacts, academics, sports...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🎓"):
        thinking = st.empty()
        for dots in ["🔵", "🔵🔵", "🔵🔵🔵", "✨ Finding answer..."]:
            thinking.markdown(f"*{dots}*")
            time.sleep(0.6)
        thinking.empty()

        answer_data = find_answer(user_input)
        st.session_state.messages.append({"role": "assistant", "content": answer_data})
        display_answer(answer_data)

st.divider()
st.caption("🎓 ISAS School Chatbot · Data from indianschoolseeb.com · Silver Jubilee Year 2026")
