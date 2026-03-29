import streamlit as st
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import TTS
try:
    from gtts import gTTS
    import base64
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="AI4Citizens",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data thu tuc
PROCEDURES = {
    "khai_sinh": {
        "name": "Dang ky khai sinh",
        "docs": ["Giay khai sinh", "CCCD cha", "CCCD me"],
        "time": "1-3 ngay",
        "fee": "Mien phi",
        "detail": """
        **CAC BUOC THUC HIEN:**

        1. **Giay khai sinh** (Mau don)
           - Lay tai UBND phuong/xa
           - Hoac tai tu Cong dich vu cong

        2. **CCCD/CMND cua cha** (ban photo)
           - Photo ro 2 mat
           - Chua qua 6 thang

        3. **CCCD/CMND cua me** (ban photo)
           - Photo ro 2 mat
           - Chua qua 6 thang

        **DEN NOP:**
        - UBND phuong/xa
        - Hoac online qua Cong dich vu cong
        - Thoi gian: 1-3 ngay lam viec
        - Mien phi
        """
    },
    "khai_tu": {
        "name": "Dang ky khai tu",
        "docs": ["Giay khai tu", "Giay bao tu", "CCCD nguoi mat", "CCCD nguoi lam don"],
        "time": "3-5 ngay",
        "fee": "Mien phi",
        "detail": """
        **CAC BUOC THUC HIEN:**

        1. **Giay dang ky khai tu**
           - Mau don co san tai UBND

        2. **Giay bao tu**
           - Cua co quan y te/benh vien

        3. **CCCD nguoi da mat**

        4. **CCCD nguoi lam don** (nguoi than)

        **DEN NOP:**
        - UBND phuong/xa noi nguoi mat thuong tru
        - Mien phi
        """
    },
    "cap_cccd": {
        "name": "Cap lai CCCD",
        "docs": ["Don xin cap lai", "So ho khau"],
        "time": "7-14 ngay",
        "fee": "11.000 - 22.000 VND",
        "detail": """
        **CAC BUOC THUC HIEN:**

        1. **Don xin cap lai CCCD**
           - Mau don tai UBND
           - Ly do: Mat, Hong, Thay doi thong tin

        2. **So ho khau** hoac **Giay xac nhan**
           - Ban photo

        **LE PHI:**
        - Lan dau: 11.000 VND
        - Lan 2 tro di: 22.000 VND

        **DEN NOP:**
        - Cong an quan
        """
    },
    "ket_hon": {
        "name": "Dang ky ket hon",
        "docs": ["Don DKKH", "CCCD vo", "CCCD chong", "Giay xac nhan hon nhan"],
        "time": "3-5 ngay",
        "fee": "Mien phi",
        "detail": """
        **CAC BUOC THUC HIEN:**

        1. **Don dang ky ket hon**
           - Mau don tai UBND

        2. **CCCD/CMND cua vo va chong**
           - Ban photo, chua qua 6 thang

        3. **Giay xac nhan tinh trang hon nhan**
           - Xac nhan doc than
           - Hoac xac nhan chua ket hon

        **DIEU KIEN:**
        - Neu vuoi/ong qua 60 tuoi: Khong can giay xac nhan

        **DEN NOP:**
        - UBND phuong/xa
        """
    },
    "tam_tru": {
        "name": "Dang ky tam tru",
        "docs": ["Don DKTTru", "CCCD", "Giay xac nhan noi o"],
        "time": "1-3 ngay",
        "fee": "Mien phi",
        "detail": """
        **CAC BUOC THUC HIEN:**

        1. **Don dang ky tam tru**
           - Mau don tai UBND

        2. **CCCD/CMND**
           - Ban photo

        3. **Giay xac nhan noi o**
           - Cua chu nha
           - Hoac cua co so quan ly

        **PHAM VI:**
        - Oi cung nguoi than: Giay xac nhan nguoi than
        - Oi tro: Hop dong thue nha

        **DEN NOP:**
        - Cong an phuong
        """
    }
}

