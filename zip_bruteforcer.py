import zipfile
import zlib
import urllib.request

def bruteforce_zip_file(zip_file_path, max_number):
    found_passwords = []
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            max_length = len(str(max_number - 1))
            for i in range(max_number):
                passwords_to_try = [str(i), str(i).zfill(max_length)]
                for password_str in passwords_to_try:
                    password = password_str.encode()
                    try:
                        zf.extractall(pwd=password)
                        print(f"Passwort gefunden: {password.decode()}")
                        found_passwords.append(password.decode())
                    except (RuntimeError, zipfile.BadZipFile, zlib.error):
                        pass

            user_choice = input("Möchten Sie auch die Passwortliste durchsuchen? (ja/nein): ")
            if user_choice.lower() == 'ja':
                list_choice = input("Welche Passwortliste möchten Sie verwenden? (10k/100k/1M): ")
                if list_choice == '10k':
                    password_list_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt"
                elif list_choice == '100k':
                    password_list_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt"
                elif list_choice == '1M':
                    password_list_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"
                else:
                    print("Ungültige Auswahl. Keine Liste wird verwendet.")
                    return

                print("Versuche Passwortliste...")
                response = urllib.request.urlopen(password_list_url)
                passwords = response.read().decode('utf-8').splitlines()

                for password in passwords:
                    try:
                        zf.extractall(pwd=password.encode())
                        print(f"Passwort gefunden: {password}")
                        found_passwords.append(password)
                    except (RuntimeError, zipfile.BadZipFile, zlib.error):
                        pass

        if found_passwords:
            print("Gefundene Passwörter:")
            for pwd in found_passwords:
                print(pwd)
        else:
            print("Kein passendes Passwort gefunden.")
    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden.")

if __name__ == "__main__":
    zip_file_path = input("Bitte den Pfad zur ZIP-Datei eingeben: ")
    max_number = int(input("Bitte die maximale Zahl der Passwörter eingeben, die getestet werden sollen: "))

    bruteforce_zip_file(zip_file_path, max_number)