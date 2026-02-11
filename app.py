import streamlit as st
import google.generativeai as genai
import json

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="ZEN Hyper-Nudge Demo", page_icon="🛡️", layout="centered")

# --- CSS DLA STYLIZACJI "MOBILE PUSH" ---
st.markdown("""
    <style>
    .push-notification {
        background-color: #1a1a1a;
        color: white;
        border-radius: 20px;
        padding: 20px;
        border-left: 5px solid #00ff88;
        font-family: 'Helvetica Neue', sans-serif;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .zen-logo { font-weight: bold; color: #00ff88; margin-bottom: 5px; }
    .nudge-header { font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    .nudge-body { font-size: 14px; color: #cccccc; margin-bottom: 15px; }
    .nudge-cta { background-color: #00ff88; color: black; padding: 8px 15px; border-radius: 10px; text-align: center; font-weight: bold; cursor: pointer; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- DANE TESTOWE (TWOJE 10 TRANSAKCJI) ---
transactions = [
    {"id": "TXN-001", "merchant": "Ryanair", "amount": 420.00, "currency": "PLN", "category": "Travel", "description": "Flight FR2344 WAW-STN"},
    {"id": "TXN-002", "merchant": "iSpot Apple Premium Reseller", "amount": 5499.00, "currency": "PLN", "category": "Electronics", "description": "iPhone 15 Pro 256GB"},
    {"id": "TXN-003", "merchant": "Sixt Rent a Car", "amount": 1250.00, "currency": "PLN", "category": "Car Rental", "description": "Security Deposit - Munich Airport"},
    {"id": "TXN-004", "merchant": "Ticketmaster", "amount": 890.00, "currency": "PLN", "category": "Entertainment", "description": "Coldplay Music of the Spheres Tour"},
    {"id": "TXN-005", "merchant": "Booking.com", "amount": 3200.00, "currency": "PLN", "category": "Travel", "description": "7 nights - Villa Toscana"},
    {"id": "TXN-006", "merchant": "Starbucks Madrid", "amount": 5.40, "currency": "EUR", "category": "Food & Drink", "description": "Foreign transaction detected"},
    {"id": "TXN-007", "merchant": "Amazon.pl", "amount": 2100.00, "currency": "PLN", "category": "Shopping", "description": "Sony PlayStation 5 Console"},
    {"id": "TXN-008", "merchant": "Hertz", "amount": 450.00, "currency": "PLN", "category": "Car Rental", "description": "Car rental payment"},
    {"id": "TXN-009", "merchant": "Biedronka", "amount": 145.20, "currency": "PLN", "category": "Groceries", "description": "Daily shopping"},
    {"id": "TXN-010", "merchant": "Airbnb", "amount": 650.00, "currency": "PLN", "category": "Travel", "description": "Weekend in Prague"}
]

# --- SIDEBAR: KONFIGURACJA ---
st.sidebar.title("⚙️ Konfiguracja")
api_key = st.sidebar.text_input("Wklej Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Konfiguracja modelu z instrukcjami systemowymi
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"response_mime_type": "application/json"},
        system_instruction="Jesteś ZEN Hyper-Nudge Engine. Analizujesz transakcje i proponujesz ubezpieczenia Affinity (Travel, Cancellation, Electronics All-Risk, Car Rental Excess). Jeśli nie ma dopasowania, zwróć pusty JSON. Odpowiadaj w języku polskim. Format: {event_detected, recommended_product, nudge_header, nudge_body, estimated_price, call_to_action}"
    )

# --- INTERFEJS GŁÓWNY ---
st.title("ZEN.COM 🛡️")
st.subheader("Symulator Silnika Hyper-Nudge")
st.write("Wybierz transakcję klienta, aby zobaczyć magię AI w ubezpieczeniach.")

# Wybór transakcji
txn_options = [f"{t['id']} - {t['merchant']} ({t['amount']} {t['currency']})" for t in transactions]
selected_txn_label = st.selectbox("Wybierz transakcję do symulacji:", txn_options)
selected_txn = next(t for t in transactions if t["id"] in selected_txn_label)

if st.button("🚀 Symuluj zdarzenie (Nudge)"):
    if not api_key:
        st.error("Proszę wpisać API Key w panelu bocznym!")
    else:
        with st.spinner('AI analizuje kontekst ryzyka...'):
            try:
                # Wysłanie danych do Gemini
                response = model.generate_content(json.dumps(selected_txn))
                res_json = json.loads(response.text)

                if res_json and "nudge_header" in res_json:
                    # WYŚWIETLENIE POWIADOMIENIA
                    st.markdown(f"""
                        <div class="push-notification">
                            <div class="zen-logo">ZEN.COM • teraz</div>
                            <div class="nudge-header">{res_json['nudge_header']}</div>
                            <div class="nudge-body">{res_json['nudge_body']}</div>
                            <div style="font-size: 12px; color: #00ff88; margin-bottom: 10px;">
                                Estymowana składka: {res_json.get('estimated_price', 'n/a')}
                            </div>
                            <div class="nudge-cta">{res_json['call_to_action']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.success(f"Wykryto okazję: {res_json['event_detected']}")
                else:
                    st.info("Brak rekomendacji dla tej transakcji (brak istotnego ryzyka ubezpieczeniowego).")
            
            except Exception as e:
                st.error(f"Błąd silnika: {e}")

# --- STOPKA PREZENTACYJNA ---
st.divider()
st.caption("Demo przygotowane dla International Insurance Broker - Affinity Division")