# Chatbot function
def chatbot_response(message):
    msg = message.lower()

    if "khai sinh" in msg or "sinh con" in msg or "be" in msg:
        return PROCEDURES["khai_sinh"]["detail"]
    elif "khai tu" in msg or "tu" in msg or "chet" in msg:
        return PROCEDURES["khai_tu"]["detail"]
    elif "cccd" in msg or "can cuoc" in msg or "cmnd" in msg:
        return PROCEDURES["cap_cccd"]["detail"]
    elif "ket hon" in msg or "cuoi" in msg or "dam cuoi" in msg:
        return PROCEDURES["ket_hon"]["detail"]
    elif "tam tru" in msg or "cho o" in msg or "thue nha" in msg:
        return PROCEDURES["tam_tru"]["detail"]
    else:
        return "**Toi co the tro gi ve cac thu tuc:**\n\n- Dang ky khai sinh\n- Dang ky khai tu\n- Cap lai CCCD\n- Dang ky ket hon\n- Dang ky tam tru\n\nHay nhap ten thu tuc ban can tro giu!"

# Text to Speech
def text_to_audio(text):
    if not TTS_AVAILABLE:
        return None
    try:
        clean_text = text.replace("*", "").replace("#", "").replace("(", "").replace(")", "")
        tts = gTTS(text=clean_text, lang="vi", slow=False)
        path = f"/tmp/audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
        tts.save(path)
        return path
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        return None

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/4A90E2/FFFFFF?text=AI4Citizens", use_column_width=True)
    st.title("🏛️ AI4Citizens")

    st.markdown("---")

    page = st.radio(
        "Chon chuc nang:",
        ["🏠 Trang chu", "💬 Chatbot", "📋 Kiem tra giay to", "📚 Danh sach", "🔊 Nghe"]
    )

    st.markdown("---")
    st.markdown("**Cuoc thi:** Sang tao Thanh thien nien TP.HCM lan thu 21")
    st.markdown("**Bang:** C (Hoc sinh THPT)")
    st.markdown("**Deadline:** 17/4/2026")

# ============================================
# MAIN CONTENT
# ============================================

