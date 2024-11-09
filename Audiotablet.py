
import qrcode 
from gtts import gTTS 
from http.server import HTTPServer, SimpleHTTPRequestHandler 
import threading 
import os 
import webbrowser 
import time

def get_tablet_details():
    print("Gathering tablet details...")
    details = {
        "Name": input("Enter tablet name: "),
        "Dosage": input("Enter dosage (e.g., 500mg): "),
        "Frequency": input("Enter frequency (e.g., twice a day): "),
        "Manufacturer": input("Enter manufacturer name: "),
        "Expiry Date": input("Enter expiry date (YYYY-MM-DD): "),
        "Instructions": input("Enter any special instructions: "),
    }
    print("Tablet details gathered.")
    return "\n".join([f"{key}: {value}" for key, value in details.items()])

def generate_audio(text, filename="tablet_info.mp3"):
    print("Generating audio file...")
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    print(f"Audio saved as '{filename}'.")

def generate_qr_code(url, filename="tablet_audio_qr_code.png"):
    print("Generating QR code...")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)
    img.show()
    print(f"QR code generated and saved as '{filename}'")

def start_local_server(port=8000):
    print("Starting local server...")
    os.chdir(os.path.dirname(__file__))
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    print("Local server started.")
    return f"http://localhost:{port}/tablet_info.mp3"

if __name__ == "__main__":
    print("Program started.")
    tablet_details = get_tablet_details()
    audio_filename = "tablet_info.mp3"
    generate_audio(tablet_details, audio_filename)
    audio_url = start_local_server()
    time.sleep(2)
    webbrowser.open(audio_url)
    generate_qr_code(audio_url)
    print("Program finished. Scan the QR code to play the audio.")
