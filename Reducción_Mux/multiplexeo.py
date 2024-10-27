import tkinter as tk
from tkinter import messagebox

# Función para generar la tabla de verdad basada en los minterms 
def generar_tabla_verdad(minterms, variables):
    n = len(variables)  # Calcula el número de variables segun los minterminos mayores (bits)
    return [[int(bit) for bit in format(i, f'0{n}b')] + [int(i in minterms)] for i in range(2 ** n)]
    # Genera todas las combinaciones de valores binarios para las variables, con una columna adicional
    # para las salidas (minterminos)
    


# Función para generar la tabla MUX basada en los minterms y la variable de control
def generar_tabla_mux(variable_idx, variables, tabla_verdad):
    n = len(variables)
    
    # Calcular el valor más alto en la tabla de verdad en decimal
    max_valor_decimal = max(int("".join(map(str, fila[:-1])), 2) for fila in tabla_verdad)
    
    # Determinar el número de índices basado en el valor más alto dividido entre 2
    num_indices = (max_valor_decimal + 1) // 2  # Se suma 1 para incluir el caso del valor más alto
    minterms_activos = [fila[-1] for fila in tabla_verdad]  # Última columna de la tabla de verdad
    tabla_mux = []
    # Crear dos listas para las dos filas del MUX (variable de control negada y sin negar)
    canal_Ap = []
    canal_A = []

    # Recorre cada fila de la tabla de verdad y organiza secuencialmente
    for i in range(0, len(minterms_activos)):
        val_decimal = int("".join(map(str, tabla_verdad[i][:-1])), 2)  # Convertir binario a decimal
        
        if i < num_indices:
            canal_Ap.append(val_decimal)
        else:
            canal_A.append(val_decimal)

    # Asegurar que ambas filas tengan el mismo número de índices
    while len(canal_Ap) < num_indices:
        canal_Ap.append('-')  # Usar un símbolo de relleno si no hay suficientes valores
    while len(canal_A) < num_indices:
        canal_A.append('-')  # Usar un símbolo de relleno si no hay suficientes valores

    # Agregar las filas a la tabla MUX
    tabla_mux.append(canal_Ap)
    tabla_mux.append(canal_A)

    return tabla_mux

# Función para imprimir la tabla de verdad en un formato 
def imprimir_tabla(tabla, variables):
    encabezado = " | ".join(variables) + " | Salida"
    return f"{encabezado}\n{'-' * (len(encabezado))}\n" + "\n".join(" | ".join(map(str, fila[:-1])) + f" | {fila[-1]}" for fila in tabla)


# Función para imprimir la tabla reducida del MUX con los resultados
def imprimir_tabla_mux(tabla_mux, variable_control, minterms):
    control_var = variable_control  # Variable de control seleccionada 

    # Crear la tabla MUX en formato texto
    resultado = "     "
    resultado += " | ".join([f"I{i}" for i in range(len(tabla_mux[0]))]) + "\n"
    resultado += f" {control_var}' | {' | '.join(map(str, tabla_mux[0]))}\n"
    resultado += f" {control_var}  | {' | '.join(map(str, tabla_mux[1]))}\n"
    resultado += f"----------------------------------------"
    
    # Calcular la fila de resultados
    fila_resultados = []
    for val_Ap, val_A in zip(tabla_mux[0], tabla_mux[1]):
        # Verificar si los valores están en los minterms
        es_minterm_Ap = val_Ap in minterms
        es_minterm_A = val_A in minterms

        if es_minterm_Ap and es_minterm_A:
            fila_resultados.append('1')  # Ambos son minterms
        elif not es_minterm_Ap and not es_minterm_A:
            fila_resultados.append('0')  # Ninguno es minterm
        elif es_minterm_Ap:
            fila_resultados.append(f"{control_var}'")  # Solo A' es un minterm
        else:
            fila_resultados.append(f"{control_var}")   # Solo A es un minterm

    # Agregar la fila de resultados al texto
    resultado += f" = | {' | '.join(fila_resultados)}\n"
    return resultado



