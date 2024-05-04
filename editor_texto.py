import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename


class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        # Ventana
        self.title('Editor de Texto')
        self.iconbitmap('editor.ico')
        self.rowconfigure(0, minsize=600, weight=1)  # Configuración tamaño mínimo de la ventana
        self.columnconfigure(1, minsize=600, weight=1)  # Configuración mínima de la segunda columna

        # Campo de texto
        self.archivo = None
        self.archivo_abierto = False  # Saber si ya se abrió un archivo anteriormente

        # Métodos de instancia
        self._crear_componentes()
        self._crear_menu()

    def _crear_componentes(self):

        # Frame de botones
        frame_botones = tk.Frame(self, relief=tk.RAISED, bd=2)
        frame_botones.grid(row=0, column=0, sticky='NS')  # NS: expandir frame de manera vertical

        # Botones
        boton_abrir = tk.Button(frame_botones, text='Abrir', command=self._abrir_archivo)
        boton_abrir.grid(row=0, column=0, sticky='WE', padx=5, pady=5)  # WE: expandir botones de manera horizontal

        boton_guardar = tk.Button(frame_botones, text='Guardar', command=self._guardar)
        boton_guardar.grid(row=1, column=0, sticky='WE', padx=5, pady=5)

        boton_guardar_como = tk.Button(frame_botones, text='Guardar como...', command=self._guardar_como)
        boton_guardar_como.grid(row=2, column=0, sticky='WE', padx=5, pady=5)

        # Campo de texto
        self.campo_texto = tk.Text(self, wrap=tk.WORD)  # Crear campo de texto
        self.campo_texto.grid(row=0, column=1, sticky='NSWE')  # NSWE: expandir completamente

    def _crear_menu(self):
        menu_app = tk.Menu(self)
        self.config(menu=menu_app)  # Agregar menú a la ventana

        # Submenú archivo
        menu_archivo = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Archivo', menu=menu_archivo)  # Agregar submenú al menú de la aplicación

        # Agregar opciones al submenú
        menu_archivo.add_command(label='Abrir', command=self._abrir_archivo)
        menu_archivo.add_command(label='Guardar', command=self._guardar)
        menu_archivo.add_command(label='Guardar como...', command=self._guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Salir', command=self.quit)

    def _abrir_archivo(self):
        self.archivo_abierto = askopenfile(mode='r+')  # Abrir archivo para edición
        self.campo_texto.delete(1.0, tk.END)  # Borrar el contenido al momento de abrir archivo
        # index 1.0: primer línea y primer caracter o columna
        if not self.archivo_abierto:  # Revisar si hay un archivo abierto
            return

        # Abrir el archivo en modo lectura/escritura como un recurso
        with open(self.archivo_abierto.name, 'r+') as self.archivo:
            texto = self.archivo.read()  # Leer contenido del archivo
            self.campo_texto.insert(1.0, texto)  # Insertar contenido del archivo en el campo de texto
            self.title(f'*Editor texto - {self.archivo.name}')  # Modificar título de la aplicación

    def _guardar(self):
        if self.archivo_abierto:  # Revisar si ya se abrió previamente un archivo, se sobrescribe
            with open(self.archivo_abierto.name, 'w') as self.archivo:  # Guardar archivo (abrirlo en modo escritura)
                texto = self.campo_texto.get(1.0, tk.END)  # Leer contenido de la caja de texto
                self.archivo.write(texto)  # Escribir el contenido al mismo archivo
                self.title(f'Editor Texto - {self.archivo.name}')  # Modificar título de la aplicación
        else:
            self._guardar_como()

    def _guardar_como(self):
        self.archivo = asksaveasfilename(  # Salvar archivo actual como un nuevo archivo
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
        )
        if not self.archivo:
            return
        with open(self.archivo, 'w') as self.archivo:  # Abrir archivo en modo escritura
            texto = self.campo_texto.get(1.0, tk.END)  # Leer contenido de la caja de texto
            self.archivo.write(texto)  # Escribir el contenido al nuevo archivo
            self.title(f'Editor Texto - {self.archivo.name}')  # Modificar título de la aplicación
            self.archivo_abierto = self.archivo  # Indicar que ya hemos abierto un archivo


if __name__ == '__main__':
    editor = Editor()
    editor.mainloop()
