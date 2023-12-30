import streamlit as st
import re
from modules.baca_riwayat import history_to_txt, read_recent_sentences, checking_to_txt
from modules.cyk_algorithm import is_accepted, get_parse_tree, get_table_element
from modules.cnf_algorithm import get_raw_set_of_production

history = []
semua_kata = []

def main():
    with open('style.css', 'r') as css_file:
        # Membaca seluruh isi file dan menyertakannya sebagai CSS
        custom_css = f"<style>{css_file.read()}</style>"
        # Menambahkan CSS ke tampilan Streamlit
        st.markdown(custom_css, unsafe_allow_html=True)
    
    with st.container():
        # Menampilkan gambar dengan path absolut
        st.image("public/header.png", caption="", use_column_width=True)
        
        global history
        
        kalimat = st.text_input("Masukan Kalimat Bahasa Indonesia Yang Ingin Diuji")

        # Mengecek apakah tombol login ditekan
        if st.button("Cek Sekarang!"):
            if not kalimat:
                st.warning("Masukkan kalimat terlebih dahulu.")
            else:
                history = kalimat
                history_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-pencarian.txt", history)
                semua_alphabet = get_raw_set_of_production()
                global semua_kata
                semua_kata = []
                for key, value in semua_alphabet.items():
                    if key not in ["K", "S", "P", "O", "Pel", "Ket", "NP", "VP", "AdjP", "PP"]:
                        for val in value:
                            semua_kata.append(val)

                cek_kalimat = re.sub(r'\s+', ' ', kalimat).strip()
                cek_kata = cek_kalimat.split()
                tidak_ketemu = 0
                kata_tidak_ketemu = []

                for kata in cek_kata:
                    if kata not in semua_kata:
                        tidak_ketemu = 1
                        kata_tidak_ketemu.append(kata)

                if tidak_ketemu == 1:
                    checking_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-pencarian.txt", "(Ada Kata Yang Tidak Ditemukan)")
                    history_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-tercheck.txt", "Unknown")
                    kata = ', '.join(kata_tidak_ketemu)
                    st.error(f"{kata} tidak ditemukan!")
                elif is_accepted(cek_kalimat):
                    checking_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-pencarian.txt", "(Sudah Baku)")
                    history_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-tercheck.txt", "True")
                    st.success("Kalimat Baku. Sudah Sesuai Dengan Kaidah Bahasa Indonesia")
                    st.subheader("Konstruksi Triangular Table:")
                    triangular_table =  get_table_element(cek_kalimat)
                    st.table(triangular_table)
                
                    # Menampilkan parse tree jika diterima
                    parse_tree = get_parse_tree(cek_kalimat)
                    if parse_tree:
                        st.subheader("Pohon Parsing:")
                        st.graphviz_chart(parse_tree.source)
                else:
                    checking_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-pencarian.txt", "(Tidak Baku)")
                    history_to_txt("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-tercheck.txt", "False")
                    st.error("Kalimat Tidak Baku. Tidak Sesuai Dengan Kaidah Bahasa Indonesia")
                    st.subheader("Konstruksi Triangular Table:")
                    triangular_table =  get_table_element(cek_kalimat)
                    st.table(triangular_table)
                
                    
    with st.expander("Riwayat Pengecekan"):
        st.write("ini merupakan riwayat pengecekan kalimat anda")
        read_history = read_recent_sentences("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-pencarian.txt")
        read_checked = read_recent_sentences("c:/Users/gus ryan/iDev/Project-Parsing-TBO/src/modules/riwayat-tercheck.txt")
        min_length = min(len(read_history), len(read_checked))
        
        for i in range(min_length):
            if read_checked[i] == "True":
                st.success(read_history[i])
            elif read_checked[i] == "False":
                st.error(read_history[i])
            else:
                st.success(read_history[i])
        
if __name__ == "__main__":
    main()