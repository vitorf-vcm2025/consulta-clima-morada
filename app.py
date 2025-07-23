import customtkinter as ctk
import tkinter
import requests
import os
# Certifique-se de que a biblioteca Pillow está instalada: pip install Pillow
from PIL import Image, ImageTk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Chave de API (Cole a sua chave aqui!) ---
        self.API_KEY_CLIMA = "a718f4efe51aaf42af500e34c391f0e0"

        # --- Configuração da Janela ---
        self.title("Consulta de Clima e Morada")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(fg_color="#ECECEC")

        # --- ADICIONA O ÍCONE PERSONALIZADO (MÉTODO SIMPLIFICADO E PADRÃO) ---
        try:
            icon_path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
            else:
                print("AVISO: Ficheiro 'icon.ico' não encontrado na pasta do projeto.")
        except Exception as e:
            print(
                f"AVISO: Não foi possível carregar o ícone 'icon.ico'. Erro: {e}")

        # --- Frame Principal ---
        main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        main_frame.pack(padx=20, pady=20, expand=True, fill="both")

        # --- Título ---
        title_label = ctk.CTkLabel(main_frame, text="Consulta por CEP", font=ctk.CTkFont(
            size=24, weight="bold"), text_color="black")
        title_label.pack(pady=(20, 10))

        # --- Entrada do CEP ---
        cep_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cep_frame.pack(pady=10, padx=20, fill="x")

        self.cep_entry = ctk.CTkEntry(
            cep_frame, placeholder_text="Digite o CEP (só números)", width=200)
        self.cep_entry.pack(side="left", expand=True, fill="x", ipady=5)

        search_button = ctk.CTkButton(
            cep_frame, text="🔍 Pesquisar", width=100, command=self.buscar_informacoes)
        search_button.pack(side="left", padx=(10, 0))

        # --- Frame de Resultados ---
        results_frame = ctk.CTkFrame(
            main_frame, fg_color="#F0F0F0", corner_radius=10)
        results_frame.pack(pady=20, padx=20, expand=True, fill="both")

        # --- Resultados da Morada ---
        address_title = ctk.CTkLabel(results_frame, text="📍 Morada", font=ctk.CTkFont(
            size=16, weight="bold"), text_color="black")
        address_title.pack(pady=(10, 5), anchor="w", padx=15)

        self.logradouro_label = ctk.CTkLabel(
            results_frame, text="Logradouro: -", text_color="#333")
        self.logradouro_label.pack(anchor="w", padx=15)

        self.bairro_label = ctk.CTkLabel(
            results_frame, text="Bairro: -", text_color="#333")
        self.bairro_label.pack(anchor="w", padx=15)

        self.cidade_label = ctk.CTkLabel(
            results_frame, text="Cidade/UF: -", text_color="#333")
        self.cidade_label.pack(anchor="w", padx=15)

        # Divisor
        separator = ctk.CTkFrame(results_frame, height=1, fg_color="#D0D0D0")
        separator.pack(fill="x", padx=15, pady=10)

        # --- Resultados do Clima ---
        weather_title = ctk.CTkLabel(results_frame, text="☀️ Clima", font=ctk.CTkFont(
            size=16, weight="bold"), text_color="black")
        weather_title.pack(pady=(5, 5), anchor="w", padx=15)

        self.temperatura_label = ctk.CTkLabel(
            results_frame, text="Temperatura: -", text_color="#333")
        self.temperatura_label.pack(anchor="w", padx=15)

        self.descricao_label = ctk.CTkLabel(
            results_frame, text="Descrição: -", text_color="#333")
        self.descricao_label.pack(anchor="w", padx=15)

        # --- NOVA BARRA DE ESTADO ---
        self.status_bar = ctk.CTkLabel(
            self, text="A iniciar...", text_color="gray", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=(0, 5))
        self.status_bar.configure(text="Pronto.")

    def buscar_informacoes(self):
        cep = self.cep_entry.get().strip()

        if len(cep) != 8 or not cep.isdigit():
            self.logradouro_label.configure(text="Logradouro: CEP inválido!")
            self.bairro_label.configure(text="Bairro: -")
            self.cidade_label.configure(text="Cidade/UF: -")
            self.temperatura_label.configure(text="Temperatura: -")
            self.descricao_label.configure(text="Descrição: -")
            self.status_bar.configure(
                text="Por favor, insira um CEP válido.", text_color="orange")
            return

        self.status_bar.configure(text="A pesquisar CEP...", text_color="blue")
        try:
            url_cep = f"https://viacep.com.br/ws/{cep}/json/"
            response_cep = requests.get(url_cep, timeout=5)

            if response_cep.status_code == 200:
                dados_cep = response_cep.json()
                if "erro" not in dados_cep:
                    cidade = dados_cep.get("localidade", "-")
                    self.logradouro_label.configure(
                        text=f"Logradouro: {dados_cep.get('logradouro', '-')}")
                    self.bairro_label.configure(
                        text=f"Bairro: {dados_cep.get('bairro', '-')}")
                    self.cidade_label.configure(
                        text=f"Cidade/UF: {cidade}/{dados_cep.get('uf', '-')}")
                    self.buscar_clima(cidade)
                else:
                    self.logradouro_label.configure(
                        text="Logradouro: CEP não encontrado.")
                    self.status_bar.configure(
                        text="CEP não encontrado.", text_color="orange")
            else:
                self.logradouro_label.configure(
                    text="Logradouro: Erro na consulta de CEP.")
                self.status_bar.configure(
                    text="Erro na consulta de CEP.", text_color="red")
        except requests.exceptions.RequestException:
            self.logradouro_label.configure(
                text="Logradouro: Sem ligação à internet.")
            self.status_bar.configure(
                text="Erro de rede. Verifique a sua ligação.", text_color="red")

    def buscar_clima(self, cidade):
        self.status_bar.configure(
            text="A pesquisar clima...", text_color="blue")
        if self.API_KEY_CLIMA == "SUA_CHAVE_DE_API_AQUI" or self.API_KEY_CLIMA == "":
            self.temperatura_label.configure(
                text="Temperatura: Chave de API em falta.")
            self.descricao_label.configure(text="Descrição: -")
            self.status_bar.configure(
                text="Chave de API em falta no código.", text_color="red")
            return

        url_clima = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={self.API_KEY_CLIMA}&units=metric&lang=pt_br"

        try:
            response_clima = requests.get(url_clima, timeout=5)

            if response_clima.status_code == 200:
                dados_clima = response_clima.json()
                temperatura = dados_clima['main']['temp']
                descricao = dados_clima['weather'][0]['description'].capitalize(
                )
                self.temperatura_label.configure(
                    text=f"Temperatura: {temperatura:.1f}°C")
                self.descricao_label.configure(text=f"Descrição: {descricao}")
                self.status_bar.configure(
                    text="Pesquisa concluída com sucesso!", text_color="green")
            elif response_clima.status_code == 401:
                self.temperatura_label.configure(
                    text="Temperatura: Chave de API inválida.")
                self.descricao_label.configure(
                    text="Descrição: (Aguarde a ativação)")
                self.status_bar.configure(
                    text="Chave de API inválida ou inativa.", text_color="red")
            elif response_clima.status_code == 404:
                self.temperatura_label.configure(
                    text="Temperatura: Cidade não encontrada.")
                self.descricao_label.configure(text="Descrição: -")
                self.status_bar.configure(
                    text="Não foi possível encontrar o clima para esta cidade.", text_color="orange")
            else:
                self.temperatura_label.configure(
                    text=f"Temperatura: Erro ({response_clima.status_code})")
                self.descricao_label.configure(text="Descrição: -")
                self.status_bar.configure(
                    text=f"Erro na API de clima: {response_clima.status_code}", text_color="red")

        except requests.exceptions.RequestException:
            self.temperatura_label.configure(
                text="Temperatura: Sem ligação à internet.")
            self.descricao_label.configure(text="Descrição: -")
            self.status_bar.configure(
                text="Erro de rede. Verifique a sua ligação.", text_color="red")


# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = App()
    app.mainloop()
