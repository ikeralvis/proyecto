# Simon Little - Memory Game Project 🎮

Simon Little es un juego de memoria interactivo que desafía a los jugadores a recordar y repetir una secuencia de patrones LED. Este proyecto combina un componente de hardware basado en microcontroladores con una GUI en Python, creando una experiencia de juego divertida y envolvente.

---

## 🎮 Overview

- **Interfaz:** Interactiva y amigable.
- **Desafío:** Memorizar y reproducir patrones LED.
- **Componentes:** Hardware (microcontrolador STM32) y software (Python GUI).
- **Objetivo:** Obtener la máxima puntuación reproduciendo secuencias correctamente.

---

## 🔧 Hardware Requirements

- **Microcontrolador:** STM32
- **LED:** 1 LEDs para mostrar el inicio del juego.
- **Botones:** 2 botones con LED para la interacción del jugador.
- **Interfaz de comunicación:** UART (Serial).

---

## 💻 Software Requirements

### Microcontroller
- STM32 HAL Library
- UART Communication
- GPIO Interrupt Handling

### Python Application
- **Python 3.13**
- **Librerías requeridas:**
  - `pyserial`
  - `customtkinter`
  - `pygame`
  - `pillow` (PIL)

---

## 🎲 Game Mechanics

- Generación aleatoria de una secuencia de 5 patrones LED.
- El jugador debe reproducir la secuencia exacta utilizando los botones.
- **Puntaje:** Basado en la cantidad de secuencias correctas.
- **Efectos de sonido:** Feedback para progresos del juego.

---

## 📦 Installation

### Microcontroller Setup
1. Usa **STM32CubeIDE** u otro IDE compatible.
2. Configura UART y ajustes GPIO.
3. Sube el firmware proporcionado al microcontrolador.

### Python Application Setup
1. Instala las librerías necesarias:
   ```bash
   pip install pyserial customtkinter pygame pillow
