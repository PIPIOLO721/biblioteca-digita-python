import tkinter as tk
from tkinter import messagebox, scrolledtext
from base_de_datos import Biblioteca  

_original_Tk = tk.Tk
class FullscreenTk(_original_Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fullscreen_active = True
        self.attributes("-fullscreen", True)
        
        self.bind("<Escape>", self._toggle_fullscreen)

    def _toggle_fullscreen(self, event=None):
        self._fullscreen_active = not self._fullscreen_active
        self.attributes("-fullscreen", self._fullscreen_active)

    def geometry(self, newGeometry=None):
        
        if newGeometry is None:
            return super().geometry()
        if self._fullscreen_active:
            return
        return super().geometry(newGeometry)

tk.Tk = FullscreenTk
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class BibliotecaGUI:
    def __init__(self, root): 
        self.root = root
        self.root.title("Biblioteca")
        self.biblioteca = Biblioteca()

       
        self.right_panel = tk.Frame(root, width=WINDOW_WIDTH // 2, bg="#4A5240", bd=2, relief="sunken")
        self.right_panel.pack(side="right", fill="both", expand=True)

        tk.Label(root, text="BIBLIOTECA", font=("Montserrat", 22, "bold")).pack(pady=8)

        btn_frame = tk.Frame(root)
        btn_frame.pack(
            padx=10, 
            pady=10, 
            anchor="w"    
        ) 

        botones = [
            ("Registrar libro 📚", self.registrar_libro),
            ("Registrar usuario 👤", self.registrar_usuario),
            ("Ver libros disponibles 📖", self.mostrar_libros),
            ("Prestar libro 📘", self.prestar_libro),
            ("Devolver libro 🔄", self.devolver_libro),
            ("Ver lista de libros prestados 📝", self.mostrar_prestados),
            ("Ver lista de usuarios registrados 🧑‍🤝‍🧑", self.mostrar_usuarios),
            ("Salir ❌", root.quit),
    
        ]
       
        for (txt, cmd) in botones:
            tk.Button(
                btn_frame,
                text=txt,
                width=35,
                height=1,
                font=("Montserrat", 12),
                command=cmd,
                activebackground= "#28721D",
                bg="#3E8034",
                cursor="hand2", 
            ).pack(pady=10 , anchor="w")  
   
        
        

    def registrar_libro(self):

        fields = [
            ("Título:", "titulo", str),
            ("Autor:", "autor", str),
        ]

        def on_submit(values):
            titulo = values.get("titulo")
            autor = values.get("autor")
            if not titulo:
                messagebox.showerror("Error", "El título es obligatorio.", parent=self.root)
                return
            if autor is None:
                autor = ""
            try:
                res = self.biblioteca.registrar_libro(titulo, autor)
                messagebox.showinfo(res, f"Libro '{titulo}' registrado.")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)

        self._open_form_in_right_panel("Registrar libro", fields, on_submit)

    def registrar_usuario(self):
       
        fields = [
            ("Nombre:", "nombre", str),
            ("CC (número):", "cc", int),
        ]

        def on_submit(values):
            nombre = values.get("nombre")
            cc = values.get("cc")
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.", parent=self.root)
                return
            if cc is None:
                messagebox.showerror("Error", "La CC es obligatoria y debe ser numérica.", parent=self.root)
                return
            try:
                res = self.biblioteca.registrar_usuario(nombre, cc)
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado.", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)

        self._open_form_in_right_panel("Registrar usuario", fields, on_submit)

    def mostrar_libros(self):
        try:
            res = self.biblioteca.mostrar_libros()
            self._display_return_or_attr(res, ("libros", "books"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def prestar_libro(self):
       
        fields = [
            ("CC del usuario:", "cc", int),
            ("Título del libro:", "titulo", str),
        ]

        def on_submit(values):
            cc = values.get("cc")
            titulo = values.get("titulo")
            if cc is None:
                messagebox.showerror("Error", "La CC es obligatoria y debe ser numérica.", parent=self.root)
                return
            if not titulo:
                messagebox.showerror("Error", "El título es obligatorio.", parent=self.root)
                return
            try:
                res = self.biblioteca.prestar_libro(cc, titulo)
                messagebox.showinfo(res, f"Prestar libro '{titulo}' al CC {cc}.")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)

        self._open_form_in_right_panel("Prestar libro", fields, on_submit)

    def devolver_libro(self):
       
        fields = [
            ("CC del usuario:", "cc", int),
            ("Título del libro:", "titulo", str),
        ]

        def on_submit(values):
            cc = values.get("cc")
            titulo = values.get("titulo")
            if cc is None:
                messagebox.showerror("Error", "La CC es obligatoria y debe ser numérica.", parent=self.root)
                return
            if not titulo:
                messagebox.showerror("Error", "El título es obligatorio.", parent=self.root)
                return
            try:
                res = self.biblioteca.devolver_libro(cc, titulo)
                self._show_result(res, f"Devolver libro '{titulo}' del CC {cc}.")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)

        self._open_form_in_right_panel("Devolver libro", fields, on_submit)

    def mostrar_prestados(self):
        try:
            res = None
            if hasattr(self.biblioteca, "mostrar_usuarios_prestados"):
                res = self.biblioteca.mostrar_usuarios_prestados()
            else:
                res = getattr(self.biblioteca, "prestamos", None) or getattr(self.biblioteca, "prestados", None)
            self._display_return_or_attr(res, ("prestamos", "prestados"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_usuarios(self):
        try:
            res = None
            if hasattr(self.biblioteca, "mostrar_usuarios"):
                res = self.biblioteca.mostrar_usuarios()
            else:
                res = getattr(self.biblioteca, "usuarios", None) or getattr(self.biblioteca, "users", None)
            self._display_return_or_attr(res, ("usuarios", "users"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

   
    def _show_result(self, res, default_msg):
        if isinstance(res, (list, tuple, set)):
            self._open_right_panel("Resultado", "\n".join(map(str, res)))
        elif isinstance(res, str):
            self._open_right_panel("Resultado", res)
        elif res is None:
            self._open_right_panel("Resultado", default_msg)
        else:
            self._open_right_panel("Resultado", str(res))

    def _display_return_or_attr(self, res, attr_names):
        if isinstance(res, str):
            self._open_right_panel("Listado", res)
            return
        if isinstance(res, (list, tuple, set)) and res:
            self._open_right_panel("Listado", "\n".join(map(str, res)))
            return

        items = []
        for name in attr_names:
            if hasattr(self.biblioteca, name):
                col = getattr(self.biblioteca, name)
                if isinstance(col, (list, tuple, set)):
                    items = list(col)
                    break
        if not items:
            for name in ("libros", "usuarios", "prestamos", "prestados", "books", "users"):
                if hasattr(self.biblioteca, name):
                    col = getattr(self.biblioteca, name)
                    if isinstance(col, (list, tuple, set)):
                        items = list(col)
                        break

        if items:
            self._open_right_panel("Listado", "\n".join(map(str, items)))
        else:
            self._open_right_panel("Listado", "No hay elementos para mostrar o el método devolvió None.")

    def _open_right_panel(self, title, text):
      
        for w in self.right_panel.winfo_children():
            w.destroy()

       
        header = tk.Label(self.right_panel, text=title, font=("Montserrat", 16, "bold"), bg=self.right_panel['bg'])
        header.pack(pady=8)

      
        txt = scrolledtext.ScrolledText(self.right_panel)
        txt.pack(fill="both", expand=True, padx=10, pady=5)
        txt.insert("1.0", text)
        txt.config(state="disabled")

        
        btn_frame = tk.Frame(self.right_panel, bg=self.right_panel['bg'])
        btn_frame.pack(pady=8)
        volver_btn = tk.Button(
            btn_frame, 
            text="Cerrar", 
            width=16, 
            height=2, 
            font=("Arial", 12),
                               command=lambda: [w.destroy() for w in self.right_panel.winfo_children()],
                               bg="#3E8034", activebackground="#28721D", cursor="hand2")
        volver_btn.pack()

    def _open_form_in_right_panel(self, title, fields, submit_callback):
        """
        fields: list of tuples (label_text, key, type) where type is str or int
        submit_callback: function(values_dict) called on submit; values already converted or None for empty
        """
       
        for w in self.right_panel.winfo_children():
            w.destroy()

        header = tk.Label(self.right_panel, 
                          text=title, 
                          font=("Montserrat", 16, "bold"), 
                          bg=self.right_panel['bg'])
        header.pack(pady=8)

        form_frame = tk.Frame(self.right_panel, bg=self.right_panel['bg'])
        form_frame.pack(fill="both", expand=True, padx=10, pady=5)

        entries = {}
        for (lbl_text, key, typ) in fields:
            lbl = tk.Label(form_frame, text=lbl_text, anchor="w", bg=self.right_panel['bg'], font=("Montserrat", 12))
            lbl.pack(fill="x", pady=(6, 0))
            ent = tk.Entry(form_frame)
            ent.pack(fill="x", pady=(0, 6))
            entries[key] = (ent, typ)

        btn_frame = tk.Frame(self.right_panel, bg=self.right_panel['bg'])
        btn_frame.pack(pady=8)

        def do_submit():
            values = {}
            for key, (ent, typ) in entries.items():
                raw = ent.get().strip()
                if raw == "":
                    val = None
                else:
                    if typ is int:
                        try:
                            val = int(raw)
                        except ValueError:
                            messagebox.showerror("Error", f"El campo '{key}' debe ser numérico.", parent=self.root)
                            return
                    else:
                        val = raw
                values[key] = val
            submit_callback(values)

        submit_btn = tk.Button(btn_frame, text="Enviar", width=12, height=2, font=("Arial", 12),
                               command=do_submit, bg="#3E8034", activebackground="#28721D", cursor="hand2")
        submit_btn.pack(side="left", padx=6)

        cancelar_btn = tk.Button(btn_frame, text="Cancelar", width=12, height=2, font=("Arial", 12),
                                 command=lambda: [w.destroy() for w in self.right_panel.winfo_children()],
                                 bg="#3E8034", activebackground="#28721D", cursor="hand2")
        cancelar_btn.pack(side="left", padx=6)

    
    def _open_text_window(self, title, text):
        win = tk.Toplevel(self.root)
        win.title(title)
        
        win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - WINDOW_WIDTH) // 2
        y = (sh - WINDOW_HEIGHT) // 2
        win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        txt = scrolledtext.ScrolledText(win)
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", text)
        txt.config(state="disabled")

    
        btn_frame = tk.Frame(win)
        btn_frame.pack(side="bottom", pady=10)
        volver_btn = tk.Button(btn_frame, text="Volver", width=16, height=2, font=("Arial", 12), command=win.destroy)
        volver_btn.pack()

if __name__ == "__main__":
    root = tk.Tk()

  
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - WINDOW_WIDTH) // 2
    y = (sh - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    

    valid_credentials = {"keyner lozano": "1109381992",
                         "Esteban Perea" : "1107835902", 
                         "Marlon Solis": "1107835973"}

    class LoginFrame(tk.Frame):
        def __init__(self, parent, on_success):
            super().__init__(parent)
            self.parent = parent
            self.on_success = on_success

          

            self.config(padx=200, pady=50, bg="#4A5240")
            title = tk.Label(
                self,
                text="LOGIN",
                font=("Montserrat", 18, "bold"),
                bg="#4A5240",
)

            title.pack(pady=(0,10))

            lbl_user = tk.Label(
                self,
                font="Montserrat",
                text="Usuario:",
                bg="#4A5240")

            lbl_user.pack(anchor="w")
            self.usuario_entry = tk.Entry(self)
            self.usuario_entry.pack(
                fill="x",
                pady=(0,8))

            lbl_pass = tk.Label(
                self,
                font="Montserrat",
                text="Contraseña:",
                bg="#4A5240")

            lbl_pass.pack(anchor="w")
            self.password_entry = tk.Entry(self, show="*")
            self.password_entry.pack(
                fill="x",
                pady=(0,12))

            btn_frame = tk.Frame(self, bg="#4A5240")
            btn_frame.pack()
            login_btn = tk.Button(
                btn_frame,
                font="Montserrat",
                text="Ingresar",
                width=12,
                activebackground="#28721D",
                bg="#3E8034",
                cursor="hand2",
                command=self.try_login)
            login_btn.pack(side="left", padx=5)

            cancel_btn = tk.Button(
                btn_frame,
                font="Montserrat",
                text="Salir",
                width=12,
                activebackground="#28721D",
                bg="#3E8034",
                cursor="hand2",
                command=parent.quit)
            cancel_btn.pack(side="left", padx=5)

            self.usuario_entry.focus_set()

        def try_login(self):
            usuario = self.usuario_entry.get()
            contrasena = self.password_entry.get()
            if valid_credentials.get(usuario) == contrasena:
                self.destroy()
                self.on_success()
            else:
                messagebox.showerror("Login fallido", "Usuario o contraseña incorrectos.", parent=self.parent)
                self.password_entry.delete(0, tk.END)

    def start_app():
       
        BibliotecaGUI(root)

    
    login_frame = LoginFrame(root, start_app)
    login_frame.place(
        relx=0.5, 
        rely=0.5, 
        anchor="center")

    root.mainloop()
    