# Función para calcular el MUX y mostrar los resultados
def calcular_mux():
    try:
        # Obtiene los minterms ingresados por el usuario en el cuadro de entrada (entry_minterms)
        # La entrada se convierte en una lista de enteros. Se asume que el usuario separa los minterms por comas.
        minterms = list(map(int, entry_minterms.get().split(',')))

        # Calcula el número de variables necesarias basándose en el minterm más grande
        # La función bin convierte el número más alto en binario y se usa "-2" para quitar el prefijo '0b'.
        num_variables = len(bin(max(minterms))) - 2

        # Genera una lista de variables (A, B, C, ...) según la cantidad de variables necesarias.
        # Usa la función chr(i) para generar las letras a partir de su código ASCII, comenzando en 'A' (ASCII 65).
        variables = [chr(i) for i in range(65, 65 + num_variables)]

        # Busca el índice de la variable de control seleccionada (A, B, C, ...), la cual se obtiene del menú de opciones.
        variable_idx = variables.index(variable_control.get()) 

        # Genera la tabla de verdad usando los minterms y las variables. Esta función devuelve todas las combinaciones de valores binarios.
        tabla_verdad = generar_tabla_verdad(minterms, variables)

        # Genera la tabla MUX usando el índice de la variable de control, las variables, y la tabla de verdad previamente generada.
        tabla_mux = generar_tabla_mux(variable_idx, variables, tabla_verdad)

        # Limpia el área de texto donde se muestran los resultados (desde la posición 1.0 hasta el final).
        resultado_texto.delete(1.0, tk.END)

        # Inserta las variables usadas en el área de texto, formateadas como una lista separada por comas.
        resultado_texto.insert(tk.END, f"Variables: {', '.join(variables)}\n\n")

        # Inserta la tabla de verdad en el área de texto, formateada en una tabla amigable mediante la función imprimir_tabla().
        resultado_texto.insert(tk.END, f"Tabla de Verdad:\n{imprimir_tabla(tabla_verdad, variables)}\n\n")

        # Inserta la tabla MUX en el área de texto, mostrando las filas según la variable de control seleccionada y los minterms.
        resultado_texto.insert(tk.END, f"Tabla MUX (Control: {variable_control.get()}):\n{imprimir_tabla_mux(tabla_mux, variable_control.get(), minterms)}\n")

        # Limpia cualquier dibujo anterior en el canvas (lienzo) donde se mostrará la animación de las líneas de control.
        canvas.delete("all")

        # Llama a la función que muestra la animación de las líneas de control en el canvas, pasando las variables y el índice de control.
        mostrar_animacion_líneas(variables, variable_idx)

    # Si ocurre algún error (como valores de entrada no válidos), se muestra un mensaje de error en una ventana emergente.
    except Exception as e:
        messagebox.showerror("Error", str(e))



# Función para mostrar la animación de las líneas de control del MUX en el canvas
def mostrar_animacion_líneas(variables, variable_idx):
    # Establece la posición inicial en el eje Y y calcula la altura del MUX en función del número de variables.
    y_start, mux_height = 50, 50 * len(variables)

    # Dibuja un rectángulo que representa el MUX en el canvas, con su altura proporcional al número de variables.
    canvas.create_rectangle(150, y_start, 200, y_start + mux_height, fill="#D3D3D3", outline="black", width=2)

    # Coloca el texto "MUX" dentro del rectángulo dibujado, centrado en el MUX.
    canvas.create_text(175, y_start + mux_height / 2, text="MUX", font=("Arial", 12))

    # Recorre cada variable para dibujar las líneas de control en el canvas.
    for i, var in enumerate(variables):
        # Calcula la posición en Y para cada línea de control.
        y_pos = y_start + (i * 50) + 15

        # Dibuja una línea horizontal desde el lado izquierdo (50) hasta el borde del MUX (150).
        canvas.create_line(50, y_pos, 150, y_pos, width=2, fill="blue")

        # Agrega el nombre de la variable (A, B, C, etc.) al inicio de la línea, alineado a la derecha.
        canvas.create_text(40, y_pos, text=var, anchor=tk.E)

    # Dibuja la línea de salida desde el lado derecho del MUX (200) hacia la derecha.
    canvas.create_line(200, y_start + mux_height / 2, 300, y_start + mux_height / 2, width=2, fill="black")

    # Añade el texto "Salida" al final de la línea de salida.
    canvas.create_text(320, y_start + mux_height / 2, text="Salida", anchor=tk.W)

    # Inicia la animación llamando a la función animar_lineas(), comenzando desde la primera variable.
    animar_lineas(canvas, variables, 0, variable_idx)


