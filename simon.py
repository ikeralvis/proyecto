import os
import serial
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

# Configuración de las rutas de Tcl y Tk
os.environ['TCL_LIBRARY'] = r'C:\Users\Usuario\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Usuario\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

class SimonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego Simon")
        self.setup_serial()
        self.setup_styles()
        self.create_gui()

    def setup_styles(self):
        # Crear fuente personalizada para el botón
        self.button_font = tkfont.Font(
            family="Helvetica",
            size=16,
            weight="bold"
        )

        # Crear un estilo personalizado para el botón de inicio
        self.style = ttk.Style()
        self.style.configure(
            'Start.TButton',
            font=self.button_font,
            padding=(20, 10),
            background='#4C1950',
            foreground='white'
        )

        # Configurar los estados del botón
        self.style.map('Start.TButton',
            background=[('active', '#45a049'), ('pressed', '#3d8b40')],
            relief=[('pressed', 'sunken')]
        )

    def setup_serial(self):
        self.port = "COM5"
        self.baud_rate = 115200
        self.ser = None
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Conectado a {self.port} a {self.baud_rate} baudios.")
        except serial.SerialException as e:
            print(f"Error al conectar al puerto serial: {e}")

    def create_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        

        # Etiqueta de bienvenida
        self.label = ttk.Label(
            main_frame, 
            text="Bienvenido al juego de Simon, dale al botón para empezar y comenzar con el juego. ¡Buena suerte!",
            wraplength=500,
            font=("Helvetica", 14)
        )
        self.label.grid(row=0, column=0, pady=15, columnspan=3)

        # Como funciona el juego
        self.label = ttk.Label(
            main_frame, 
            text="El juego Simón con dos botones funciona mostrando una secuencia de luces en dos LEDs, una tras otra, que el jugador debe replicar presionando el botón correspondiente al LED encendido. La partida comienza con una secuencia aleatoria de cinco pulsos. El jugador tiene que seguirla en orden y cada acierto suma puntos según el número de pulsaciones correctas consecutivas: 5 puntos si completa la secuencia, 4 si acierta las primeras cuatro, y así sucesivamente.",
            wraplength=500,
            font=("Helvetica", 10)
        )
        self.label.grid(row=2, column=0, pady=20)

       # Frame para el botón de inicio (para centrado y efectos)
        start_frame = tk.Frame(main_frame, bg='#f0f0f0')
        start_frame.grid(row=1, column=0, columnspan=3, pady=20)

        # Botón de inicio personalizado
        self.start_button = tk.Button(
            start_frame,
            text="EMPEZAR JUEGO",
            font=self.button_font,
            command=self.iniciar_juego_con_efecto,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.RAISED,
            bd=3,
            padx=30,
            pady=15,
            cursor='hand2'  # Cambia el cursor al pasar por encima
        )
        self.start_button.grid(row=0, column=0, padx=20)

        # Configurar efectos hover
        self.start_button.bind('<Enter>', self.on_enter)
        self.start_button.bind('<Leave>', self.on_leave)
        self.start_button.bind('<Button-1>', self.on_click)

        # Entrada para comandos UART
        self.uart_frame = ttk.LabelFrame(main_frame, text="Control Debug Botones", padding="10")
        self.uart_frame.grid(row=3, column=0, pady=20, sticky=(tk.W, tk.E))

        self.uart_entry = ttk.Entry(self.uart_frame)
        self.uart_entry.grid(row=0, column=0, padx=5)

        self.send_button = ttk.Button(
            self.uart_frame,
            text="Enviar",
            command=self.enviar_comando
        )
        self.send_button.grid(row=0, column=1, padx=5)

        # Frame para agrupar los botones LED
        self.led_frame = ttk.LabelFrame(main_frame, text="Control de LEDs", padding="10")
        self.led_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        self.led_frame.grid_columnconfigure(0, weight=1)
        self.led_frame.grid_columnconfigure(1, weight=1)
        self.led_frame.grid_columnconfigure(2, weight=1)

        # Botones LED en el frame agrupado
        self.led_button = ttk.Button(
            self.led_frame,
            text="LED 1",
            command=lambda: self.enviar_uart("LED1")
        )
        self.led_button.grid(row=0, column=0, padx=5, pady=5)

        self.led2_button = ttk.Button(
            self.led_frame,
            text="LED 2",
            command=lambda: self.enviar_uart("LED2")
        )
        self.led2_button.grid(row=0, column=1, padx=5, pady=5)

        self.led3_button = ttk.Button(
            self.led_frame,
            text="LED 3",
            command=lambda: self.enviar_uart("LED3")
        )
        self.led3_button.grid(row=0, column=2, padx=5, pady=5)


    def enviar_uart(self, comando):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(comando.encode('utf-8'))
                print(f"Enviado: {comando}")
            except Exception as e:
                print(f"Error al enviar: {e}")
        else:
            print("Puerto serial no disponible")

    def enviar_comando(self):
        comando = self.uart_entry.get()
        if comando:
            self.enviar_uart(comando)
            self.uart_entry.delete(0, tk.END)

    def on_enter(self, event):
        """Efecto al pasar el mouse por encima"""
        self.start_button.config(bg='#45a049')

    def on_leave(self, event):
        """Efecto al retirar el mouse"""
        self.start_button.config(bg='#4CAF50')

    def on_click(self, event):
        """Efecto al hacer clic"""
        self.start_button.config(relief=tk.SUNKEN)
        self.root.after(100, lambda: self.start_button.config(relief=tk.RAISED))

    def iniciar_juego_con_efecto(self):
        """Inicia el juego con efecto visual"""
        # Efecto de "flash" al iniciar
        original_color = self.start_button.cget('bg')
        self.start_button.config(bg='white')
        self.root.after(100, lambda: self.start_button.config(bg=original_color))
        self.iniciar_juego()

    def iniciar_juego(self):
        print("Juego empezado")
        self.enviar_uart("STRT")  # Envía START al iniciar el juego

    def cerrar_aplicacion(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Cerrando conexión serie.")
        self.root.quit()

def main():
    root = tk.Tk()
    app = SimonGame(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()

if __name__ == "__main__":
    main()