if page == "🏠 Trang chu":
    st.title("🏛️ Tro Ly Thu Tuc Hanh Chinh")
    st.markdown("### Ho tro nguoi dan thuc hien thu tuc hanh chinh cap phuong/xa")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Thu tuc", "5", "loai")
    with col2:
        st.metric("Ho tro", "24/7", "ngay")
    with col3:
        st.metric("Mien phi", "100%", "luon")

    st.markdown("---")

    st.subheader("Tinh nang chinh")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🤖 Chatbot
        - Tu van 24/7
        - Hieu cau hoi tu nhien
        - Tra loi nhanh chong
        """)
        st.markdown("""
        ### 📋 Kiem tra giay to
        - Phat hiet giay to thieu
        - Goi y giay to can them
        - Luu thoi gian
        """)

    with col2:
        st.markdown("""
        ### 🔊 Doc cau tra loi
        - Ho tro nguoi lon tuoi
        - Ho tro nguoi khiem thi
        - Gioi noi Tieng Viet
        """)
        st.markdown("""
        ### 📚 Danh sach thu tuc
        - Huong dan chi tiet
        - Le phi moi thu tuc
        - Thoi gian xu ly
        """)

elif page == "💬 Chatbot":
    st.title("💬 Chatbot Tu Van")

    st.markdown("Hoi ve thu tuc hanh chinh - Nhan cau traloi ngay")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Nhap cau hoi..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            response = chatbot_response(prompt)
            st.markdown(response)

        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Examples
    st.markdown("---")
    st.markdown("**Vi du cau hoi:**")
    ex1, ex2, ex3, ex4 = st.columns(4)
    with ex1:
        if st.button("Khai sinh"):
            st.session_state.messages.append({"role": "user", "content": "Lam khai sinh can giay to gi?"})
            st.rerun()
    with ex2:
        if st.button("Ket hon"):
            st.session_state.messages.append({"role": "user", "content": "Thu tuc dang ky ket hon"})
            st.rerun()
    with ex3:
        if st.button("CCCD"):
            st.session_state.messages.append({"role": "user", "content": "Cap lai CCCD mat"})
            st.rerun()
    with ex4:
        if st.button("Tam tru"):
            st.session_state.messages.append({"role": "user", "content": "Dang ky tam tru o dau?"})
            st.rerun()

elif page == "📋 Kiem tra giay to":
    st.title("📋 Kiem Tra Giay To Con Thieu")

    st.markdown("Kiem tra giay to can thiet cho thu tuc hanh chinh")

    # Select procedure
    procedure_keys = [k for k in PROCEDURES.keys()]
    procedure_names = [PROCEDURES[k]["name"] for k in procedure_keys]

    selected_idx = st.selectbox("Chon thu tuc:", range(len(procedure_names)), format_func=lambda x: procedure_names[x])
    selected_key = procedure_keys[selected_idx]
    selected_proc = PROCEDURES[selected_key]

    st.markdown("---")

    # Display required documents
    st.subheader(f"📄 {selected_proc['name'].upper()}")
    st.markdown(f"**Thoi gian:** {selected_proc['time']} | **Le phi:** {selected_proc['fee']}")

    st.markdown("---")
    st.markdown("### Giay to can co:")

    for i, doc in enumerate(selected_proc["docs"], 1):
        st.checkbox(f"{i}. {doc}", key=f"doc_{i}")

    # Check button
    if st.button("🔍 Kiem tra", type="primary"):
        checked = sum(1 for i in range(len(selected_proc["docs"])) if st.session_state.get(f"doc_{i+1}", False))
        total = len(selected_proc["docs"])

        if checked == total:
            st.success(f"🎉 TUYET VOI! Ho so DA DAY DU ({checked}/{total})")
            st.info(f"Ban co the nop ho so ngay! Thoi gian: {selected_proc['time']}, Le phi: {selected_proc['fee']}")
        else:
            warning = f"⚠️ Con thieu {total - checked} giay to:"
            missing = []
            for i, doc in enumerate(selected_proc["docs"], 1):
                if not st.session_state.get(f"doc_{i}", False):
                    missing.append(f"{i}. {doc}")
            st.warning(warning)
            for m in missing:
                st.markdown(f"  - {m}")

    st.markdown("---")
    st.info("💡 Ban khong can upload anh - chi can tick vao giay to da co!")

elif page == "📚 Danh sach":
    st.title("📚 Danh Sach Thu Tuc Hanh Chinh")

    st.markdown("Danh sach tat ca thu tuc duoc ho tro:")

    for i, (key, proc) in enumerate(PROCEDURES.items(), 1):
        with st.expander(f"{i}. {proc['name']}", expanded=False):
            st.markdown(f"**Thoi gian:** {proc['time']}")
            st.markdown(f"**Le phi:** {proc['fee']}")
            st.markdown("**Giay to can co:**")
            for doc in proc["docs"]:
                st.markdown(f"  - {doc}")
            st.markdown("---")
            st.markdown(proc["detail"])

elif page == "🔊 Nghe":
    st.title("🔊 Nghe Cau Tra Loi")

    st.markdown("Tu dong doc cau tra loi bang gioi noi Tieng Viet")

    st.info("💡 Dung bang Chatbot truoc, roi quay lai day de nghe cau tra loi gan nhat!")

    # Get last assistant message
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        # Find last assistant message
        last_response = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "assistant":
                last_response = msg["content"]
                break

        if last_response:
            st.subheader("Cau tra loi gan nhat:")
            st.markdown(last_response)

            st.markdown("---")

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔊 NGHE", type="primary"):
                    audio_path = text_to_audio(last_response)
                    if audio_path:
                        st.success("Da xong! Bam play de nghe.")
                        try:
                            audio_file = open(audio_path, "rb")
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format="audio/mp3")
                        except:
                            st.warning("Khong the phat audio truc tiep. Vui long thu lai.")
                    else:
                        st.error("Khong the tao audio. TTS khong ho tro.")
        else:
            st.warning("Chua co cau tra loi nao! Hay dung Chatbot truoc.")
    else:
        st.warning("Chua co cau tra loi! Hay vao tab Chatbot de dat cau hoi.")

    st.markdown("---")
    st.markdown("### Ho tro:")
    st.markdown("- Nguoi lon tuoi")
    st.markdown("- Nguoi khiem thi")
    st.markdown("- Nguoi ban roi")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Made with ❤️ by AI4Citizens Team | Sang tao Thanh thien nien TP.HCM 2026</div>", unsafe_allow_html=True)