# Función para animar las líneas de control una por una
def animar_lineas(canvas, variables, idx, variable_idx):
    # Verifica si el índice actual (idx) es menor que la cantidad de variables.
    if idx < len(variables):
        # Calcula la posición Y de la línea correspondiente a la variable en la posición idx.
        y_pos = 50 + (idx * 50) + 15

        # Si la variable actual es la variable de control seleccionada, la línea será verde, de lo contrario será roja.
        color = "green" if idx == variable_idx else "red"

        # Dibuja nuevamente la línea, esta vez cambiando el color para animar la selección.
        canvas.create_line(50, y_pos, 150, y_pos, width=2, fill=color)

        # Si la variable actual es la de control, resalta el MUX con un borde verde.
        if idx == variable_idx:
            canvas.create_rectangle(150, 50, 200, 50 + 50 * len(variables), outline="green", width=2)

        # Actualiza el canvas para mostrar los cambios visuales.
        canvas.update()

        # Llama a la misma función (recursión) después de 500 ms para animar la siguiente línea.
        canvas.after(500, animar_lineas, canvas, variables, idx + 1, variable_idx)


# Configuración de la interfaz gráfica
root = tk.Tk()
root.configure(bg="#1E1E1E")
root.title("Reducción de MUX")

# Contenedor para organizar los elementos en filas y columnas
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(padx=10, pady=10)

# Entrada de minterms
label_minterms = tk.Label(frame, text="Minterms (separados por coma):", fg="white", bg="#1E1E1E")
label_minterms.grid(row=0, column=0, padx=5, pady=5)
entry_minterms = tk.Entry(frame)
entry_minterms.grid(row=0, column=1, padx=5, pady=5)

# Selección de variable de control
label_variable = tk.Label(frame, text="Variable de Control:", fg="white", bg="#1E1E1E")
label_variable.grid(row=0, column=2, padx=5, pady=5)
variable_control = tk.StringVar()
variable_control.set("A")
variable_menu = tk.OptionMenu(frame, variable_control, *[chr(i) for i in range(65, 73)])
variable_menu.grid(row=0, column=3, padx=5, pady=5)

# Botón para calcular
calcular_btn = tk.Button(frame, text="Calcular MUX", command=calcular_mux, bg="#ADD8E6", fg="black")
calcular_btn.grid(row=0, column=4, padx=5, pady=5)

# Organización horizontal para el área de texto y canvas
result_canvas_frame = tk.Frame(frame, bg="#1E1E1E")
result_canvas_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

# Área de texto para mostrar resultados
resultado_texto = tk.Text(result_canvas_frame, height=20, width=40, bg="#2B2B2B", fg="white")
resultado_texto.pack(side=tk.LEFT, padx=5, pady=5)

# Canvas para la animación de líneas de selección
canvas = tk.Canvas(result_canvas_frame, width=400, height=300, bg="#1E1E1E")
canvas.pack(side=tk.RIGHT, padx=5, pady=5)

root.mainloop()