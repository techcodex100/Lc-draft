import os
import time
import datetime
import requests
import psutil
from faker import Faker
from pydantic import BaseModel

fake = Faker()

# Output directory
pdf_output_dir = "rendered_lc_draft_pdfs"
os.makedirs(pdf_output_dir, exist_ok=True)

# Render API URL
RENDER_URL = "https://lc-draft.onrender.com/generate-lc-draft-pdf/"
MAX_RETRIES = 5
DELAY_BETWEEN_REQUESTS = 2  # seconds

class LCDraftData(BaseModel):
    document_credit_no: str
    date_of_issue: str
    applicant: str
    beneficiary: str
    currency_amount: str
    available_with: str
    drafts_at: str
    drawee: str
    partial_shipments: str
    transshipment: str
    port_of_loading: str
    port_of_discharge: str
    latest_shipment_date: str
    goods_description: str
    documents_required: str
    additional_conditions: str
    charges: str
    presentation_period: str
    confirmation: str
    negotiating_bank_instructions: str
    advise_through: str
    goods_quantity: str
    goods_price: str
    goods_incoterm: str

def generate_dummy_data():
    return LCDraftData(
        document_credit_no="LC-" + str(fake.random_number(digits=6)),
        date_of_issue=str(fake.date()),
        applicant=fake.company() + "\n" + fake.address(),
        beneficiary=fake.company() + "\n" + fake.address(),
        currency_amount=fake.currency_code() + " " + str(fake.random_int(min=10000, max=100000)),
        available_with=fake.company(),
        drafts_at="Sight",
        drawee=fake.company(),
        partial_shipments=fake.random_element(elements=("Allowed", "Not Allowed")),
        transshipment=fake.random_element(elements=("Allowed", "Not Allowed")),
        port_of_loading=fake.city(),
        port_of_discharge=fake.city(),
        latest_shipment_date=str(fake.date_between(start_date="today", end_date="+60d")),
        goods_description=fake.sentence(nb_words=10),
        documents_required="Commercial Invoice, Packing List, B/L",
        additional_conditions="Documents must be in English.",
        charges="All banking charges outside India are on beneficiary's account.",
        presentation_period="21 days after shipment",
        confirmation=fake.random_element(elements=("Without", "May Add", "Add")),
        negotiating_bank_instructions="Negotiate under reserve.",
        advise_through=fake.company(),
        goods_quantity=str(fake.random_int(min=1, max=1000)) + " units",
        goods_price=str(fake.random_int(min=100, max=10000)),
        goods_incoterm=fake.random_element(elements=("FOB", "CIF", "EXW", "DDP"))
    )

# Main loop
for i in range(1, 51):
    dummy_data = generate_dummy_data()
    start_time = time.time()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(RENDER_URL, json=dummy_data.model_dump())
            if response.status_code == 200:
                break
            else:
                print(f"⚠️ Attempt {attempt}: Failed to generate PDF {i} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ Exception: {e}")
        time.sleep(3)

    if response.status_code != 200:
        print(f"❌ Skipped PDF {i} after {MAX_RETRIES} retries.")
        continue

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = os.path.join(pdf_output_dir, f"lc_draft_{i}_{timestamp}.pdf")

    with open(pdf_filename, "wb") as pdf_file:
        pdf_file.write(response.content)

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    elapsed = round(time.time() - start_time, 2)

    print(f"✅ [{i}/50] PDF Generated: {pdf_filename}")
    print(f"   CPU Usage: {cpu}% | Memory: {mem}% | Time: {elapsed}s")
    print("-" * 50)

    time.sleep(DELAY_BETWEEN_REQUESTS)

print("🎉 All 50 LC Draft PDFs attempted with retry and delay logic.")
