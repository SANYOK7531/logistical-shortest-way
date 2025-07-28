import os
import email
import xml.etree.ElementTree as ET
from email.header import decode_header
from email_connection import connect_to_mail

def decode_subject(subject_raw):
    decoded_fragments = decode_header(subject_raw)
    subject = ""
    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            subject += fragment.decode(encoding or "utf-8", errors="ignore")
        else:
            subject += fragment
    return subject.strip()

def fetch_xml_from_mail():
    print("📬 Підключення до пошти...")

    mail = connect_to_mail()

    status, messages = mail.search(None, 'UNSEEN')
    mail_ids = messages[0].split()
    print(f"📨 Непрочитані листи: {len(mail_ids)}")

    results = []

    for num in mail_ids:
        print(f"\n🔍 Перевіряю лист № {num.decode()}")
        _, msg_data = mail.fetch(num, "(RFC822)")
        message = email.message_from_bytes(msg_data[0][1])

        sender = email.utils.parseaddr(message["From"])[1]
        subject = decode_subject(message["Subject"] or "Без теми")
        print(f"➡️ Від: {sender}")
        print(f"📝 Тема: {subject}")

        for part in message.walk():
            filename = part.get_filename()
            maintype = part.get_content_maintype()

            if filename and filename.endswith(".xml"):
                print(f"📎 Знайдено вкладення: {filename} (тип: {maintype})")

                os.makedirs("temp", exist_ok=True)
                filepath = os.path.join("temp", filename)

                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))

                print(f"✅ Файл збережено: {filepath}")
                results.append((filepath, sender, subject))
                # break  # тільки один XML з листа

    mail.logout()

    if not results:
        print("📭 Завершено. Немає листів з XML-вкладенням.")
        return []

    return results

# def parse_xml(filepath):
#     tree = ET.parse(filepath)
#     root = tree.getroot()
#     locations = []

#     for loc in root.findall("Location"):
#         name = loc.find("Name").text
#         lat  = float(loc.find("Latitude").text)
#         lon  = float(loc.find("Longitude").text)
#         locations.append((name, lat, lon))

#     return locations

def parse_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    locations = []

    adresses = root.find("Adresses")

    for loc in adresses.findall("ROW"):
        name = loc.find("Cleint").text
        lat  = float(loc.find("Latitude").text)
        lon  = float(loc.find("Longitude").text)
        locations.append((name, lat, lon))

    return locations