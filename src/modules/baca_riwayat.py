def history_to_txt(file_path, content):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\n' + content)
        print(f"String berhasil ditulis ke dalam file: {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        
def checking_to_txt(file_path, content):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\t' + content)
        print(f"String berhasil ditulis ke dalam file: {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def read_recent_sentences(file_path, max_sentences=8):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            recent_sentences = lines[-max_sentences:]
        return recent_sentences
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None
