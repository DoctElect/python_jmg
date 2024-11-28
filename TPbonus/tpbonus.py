import random
import itertools
import operator
import tkinter as tk
from tkinter import messagebox

# Opérations autorisées
operations = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# Génération des chiffres et du nombre cible
def generer_tirage():
    grands_nombres = [25, 50, 75, 100]
    petits_nombres = list(range(1, 11)) * 2
    nombres = random.sample(grands_nombres, 2) + random.sample(petits_nombres, 4)
    cible = random.randint(100, 999)
    return nombres, cible

# Résolution brute-force : trouver une combinaison qui atteint la cible
def resoudre(tirage, cible):
    for r in range(2, len(tirage) + 1):  # Teste toutes les combinaisons de 2 à 6 nombres
        for nombres in itertools.permutations(tirage, r):
            for ops in itertools.product(operations.keys(), repeat=r-1):
                expression = construire_expression(nombres, ops)
                try:
                    if eval(expression) == cible:
                        return expression
                except ZeroDivisionError:
                    continue
    return None

# Construction d'une expression mathématique à partir de nombres et d'opérations
def construire_expression(nombres, ops):
    expression = str(nombres[0])
    for i, op in enumerate(ops):
        expression += f" {op} {nombres[i+1]}"
    return expression

# Interface graphique avec Tkinter
class JeuDesChiffresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu des chiffres - Des chiffres et des lettres")
        
        # Variables
        self.tirage = []
        self.cible = 0
        self.solution = None

        # Interface
        self.label_tirage = tk.Label(root, text="Chiffres :", font=("Arial", 16))
        self.label_tirage.pack(pady=10)

        self.label_cible = tk.Label(root, text="Nombre cible : ", font=("Arial", 16))
        self.label_cible.pack(pady=10)

        self.solution_button = tk.Button(root, text="Trouver une solution", command=self.trouver_solution)
        self.solution_button.pack(pady=10)

        self.user_entry = tk.Entry(root, font=("Arial", 14))
        self.user_entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Soumettre ma solution", command=self.verifier_solution)
        self.submit_button.pack(pady=10)

        self.nouveau_button = tk.Button(root, text="Nouveau tirage", command=self.nouveau_tirage)
        self.nouveau_button.pack(pady=10)

        # Charger un premier tirage
        self.nouveau_tirage()

    def nouveau_tirage(self):
        # Générer un nouveau tirage
        self.tirage, self.cible = generer_tirage()
        self.solution = None
        self.label_tirage.config(text=f"Chiffres : {', '.join(map(str, self.tirage))}")
        self.label_cible.config(text=f"Nombre cible : {self.cible}")
        self.user_entry.delete(0, tk.END)

    def trouver_solution(self):
        if not self.solution:
            self.solution = resoudre(self.tirage, self.cible)
        if self.solution:
            messagebox.showinfo("Solution trouvée", f"Solution : {self.solution} = {eval(self.solution)}")
        else:
            messagebox.showinfo("Aucune solution", "Aucune solution exacte n'a été trouvée.")

    def verifier_solution(self):
        # Vérifier la solution proposée par l'utilisateur
        user_solution = self.user_entry.get()
        try:
            # Évaluer la solution utilisateur
            result = eval(user_solution)
            if result == self.cible:
                messagebox.showinfo("Bravo !", "Votre solution est correcte !")
            else:
                messagebox.showerror("Incorrect", f"Votre solution donne {result}, mais la cible est {self.cible}.")
        except Exception as e:
            messagebox.showerror("Erreur", "Votre solution est invalide. Assurez-vous qu'elle est correctement formatée.")

# Lancer l'application
if __name__ == '__main__':
    root = tk.Tk()
    app = JeuDesChiffresApp(root)
    root.mainloop()
