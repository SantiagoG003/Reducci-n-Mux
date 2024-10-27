import tkinter as tk
from tkinter import messagebox

# Función para generar la tabla de verdad basada en los minterms y las variables
def generar_tabla_verdad(minterms, variables):
    n = len(variables)  # Calcula el número de variables
    return [[int(bit) for bit in format(i, f'0{n}b')] + [1 if i in minterms else 0] for i in range(2 ** n)]
    # Genera todas las combinaciones de valores binarios para las variables, con una columna adicional
    # que indica si ese conjunto está en los minterms (1 si es un minterm, 0 si no)
    
    
# Función para generar la tabla reducida del multiplexor (MUX)
# Se selecciona una variable de control y se registran los pasos de reducción
def generar_tabla_mux(tabla_verdad, variable_idx, variables):
    # Inicializa la nueva tabla y una lista para registrar los pasos de la reducción
    nueva_tabla, pasos_reduccion = [], [f"Seleccionando la variable de control: {variables[variable_idx]}\n"]
    # Recorre cada fila de la tabla de verdad
    for fila in tabla_verdad:
        # Solo trabaja con las filas donde la salida es 1 (minterms)
        if fila[-1] == 1:
            # Determina el valor de la variable de control para la fila actual
            resultado = f"{variables[variable_idx]}'" if fila[variable_idx] == 0 else variables[variable_idx]
            # Agrega la fila a la nueva tabla junto con el resultado
            nueva_tabla.append((fila, resultado))
            # Guarda el paso de reducción
            pasos_reduccion.append(f"Minterm {fila[:-1]} con control {fila[variable_idx]} asignado a {resultado}")
    # Retorna la nueva tabla y los pasos de reducción
    return nueva_tabla, pasos_reduccion

# Función para imprimir la tabla de verdad en un formato amigable
def imprimir_tabla(tabla, variables):
    # Crea el encabezado con los nombres de las variables y la columna de salida
    encabezado = " | ".join(variables) + " | Salida"
    # Retorna la tabla de verdad formateada
    return f"{encabezado}\n{'-' * (len(encabezado) + 2)}\n" + "\n".join(" | ".join(map(str, fila[:-1])) + f" | {fila[-1]}" for fila in tabla)

# Función para imprimir la tabla reducida del MUX
def imprimir_tabla_mux(tabla_mux, variables):
    # Crea el encabezado con los nombres de las variables y la columna de salida
    encabezado = " | ".join(variables) + " | Salida"
    # Retorna la tabla reducida del MUX formateada
    return f"{encabezado}\n{'-' * (len(encabezado) + 2)}\n" + "\n".join(" | ".join(map(str, fila[:-1])) + f" | {resultado}" for fila, resultado in tabla_mux)

# Función para calcular la tabla MUX y mostrar los resultados
def calcular_mux():
    try:
        # Obtiene los minterms ingresados por el usuario
        minterms = list(map(int, entry_minterms.get().split(',')))
        # Calcula el número de variables basado en el valor máximo de los minterms
        num_variables = len(bin(max(minterms))) - 2
        # Genera los nombres de las variables (A, B, C, etc.)
        variables = [chr(i) for i in range(65, 65 + num_variables)]
        # Obtiene la variable de control seleccionada por el usuario
        variable_seleccionada = variable_control.get()
        # Verifica si la variable seleccionada es válida
        if variable_seleccionada not in variables:
            raise ValueError("Variable seleccionada no válida.")
        # Obtiene el índice de la variable seleccionada
        variable_idx = variables.index(variable_seleccionada)
        # Genera la tabla de verdad con los minterms
        tabla_verdad = generar_tabla_verdad(minterms, variables)
        # Genera la tabla reducida del MUX y los pasos de reducción
        tabla_mux, pasos_reduccion = generar_tabla_mux(tabla_verdad, variable_idx, variables)

        # Limpia el área de texto de resultados
        resultado_texto.delete(1.0, tk.END)
        # Inserta los nombres de las variables
        resultado_texto.insert(tk.END, f"Variables: {', '.join(variables)}\n\n")
        # Inserta la tabla de verdad
        resultado_texto.insert(tk.END, f"Tabla de Verdad:\n{imprimir_tabla(tabla_verdad, variables)}\n\n")
        # Inserta la tabla reducida del MUX
        resultado_texto.insert(tk.END, f"Tabla MUX (Control: {variable_seleccionada}):\n{imprimir_tabla_mux(tabla_mux, variables)}\n\n")
        # Inserta los pasos de reducción
        resultado_texto.insert(tk.END, "Pasos de reducción:\n" + "\n".join(pasos_reduccion))

        # Limpia el canvas para la nueva animación
        canvas.delete("all")
        # Muestra la animación de las líneas de selección en el MUX
        mostrar_animacion_líneas(variables, variable_idx)
        # Genera e inserta la función reducida basada en la tabla MUX
        generar_funcion_reducida(tabla_mux)
    except Exception as e:
        # Muestra un mensaje de error si ocurre algún problema durante el cálculo
        messagebox.showerror("Error", str(e))

