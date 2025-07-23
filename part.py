def fetch_xml_from_mail(): 
    mail = imaplib.IMAP4_SSL(IMAP_SERVER) 
    mail.login(EMAIL_USER, EMAIL_PASS) 
    mail.select("inbox") 

    status, messages = mail.search(None, 'UNSEEN') 

    for num in messages[0].split(): 
        _, msg_data = mail.fetch(num, "(RFC822)") 
        message = email.message_from_bytes(msg_data[0][1]) 
        sender = email.utils.parseaddr(message["From"])[1] 
        subject = message["Subject"] or "Без теми" 
        
        for part in message.walk(): 
            if part.get_content_maintype() == 'application' and part.get_filename().endswith(".xml"): 
                os.makedirs("temp", exist_ok=True) 
                filepath = os.path.join("temp", part.get_filename()) 
                with open(filepath, "wb") as f: 
                    f.write(part.get_payload(decode=True)) 
                return filepath, sender, subject 
            
    return None, None, None 
        
def parse_xml(filepath): 
    tree = ET.parse(filepath) 
    root = tree.getroot() 
    locations = [] 
    for loc in root.findall("Location"): 
        name = loc.find("Name").text 
        lat = float(loc.find("Latitude").text) 
        lon = float(loc.find("Longitude").text) 
        locations.append((name, lat, lon)) 
        return locations