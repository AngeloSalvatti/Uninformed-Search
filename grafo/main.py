import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from random import randrange
from UninformedSearchNP import UninformedSearchNP  

class UninformedSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Search")
        
        self.nx, self.ny, self.qtd = 10, 10, 10  # Minimum dimension 10x10
        self.map = self.generate_random_problem() 
        self.origin = None
        self.destination = None
        
        self.create_widgets()
    
    def generate_random_problem(self):
        map = np.zeros((self.nx, self.ny), int)
        k = 0
        while k < self.qtd:
            i, j = randrange(0, self.nx), randrange(0, self.ny)
            if map[i][j] == 0:
                map[i][j] = 9  # obstacle
                k += 1
        return map
    
    def carrega_grid_txt(self, file):
        try:
            with open(file, 'r') as f:
                map = []
                for line in f:
                    linha = list(map(int, line.strip().split(',')))
                    map.append(linha)
                # Updates grid dimensions
                self.nx = len(map)
                self.ny = len(map[0])
                return np.array(map)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")
            return None
    
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0)

        # Grid dimensions
        ttk.Label(frame, text="Dimensions (NxN):").grid(row=0, column=0)
        self.grid_size = ttk.Entry(frame, width=5)
        self.grid_size.grid(row=0, column=1)
        self.grid_size.insert(0, "10")
        
        ttk.Label(frame, text="Search Method:").grid(row=1, column=0)
        self.method = ttk.Combobox(frame, values=["BFS", "DFS" , "LDS", "ID", "bidirectional"])
        self.method.grid(row=1,column=1, columnspan=2)
        self.method.current(0)                                                      
        #limit
        ttk.Label(frame, text="limit:").grid(row=2, column=0)
        self.limit = ttk.Entry(frame, width=5)
        self.limit.grid(row=2, column=1)
        
        self.btn_buscar = ttk.Button(frame, text="Search Path", command=self.Search_Path)
        self.btn_buscar.grid(row=3, column=0, columnspan=3, pady=5)
        
        self.btn_novo = ttk.Button(frame, text="New Grid", command=self.New_Grid)
        self.btn_novo.grid(row=4, column=0, columnspan=3, pady=5)

        self.btn_carregar = ttk.Button(frame, text="Load Grid", command=self.Load_Grid)
        self.btn_carregar.grid(row=5, column=0, columnspan=3, pady=5)
        
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.grid(row=1, column=0)
        self.canvas.bind("<Button-1>", self.select_point)
        self.draw_grid()
    
    def draw_grid(self, path=[]):
        self.canvas.delete("all")
        cell_size = 30
        canvas_width = self.ny * cell_size
        canvas_height = self.nx * cell_size
        self.canvas.config(width=canvas_width, height=canvas_height)
        
        for i in range(self.nx):
            for j in range(self.ny):
                color = "white"
                if self.map[i][j] == 9:
                    color = "black"
                elif [i, j] in path:
                    idx = path.index([i, j])
                    frac = idx / len(path)
                    r = int(255 * frac)
                    b = int(255 * (1 - frac))
                    color = f"#{r:02x}00{b:02x}"
                elif [i, j] == self.origin:
                    color = "green"
                elif [i, j] == self.destination:
                    color = "red"
                
                self.canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color, outline="gray")
    
    def select_point(self, event):
        cell_size = 30
        j = event.x // cell_size
        i = event.y // cell_size
        
        
        if self.map[i][j] == 9:
            return
        
        if self.origin is None:
            self.origin = [i, j]
        elif self.destination is None:
            self.destination = [i, j]
        else:
            self.origin, self.destination = [i, j], None
        
        self.draw_grid()
    
    def Search_Path(self):
        if self.origin is None or self.destination is None:
            messagebox.showerror("Error", "Select origin & destination!")
            return
        limit=int(self.limit.get())
        sol = UninformedSearchNP()
        method = self.method.get()
        if method == "BFS":
            path = sol.amplitude(self.origin, self.destination, self.nx, self.ny, self.map)
        elif method == "DFS":
            path = sol.profundidade(self.origin, self.destination, self.nx, self.ny, self.map)
        elif method == "LDS":
            path = sol.prof_limitada(self.origin,self.destination,self.nx,self.ny,self.map,limit)
        elif method == "ID":
            limit_maximo = self.nx*self.ny
            path = sol.aprof_iterativo(self.origin,self.destination,self.nx,self.ny,self.map,limit_maximo) 
        elif method == "bidirectional":
            path = sol.bidirecional(self.origin,self.destination,self.nx,self.ny,self.map)
        
        if path:
            self.draw_grid(path)
        else:
            messagebox.showinfo("Search", "path not found!")
    
    def New_Grid(self):
        try:
            size = int(self.grid_size.get())
            if size < 10:
                raise ValueError
            self.nx = self.ny = size
        except ValueError:
            messagebox.showerror("Error", "Invalid dimension! Use a value >= 10.")
            return
        self.map = self.generate_random_problem()
        self.origin = None
        self.destination = None
        self.draw_grid()

    def Load_Grid(self):
        file = filedialog.askopenfilename(filetypes=[("text files", "*.txt")])
        if file:
            map = self.carrega_grid_txt(file)
            if map is not None:
                self.map = map
                self.draw_grid()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = UninformedSearchGUI(root)
    root.mainloop()