# Función para generar e imprimir la función lógica reducida del MUX
def generar_funcion_reducida(tabla_mux):
    # Crea la función reducida como una suma de términos
    terminos = " + ".join(resultado for fila, resultado in tabla_mux)
    # Inserta la función reducida en el área de texto de resultados
    resultado_texto.insert(tk.END, f"\nFunción reducida del MUX: {terminos}\n")

# Función para mostrar la animación de las líneas de control del MUX en el canvas
def mostrar_animacion_líneas(variables, variable_idx):
    # Coordenadas iniciales y altura del MUX
    y_start, mux_height = 50, 50 * len(variables)
    # Dibuja el MUX como un rectángulo en el canvas
    canvas.create_rectangle(150, y_start, 200, y_start + mux_height, fill="#D3D3D3", outline="black", width=2)
    # Dibuja el texto "MUX" en el centro del rectángulo
    canvas.create_text(175, y_start + mux_height / 2, text="MUX", font=("Arial", 12))
    # Recorre cada variable para dibujar las líneas de control
    for i, var in enumerate(variables):
        # Calcula la posición vertical para cada línea
        y_pos = y_start + (i * 50) + 15
        # Dibuja la línea desde el lado izquierdo hasta el MUX
        canvas.create_line(50, y_pos, 150, y_pos, width=2, fill="blue")
        # Dibuja el nombre de la variable al lado izquierdo de la línea
        canvas.create_text(40, y_pos, text=var, anchor=tk.E)
    # Dibuja la línea de salida del MUX
    canvas.create_line(200, y_start + mux_height / 2, 300, y_start + mux_height / 2, width=2, fill="black")
    # Dibuja el texto "Salida" al final de la línea
    canvas.create_text(320, y_start + mux_height / 2, text="Salida", anchor=tk.W)
    # Inicia la animación de las líneas, resaltando la variable de control
    animar_lineas(canvas, variables, 0, variable_idx)

# Función recursiva para animar las líneas de control en el MUX
def animar_lineas(canvas, variables, idx, variable_idx):
    # Verifica si aún hay variables por animar
    if idx < len(variables):
        # Calcula la posición vertical de la línea actual
        y_pos = 50 + (idx * 50) + 15
        # Cambia el color de la línea según si es la variable de control o no
        color = "green" if idx == variable_idx else "red"
        # Dibuja la línea en el color correspondiente
        canvas.create_line(50, y_pos, 150, y_pos, width=2, fill=color)
        # Si es la variable de control, resalta el rectángulo del MUX
        if idx == variable_idx:
            canvas.create_rectangle(150, 50, 200, 50 + 50 * len(variables), outline="green", width=2)
        # Actualiza el canvas y continúa la animación después de un retraso
        canvas.update()
        canvas.after(500, animar_lineas, canvas, variables, idx + 1, variable_idx)

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
