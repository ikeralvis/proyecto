import os
import random
import threading
import serial
import customtkinter as ctk
from PIL import Image, ImageTk
import time
import serial.tools.list_ports
import pygame




# Configuración de las rutas de Tcl y Tk
os.environ['TCL_LIBRARY'] = r'C:\Users\Usuario\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Usuario\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

# Configurar el tema y apariencia de CustomTkinter
ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

class SimonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simon Little")
        self.root.iconbitmap("simon.ico")

        self.create_gui()
        self.setup_serial()
        

    def setup_serial(self):
        self.port = "COM5"  # Puerto serie por defecto
        self.baud_rate = 115200 
        self.ser = None
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Conectado a {self.port} a {self.baud_rate} baudios.")
        except serial.SerialException as e:
            print(f"Error al conectar al puerto serial: {e}")

    def create_gui(self):
        # Fuente personalizada para el título
        fuente_titulo = ctk.CTkFont(family="Quicksand", 
                                    size=24, 
                                    weight="bold")
        
        fuente_subtitulo = ctk.CTkFont(family="Comfortaa", 
                                       size=16, 
                                       weight="normal")
        
        fuente_boton = ctk.CTkFont(family="Comic Sans MS", 
                                   size=24, 
                                   weight="bold")
        
        fuente_texto = ctk.CTkFont(family="Arial",
                                    size=14,
                                    weight="normal")

        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=10, border_width=1)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Etiqueta de bienvenida
        welcome_label = ctk.CTkLabel(
            main_frame, 
            text="Bienvenido al juego de Simon Little\n Dale al botón \"Empezar Juego\" para empezar este increible juego de memoria\n ¡Buena suerte!",
            wraplength=500,
            font= fuente_titulo
        )
        welcome_label.pack(pady=15)

        # Descripción del juego
        description_label = ctk.CTkLabel(
            main_frame, 
            text="El juego Simón Little funciona mostrando una secuencia de luces en dos LEDs, una tras otra, que el jugador debe memorizar y replicar presionando el botón correspondiente al LED encendido. La partida comienza con una secuencia aleatoria de cinco pulsaciones. El jugador tiene que seguirla en orden y cada acierto suma puntos según el número de pulsaciones correctas consecutivas: cinco puntos si completa la secuencia, cuatro si acierta cuatro, y así sucesivamente. Los puntos se acumulan en cada partida y se muestran en la pantalla una vez finalizada la misma.",
            wraplength=600,
            font= fuente_subtitulo
        )
        description_label.pack(pady=20, padx=30)

        # Botón de inicio personalizado
        imagen = Image.open("simon.png")
        imagen = imagen.resize((30, 30))

        self.start_button = ctk.CTkButton(
            main_frame,
            text="EMPEZAR JUEGO",
            command=self.iniciar_juego,
            font= fuente_boton,
            corner_radius=20,
            hover_color="#00aaff",
            width=300,
            height=60,
            cursor="hand2",
            image=ImageTk.PhotoImage(imagen),
        )
        self.start_button.pack(pady=20)

        # Contadores, uno a la izquierda y otro a la derecha
        contador_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        contador_frame.pack(pady=10)

        # Contador de puntuación
        self.score_label = ctk.CTkLabel(
            contador_frame,
            text="Puntuación actual: 0",
            font= fuente_texto
        )
        self.score_label.pack(padx= 15 ,pady=10, side="left")

        # Contador de puntuación total de todos los juegos
        self.total_score_label = ctk.CTkLabel(
            contador_frame,
            text="Puntuación total: 0",
            font= fuente_texto
        )
        self.total_score_label.pack(padx= 15, pady=10, side="right")

        # Bind Ctrl+D to show debug controls
        self.root.bind('<Control-d>', self.toggle_debug_controls)

    def toggle_debug_controls(self, event):
        if hasattr(self, 'debug_controls_visible') and self.debug_controls_visible:
            self.uart_frame.pack_forget()
            self.led_frame.pack_forget()
            self.debug_controls_visible = False
        else:
            # Crear frame de debug
            self.uart_frame = ctk.CTkFrame(self.root, corner_radius=10)
            self.uart_frame.pack(padx=20, pady=20, fill="x")

            # Entrada para comandos UART
            self.uart_entry = ctk.CTkEntry(
                self.uart_frame, 
                placeholder_text="Introduce comando UART"
            )
            self.uart_entry.pack(side="left", padx=10, expand=True, fill="x")

            # Botón de envío
            self.send_button = ctk.CTkButton(
                self.uart_frame,
                text="Enviar",
                command=self.enviar_comando,
                width=100
            )
            self.send_button.pack(side="right", padx=10)

            # Frame para LEDs
            self.led_frame = ctk.CTkFrame(self.root, corner_radius=10)
            self.led_frame.pack(padx=20, pady=10, fill="x")

            led_buttons = [
                ("LED 1", lambda: self.enviar_uart("LED1")),
                ("LED 2", lambda: self.enviar_uart("LED2")),
                ("LED 3", lambda: self.enviar_uart("LED3"))
            ]

            for text, command in led_buttons:
                button = ctk.CTkButton(
                    self.led_frame, 
                    text=text, 
                    command=command
                )
                button.pack(side="left", expand=True, padx=10, pady=10)

            # Elegir puerto serie
            self.port_label = ctk.CTkLabel(
                self.uart_frame, 
                text="Puerto serie:"
            )
            self.port_label.pack(side="left", padx=10)

            # Obtener lista de puertos disponibles
            available_ports = [port.device for port in serial.tools.list_ports.comports()]

            # Manejar el caso de que no haya puertos disponibles
            if not available_ports:
                available_ports = ["No hay puertos disponibles"]

            self.port_combobox = ctk.CTkComboBox(
                self.uart_frame,
                values=available_ports,
                width=100
            )
            
            print("Puertos disponibles",available_ports)
            print("Puerto elegido",self.port_combobox.get())
            print("Puerto actual",self.port)

            # Establecer un valor predeterminado si hay puertos disponibles
            if available_ports and available_ports[0] != "No hay puertos disponibles":
                self.port_combobox.set(available_ports[0])

            self.port_combobox.pack(side="left", padx=10)

            self.debug_controls_visible = True

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
            self.uart_entry.delete(0, 'end')

    def iniciar_juego(self):
        self.enviar_uart("STRT")  # Envía START al iniciar el juego
        print("Juego empezado")
        self.bucle_juego()

    def bucle_juego(self):

        def temporizador(tiempo_limite, bandera_tiempo):
            time.sleep(tiempo_limite)
            bandera_tiempo[0] = True

        def reproducir_sonido(ruta):
            # Inicializar pygame mixer
            pygame.mixer.init()
            
            try:
                # Cargar el sonido
                pygame.mixer.music.load(ruta)
                
                # Reproducir el sonido
                pygame.mixer.music.play()
                
                # Esperar a que termine de sonar
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            
            except FileNotFoundError:
                print("Error: El archivo de sonido no se encontró.")
            except Exception as e:
                print(f"Error al reproducir el sonido: {e}")
            
            # Cerrar pygame mixer
            pygame.mixer.quit()

        def juego_thread():
            try:
                while True:

                    if not self.ser or not self.ser.is_open:
                        print("La conexión serial no está disponible. Saliendo del bucle de juego.")
                        break
                    
                    # Generar secuencia de 5 colores
                    lista_colores = ["LED1", "LED2"]
                    secuencia = [random.choice(lista_colores) for _ in range(5)]
                    print("Secuencia generada:", secuencia)

                    # Reproducir sonido de inicio
                    self.enviar_uart("LED3")
                    reproducir_sonido("contador.mp3")
                    self.enviar_uart("NED3")

                    # Mostrar la secuencia generada en los LED
                    for color in secuencia:
                        if not self.ser or not self.ser.is_open:
                            print("Conexión cerrada durante la ejecución del juego.")
                        self.enviar_uart(color)
                        time.sleep(1)

                    # Recibir la secuencia de la placa
                    secuencia_placa = []
                    print("Esperando secuencia del usuario...")
                    tiempo_finalizado = [False]

                    hilo_temporizador = threading.Thread(target=temporizador, args=(20, tiempo_finalizado))
                    hilo_temporizador.start()
                    
                    # Bucle para recoger las pulsaciones
                    while len(secuencia_placa) < 5 and not tiempo_finalizado[0]:
                        if not self.ser or not self.ser.is_open:
                            print("Conexión cerrada durante la ejecución del juego.")
                            return
    
                        # Leer entrada si está disponible
                        if self.ser.in_waiting:
                            entrada = self.ser.readline()
                            print(entrada)
                            dato = entrada.decode('utf-8').replace('\x00', '').replace('\x001','').strip()
                            print (dato)
                            if (dato[0] == "1"):
                                secuencia_placa.append("LED1")
                            elif (dato[0] == "2"):
                                secuencia_placa.append("LED2")
                            print("Secuencia del usuario:", secuencia_placa)
                    
                    # Verificar condición de finalización
                    if tiempo_finalizado[0]:
                        reproducir_sonido("reloj.mp3")
                        print("Tiempo finalizado.")
                        print("Secuencia del usuario:", secuencia_placa)
                    elif len(secuencia_placa) == 5:
                        print("Secuencia del usuario:", secuencia_placa)
    
                        # Comprobar si la secuencia es correcta
                        if secuencia == secuencia_placa:
                            print("¡Secuencia correcta!")
                            reproducir_sonido("completado.mp3")
                        else:
                            print("Secuencia incorrecta.")
                            reproducir_sonido("super-mario-death-sound-sound-effect.mp3")

                    # Calcular la puntuación basada en la cantidad de LEDs acertados
                    aciertos = sum(1 for i in range(len(secuencia_placa)) if i < len(secuencia) and secuencia[i] == secuencia_placa[i])
                    puntuacion = aciertos
                    print(f"Puntuación: {puntuacion} de 5")
                    self.actualizar_puntuacion(puntuacion)
                    
                    # Pequeña pausa entre rondas
                    time.sleep(10)
            except serial.SerialException as e:
                print(f"Error en la comunicación serial: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            finally:
                if self.ser and self.ser.is_open:
                    print("juegoacabado")

        threading.Thread(target=juego_thread, daemon=True).start()


    def cerrar_aplicacion(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Cerrando conexión serie.")
        self.root.quit()

    def actualizar_puntuacion(self, puntuacion):
        self.score_label.configure(text=f"Puntuación actual: {puntuacion}")
        self.total_score_label.configure(text=f"Puntuación total: {puntuacion + int(self.total_score_label.cget('text').split(': ')[1])}")


def main():
    root = ctk.CTk()
    app = SimonGame(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()

if __name__ == "__main__":
    main()
