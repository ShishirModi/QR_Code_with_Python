import pyqrcode
import cv2
from pyzbar import pyzbar
import time

def qr_code_generate():
    print("What should the QR Code contain?")
    s = input("Input: ")
    txt = pyqrcode.create(s)
    def format():
        print("""Which format do you prefer the QR Code to be in?
        a) png
        b) svg
        Please respond in (a) or (b)""")
        choice = input("Your choice: ")
        
        file_name = input("Please enter file name for output: ")

        if 'a' in choice or 'A' in choice or 'png' in choice or 'PNG' in choice:
            txt.png(f"{file_name}.png", scale=8)

        elif 'b' in choice or 'B' in choice or 'svg' in choice or 'SVG' in choice:
            txt.svg(f"{file_name}.svg", scale=8)

        else:
            print("Invalid input")
            format()

    format()

def qr_code_read():
    def read_barcodes(frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            with open("barcode_result.txt", mode ='w') as file:
                file.write("Recognized Barcode:" + barcode_info)
        return frame

    def main():
        print("")
        print("The scanned result will be available in the same folder as this file with the name 'qrcode_result.txt'")
        print("If a green square/rectangle appears around the code, it has been scanned.")
        print("Exit the program by pressing 'Esc' or 'Escape' key.")
        print("")
        time.sleep(10)

        camera = cv2.VideoCapture(0)
        success, frame = camera.read()
        if not success:
            camera = cv2.VideoCapture(1)
            success, frame = camera.read()
            if not success:
                print("")
                print("There was a problem accessing your camera, please try again")
                print("Exiting now...")
                time.sleep(10)
                exit()

        ret, frame = camera.read()
        while ret:
            ret, frame = camera.read()
            frame = read_barcodes(frame)
            cv2.imshow('Barcode/QR code reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        camera.release()
        cv2.destroyAllWindows()
    if __name__ == '__main__':
        main()

def start():
    print("""Would you like to:
    a) Create a QR Code
    b) Read a QR code
    Please respond in (a) or (b)""")

    choice = input("Your choice: ")

    if 'a' in choice or 'A' in choice or 'create' in choice or 'CREATE' in choice:
        qr_code_generate()

    elif 'b' in choice or 'B' in choice or 'read' in choice or 'READ' in choice:
        qr_code_read()

    else:
        print("Invalid input")
        start()

start()
