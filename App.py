import customtkinter as ctk
import requests
from methods import *
from connection import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.configuracao_base()
        self.janela_login()

    def configuracao_base(self):
        self.title('Gerador Voucher')
        self.resizable(False, False)
        self.geometry('500x300')

    def janela_login(self):
        self.frame = ctk.CTkFrame(self, width=500, height=50, corner_radius=0, bg_color='teal', fg_color='#30A6D9')
        self.frame.place(x=0, y=10)
        ctk.CTkLabel(self.frame, text='Gerador de Voucher', font=('Century Gothic bold', 20),
                     text_color='#fff').place(x=165, y=12)
        self.frame_login = ctk.CTkFrame(self, width=500, height=200, corner_radius=0, bg_color='transparent',
                                        fg_color='transparent')
        self.frame_login.place(x=0, y=60)
        ctk.CTkLabel(self.frame_login, text='Login', font=('Century Gothic bold', 16)).place(x=230, y=5)
        login_entry = ctk.CTkEntry(self.frame_login)
        login_entry.place(x=180, y=35)
        ctk.CTkLabel(self.frame_login, text='Senha', font=('Century Gothic bold', 16)).place(x=230, y=75)
        senha_entry = ctk.CTkEntry(self.frame_login, show='*')
        senha_entry.place(x=180, y=105)
        validacao_login = ctk.CTkLabel(self.frame_login, text='', font=('Century Gothic bold', 16), text_color='red')
        validacao_login.place(x=160, y=135)

        def validar_usuario():
            user = login_entry.get()
            password = senha_entry.get()

            validacao = login(self.session, user, password)
            if validacao:
                self.janela_menu()
            else:
                validacao_login.configure(text=f'Problema ao realizar login')

        ctk.CTkButton(self.frame_login, text='LOGIN', command=validar_usuario, fg_color='#30A6D9', hover_color='#3071D9', font=('Century Gothic bold', 14)).place(x=180, y=170)

    def janela_menu(self):
        self.frame_login.destroy()
        self.frame.destroy()

        frame_menu = ctk.CTkFrame(self, width=150, height=300, bg_color='#D3DFEA',
                                        fg_color='#D3DFEA', border_width=1, border_color='black')
        frame_menu.place(x=0, y=0)
        botao_gerar = ctk.CTkButton(frame_menu, text='GERAR', command=self.janela_gerador, fg_color='#30A6D9',
                                    hover_color='#3071D9', font=('Century Gothic bold', 14), width=110)
        botao_gerar.place(x=20, y=80)
        botao_estender = ctk.CTkButton(frame_menu, text='ESTENDER', command=self.janela_extend, fg_color='#30A6D9',
                                    hover_color='#3071D9', font=('Century Gothic bold', 14), width=110)
        botao_estender.place(x=20, y=120)
        botao_apagar = ctk.CTkButton(frame_menu, text='APAGAR', command=self.janela_revoke, fg_color='#30A6D9',
                                       hover_color='#3071D9', font=('Century Gothic bold', 14), width=110)
        botao_apagar.place(x=20, y=160)

    def janela_gerador(self):
        try:
            self.frame_extend.destroy()
            self.frame_revoke.destroy()
        except:
            pass

        self.plan_var = ctk.BooleanVar()
        self.text_var = ctk.BooleanVar()

        self.frame_gerar = ctk.CTkFrame(self, width=350, height=300, corner_radius=5, bg_color='transparent',
                                        fg_color='transparent', border_width=1, border_color='black')
        self.frame_gerar.place(x=150, y=0)
        ctk.CTkLabel(self.frame_gerar, text='Dias', font=('Century Gothic bold', 16)).place(x=45, y=5)
        dias_entry = ctk.CTkEntry(self.frame_gerar, width=100)
        dias_entry.place(x=15, y=35)
        ctk.CTkLabel(self.frame_gerar, text='Quantidade', font=('Century Gothic bold', 16)).place(x=130, y=5)
        quant_entry = ctk.CTkEntry(self.frame_gerar, width=100)
        quant_entry.place(x=120, y=35)
        ctk.CTkLabel(self.frame_gerar, text='Setor', font=('Century Gothic bold', 16)).place(x=255, y=5)
        setor_entry = ctk.CTkEntry(self.frame_gerar, width=100)
        setor_entry.place(x=225, y=35)
        ctk.CTkLabel(self.frame_gerar, text='Dispositivo', font=('Century Gothic bold', 16)).place(x=60, y=75)
        dispo_entry = ctk.CTkEntry(self.frame_gerar, width=170)
        dispo_entry.place(x=15, y=105)
        ctk.CTkLabel(self.frame_gerar, text='Nome', font=('Century Gothic bold', 16)).place(x=240, y=75)
        nome_entry = ctk.CTkEntry(self.frame_gerar, width=130)
        nome_entry.place(x=195, y=105)
        validacao_gerador = ctk.CTkLabel(self.frame_gerar, text='', font=('Century Gothic bold', 16),
                                              text_color='red')
        validacao_gerador.place(x=100, y=135)
        criar_plan = ctk.CTkCheckBox(self.frame_gerar, text='Salvar na planilha', onvalue=True, offvalue=False,
                                          variable=self.plan_var, border_width=1)
        criar_plan.place(x=40, y=168)
        criar_txt = ctk.CTkCheckBox(self.frame_gerar, text='Criar TXT', onvalue=True, offvalue=False,
                                         variable=self.text_var, border_width=1)
        criar_txt.place(x=200, y=168)

        def gerar():
            dias = dias_entry.get()
            quant = quant_entry.get()
            dispo = dispo_entry.get()
            setor = setor_entry.get()
            nome = nome_entry.get()

            def planilha():
                salvar = salvar_planilha(vouchers_code, nome, setor, dispo, dias)
                if salvar:
                    planilha()

            if dias != '' and quant != '' and dispo != '' and nome != '':
                response, created_time = create_voucher(self.session, dias, quant, dispo, setor, nome)
                if response.status_code != 200:
                    validacao_gerador.configure(text=f'{response.text}')
                else:
                    vouchers_code = detalhes_voucher(self.session, created_time)
                    self.apresentar_vouchers(vouchers_code)
                    if self.plan_var.get():
                        planilha()
                    if self.text_var.get():
                        criar_txtfile(vouchers_code)

            else:
                validacao_gerador.configure(text='Todos campos são obrigatórios')

        botao_gerar = ctk.CTkButton(self.frame_gerar, text='GERAR', command=gerar, fg_color='#30A6D9', hover_color='#3071D9', font=('Century Gothic bold', 14), width=150)
        botao_gerar.place(x=100, y=210)

    def apresentar_vouchers(self, voucher_code):
        def copy_text(event):
            text = event.widget.cget("text")
            event.widget.focus_set()
            event.widget.clipboard_clear()
            event.widget.clipboard_append(text)

        def criar_label(frame, texto):
            label = ctk.CTkLabel(frame, text=texto)
            label.pack()
            label.configure(cursor="hand2")
            label.bind("<Button-1>", copy_text)

        def fechar_vouchers():
            self.frame_vouchers.destroy()

        self.frame_vouchers = ctk.CTkScrollableFrame(self, width=350, height=200, corner_radius=0,
                                                     bg_color='transparent', fg_color='transparent')
        self.frame_vouchers.place(x=150, y=10)
        for voucher in voucher_code:
            criar_label(self.frame_vouchers, voucher)

        ctk.CTkButton(self.frame_vouchers, text='FECHAR', command=fechar_vouchers,
                      fg_color='#30A6D9', hover_color='#3071D9', font=('Century Gothic bold', 14)).pack()

    def janela_extend(self):
        try:
            self.frame_gerar.destroy()
            self.frame_revoke.destroy()
        except:
            pass

        self.frame_extend = ctk.CTkFrame(self, width=350, height=300, corner_radius=5, bg_color='transparent',
                                        fg_color='transparent', border_width=1, border_color='black')
        self.frame_extend.place(x=150, y=0)
        ctk.CTkLabel(self.frame_extend, text='Dias', font=('Century Gothic bold', 16)).place(x=105, y=55)
        dias_entry = ctk.CTkEntry(self.frame_extend, width=100)
        dias_entry.place(x=75, y=80)
        ctk.CTkLabel(self.frame_extend, text='Code', font=('Century Gothic bold', 16)).place(x=210, y=55)
        code_entry = ctk.CTkEntry(self.frame_extend, width=100)
        code_entry.place(x=180, y=80)

        def extend():
            code = code_entry.get()
            dias = dias_entry.get()
            if code == "" or dias == "":
                tkinter.messagebox.showinfo('Erro', 'Todos os campos devem ser preenchidos')
            else:
                conn, cursor = bd()
                code = select_data(conn, cursor, code)
                extend_voucher(self.session, code, int(dias))

        botao_extend = ctk.CTkButton(self.frame_extend, text='Estender', command=extend, fg_color='#30A6D9',
                                    hover_color='#3071D9', font=('Century Gothic bold', 14), width=150)
        botao_extend.place(x=100, y=165)

    def janela_revoke(self):
        try:
            self.frame_gerar.destroy()
            self.frame_extend.destroy()
        except:
            pass

        self.frame_revoke = ctk.CTkFrame(self, width=350, height=300, corner_radius=5, bg_color='transparent',
                                        fg_color='transparent', border_width=1, border_color='black')
        self.frame_revoke.place(x=150, y=0)
        ctk.CTkLabel(self.frame_revoke, text='Code', font=('Century Gothic bold', 16)).place(x=155, y=55)
        code_entry = ctk.CTkEntry(self.frame_revoke, width=100)
        code_entry.place(x=125, y=80)

        def revoke():
            code = code_entry.get()
            if code == "":
                tkinter.messagebox.showinfo('Erro', 'Todos os campos devem ser preenchidos')
            else:
                conn, cursor = bd()
                code = select_data(conn, cursor, code)
                revoke_voucher(self.session, code)

        botao_extend = ctk.CTkButton(self.frame_revoke, text='Apagar', command=revoke, fg_color='#30A6D9',
                                     hover_color='#3071D9', font=('Century Gothic bold', 14), width=150)
        botao_extend.place(x=100, y=165)


if __name__ == '__main__':
    app = App()
    app.mainloop()
