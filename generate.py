import qrcode
from pathlib import Path

from qrcode.constants import ERROR_CORRECT_M


def generate_qr(url: str, output_path: str) -> Path:
    if not url:
        raise ValueError("URL cannot be empty.")
    p = Path(output_path).expanduser().resolve()
    p.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(p)
    return p


# --------------------------------------------------------------------
# Dummy main function for testing without a GUI
# --------------------------------------------------------------------
def main():
    print("=== QR Code Generator Test ===")
    url = input("Enter the URL to encode: ").strip()
    output_path = input("Enter output file path (e.g. sheet_qr.png): ").strip()

    if not output_path.lower().endswith(".png"):
        output_path += ".png"

    try:
        saved_path = generate_qr(url, output_path)
        print(f"✅ QR code successfully saved to: {saved_path}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
