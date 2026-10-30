from decimal import Decimal
import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from qdk import code, qsharp
from qdk.qsharp import QSharpError


class CalculadoraApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculadora quântica | QDK")
        self.root.geometry("760x760")
        self.root.minsize(600, 680)

        self.cores = {
            "fundo": "#0B1020",
            "painel": "#141B2D",
            "painel_claro": "#1B2540",
            "borda": "#273552",
            "texto": "#F1F5FF",
            "texto_sutil": "#9AA9C5",
            "ciano": "#56D6D0",
            "roxo": "#9A83FF",
            "verde": "#8BE0B0",
        }
        self.root.configure(bg=self.cores["fundo"])

        conteudo = tk.Frame(root, bg=self.cores["fundo"], padx=30, pady=26)
        conteudo.pack(fill="both", expand=True)

        topo = tk.Frame(conteudo, bg=self.cores["fundo"])
        topo.pack(fill="x", pady=(0, 22))
        marca = tk.Label(
            topo,
            text="Q",
            bg=self.cores["ciano"],
            fg=self.cores["fundo"],
            font=("Segoe UI", 17, "bold"),
            width=2,
            height=1,
            padx=3,
            pady=2,
        )
        marca.pack(side="left", padx=(0, 14))
        titulo = tk.Frame(topo, bg=self.cores["fundo"])
        titulo.pack(side="left", fill="x", expand=True)
        tk.Label(
            titulo,
            text="QDK  /  QUANTUM LAB",
            bg=self.cores["fundo"],
            fg=self.cores["ciano"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            titulo,
            text="Calculadora quântica",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w", pady=(2, 0))
        tk.Label(
            titulo,
            text="Cálculos clássicos com um circuito quântico demonstrativo.",
            bg=self.cores["fundo"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        calculadora = tk.Frame(
            conteudo,
            bg=self.cores["painel"],
            padx=22,
            pady=20,
            highlightthickness=1,
            highlightbackground=self.cores["borda"],
        )
        calculadora.pack(fill="x")
        tk.Label(
            calculadora,
            text="FAÇA SEU CÁLCULO",
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 14))

        entradas = tk.Frame(calculadora, bg=self.cores["painel"])
        entradas.pack(fill="x")
        entradas.columnconfigure(0, weight=1)
        entradas.columnconfigure(2, weight=1)
        campo_primeiro, self.primeiro_valor = self._campo_valor(
            entradas, "PRIMEIRO VALOR"
        )
        campo_primeiro.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.primeiro_valor.insert(0, "10")

        seletor = tk.Frame(entradas, bg=self.cores["painel"])
        seletor.grid(row=0, column=1, padx=4)
        tk.Label(
            seletor,
            text="OPERAÇÃO",
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(0, 8))
        botoes_operacao = tk.Frame(seletor, bg=self.cores["painel"])
        botoes_operacao.pack()
        self.operacao = "+"
        self.botoes_operacao = {}
        for simbolo in ("+", "-", "*", "/"):
            botao = tk.Button(
                botoes_operacao,
                text=simbolo,
                command=lambda op=simbolo: self.selecionar_operacao(op),
                relief="flat",
                bd=0,
                width=3,
                height=1,
                cursor="hand2",
                font=("Segoe UI", 13, "bold"),
                padx=3,
                pady=5,
            )
            botao.pack(side="left", padx=2)
            self.botoes_operacao[simbolo] = botao
        self.selecionar_operacao("+")

        campo_segundo, self.segundo_valor = self._campo_valor(
            entradas, "SEGUNDO VALOR"
        )
        campo_segundo.grid(row=0, column=2, sticky="ew", padx=(12, 0))
        self.segundo_valor.insert(0, "2")

        base_seletor = tk.Frame(calculadora, bg=self.cores["painel"])
        base_seletor.pack(fill="x", pady=(16, 0))
        tk.Label(
            base_seletor,
            text="BASE DOS NÚMEROS",
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(0, 12))
        self.base = 10
        self.botoes_base = {}
        for nome, base in (("BIN", 2), ("OCT", 8), ("DEC", 10), ("HEX", 16)):
            botao = tk.Button(
                base_seletor,
                text=nome,
                command=lambda valor=base: self.selecionar_base(valor),
                relief="flat",
                bd=0,
                width=5,
                cursor="hand2",
                font=("Segoe UI", 8, "bold"),
                padx=3,
                pady=5,
            )
            botao.pack(side="left", padx=2)
            self.botoes_base[base] = botao

        self.dica_base = tk.Label(
            calculadora,
            text="Inteiros na base selecionada; divisão inteira fora da base decimal.",
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.dica_base.pack(fill="x", pady=(8, 0))
        self.selecionar_base(10)
        botoes_acao = tk.Frame(calculadora, bg=self.cores["painel"])
        botoes_acao.pack(fill="x", pady=(14, 0))
        tk.Button(
            botoes_acao,
            text="Calcular   →",
            command=self.calcular,
            bg=self.cores["ciano"],
            fg=self.cores["fundo"],
            activebackground="#78E7E1",
            activeforeground=self.cores["fundo"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            pady=11,
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Button(
            botoes_acao,
            text="⟳  Atualizar",
            command=self.atualizar,
            bg=self.cores["painel_claro"],
            fg=self.cores["texto"],
            activebackground=self.cores["borda"],
            activeforeground=self.cores["texto"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=11,
        ).pack(side="right")

        resultado_cartao = tk.Frame(
            conteudo,
            bg=self.cores["painel_claro"],
            padx=22,
            pady=16,
            highlightthickness=1,
            highlightbackground=self.cores["borda"],
        )
        resultado_cartao.pack(fill="x", pady=(16, 16))
        cabecalho_resultado = tk.Frame(resultado_cartao, bg=self.cores["painel_claro"])
        cabecalho_resultado.pack(fill="x")
        tk.Label(
            cabecalho_resultado,
            text="RESULTADO",
            bg=self.cores["painel_claro"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")
        tk.Label(
            cabecalho_resultado,
            text="●  PRONTO",
            bg=self.cores["painel_claro"],
            fg=self.cores["verde"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="right")
        self.resultado = tk.Label(
            resultado_cartao,
            text="Informe os valores e clique em Calcular.",
            bg=self.cores["painel_claro"],
            fg=self.cores["texto"],
            font=("Segoe UI", 19, "bold"),
            anchor="w",
            wraplength=650,
        )
        self.resultado.pack(fill="x", pady=(9, 0))

        circuito_cartao = tk.Frame(
            conteudo,
            bg=self.cores["painel"],
            padx=22,
            pady=18,
            highlightthickness=1,
            highlightbackground=self.cores["borda"],
        )
        circuito_cartao.pack(fill="both", expand=True)
        cabecalho_circuito = tk.Frame(circuito_cartao, bg=self.cores["painel"])
        cabecalho_circuito.pack(fill="x")
        tk.Label(
            cabecalho_circuito,
            text="Circuito quântico",
            bg=self.cores["painel"],
            fg=self.cores["texto"],
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")
        tk.Label(
            cabecalho_circuito,
            text="REGISTRADORES DA OPERAÇÃO",
            bg=self.cores["painel_claro"],
            fg=self.cores["roxo"],
            padx=9,
            pady=4,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="right")
        tk.Label(
            circuito_cartao,
            text=(
                "O circuito prepara registradores quânticos para os operandos, "
                "a operação e o resultado. O valor numérico é calculado em Q# "
                "e codificado no circuito; as portas não executam a aritmética."
            ),
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            justify="left",
            wraplength=640,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(6, 12))

        self.circuito_texto = tk.Text(
            circuito_cartao,
            height=6,
            wrap="none",
            font=("Consolas", 11),
            bg="#0A0F1C",
            fg="#B9C9E8",
            insertbackground=self.cores["ciano"],
            relief="flat",
            padx=14,
            pady=12,
            state="normal",
        )
        self.circuito_texto.pack(fill="both", expand=True)
        self.circuito_texto.insert(
            "1.0", "Faça um cálculo para gerar o circuito correspondente."
        )
        self.circuito_texto.configure(state="disabled")
        self.registradores = tk.Label(
            circuito_cartao,
            text="Registradores: A | B | operação | resultado",
            bg=self.cores["painel"],
            fg=self.cores["ciano"],
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        )
        self.registradores.pack(fill="x", pady=(10, 0))

        self.circuito_estado = tk.Label(
            circuito_cartao,
            text="Circuito aguardando cálculo",
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.circuito_estado.pack(fill="x", pady=(4, 0))

        self.primeiro_valor.focus_set()
        self.root.bind("<Return>", lambda _event: self.calcular())

    def _campo_valor(
        self, parent: tk.Widget, rotulo: str
    ) -> tuple[tk.Frame, tk.Entry]:
        grupo = tk.Frame(parent, bg=self.cores["painel"])
        tk.Label(
            grupo,
            text=rotulo,
            bg=self.cores["painel"],
            fg=self.cores["texto_sutil"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(0, 8))
        campo = tk.Entry(
            grupo,
            bg="#0D1425",
            fg=self.cores["texto"],
            insertbackground=self.cores["ciano"],
            selectbackground=self.cores["roxo"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.cores["borda"],
            highlightcolor=self.cores["ciano"],
            font=("Segoe UI", 15),
        )
        campo.pack(fill="x", ipady=9, padx=1)
        grupo.grid_columnconfigure(0, weight=1)
        return grupo, campo

    def selecionar_operacao(self, operacao: str) -> None:
        self.operacao = operacao
        for simbolo, botao in self.botoes_operacao.items():
            selecionado = simbolo == operacao
            botao.configure(
                bg=self.cores["ciano"] if selecionado else self.cores["painel_claro"],
                fg=self.cores["fundo"] if selecionado else self.cores["texto_sutil"],
                activebackground=self.cores["ciano"],
                activeforeground=self.cores["fundo"],
            )

    def selecionar_base(self, base: int) -> None:
        self.base = base
        nomes = {2: "binária", 8: "octal", 10: "decimal", 16: "hexadecimal"}
        if base == 10:
            dica = "Digite os valores em decimal; casas decimais são permitidas."
        else:
            dica = (
                f"Digite inteiros na base {nomes[base]}; "
                "a divisão retorna o quociente inteiro."
            )
        self.dica_base.configure(text=dica)
        for valor, botao in self.botoes_base.items():
            selecionado = valor == base
            botao.configure(
                bg=self.cores["roxo"] if selecionado else self.cores["painel_claro"],
                fg=self.cores["texto"] if selecionado else self.cores["texto_sutil"],
                activebackground=self.cores["roxo"],
                activeforeground=self.cores["texto"],
            )

    def atualizar_circuito(
        self, a: int, b: int, valor: int, operacao: str, casas_decimais: int
    ) -> None:
        valores = (a, b, valor)
        largura = max(1, *(abs(numero).bit_length() + 1 for numero in valores))
        if largura > 64:
            self.exibir_circuito(
                "Os valores excedem os 64 qubits de codificação suportados."
            )
            self.circuito_estado.configure(
                text="Circuito não gerado: limite de 64 qubits por registrador.",
                fg=self.cores["texto_sutil"],
            )
            return

        codigo_operacao = {"+": 0, "-": 1, "*": 2, "/": 3}[operacao]
        try:
            circuito = qsharp.circuit(
                f"CircuitoCalculadora({a}, {b}, {codigo_operacao}, {valor}, {largura})"
            )
        except QSharpError as error:
            self.exibir_circuito(f"Não foi possível gerar o circuito: {error}")
            self.circuito_estado.configure(
                text="Falha ao gerar o circuito Q#.",
                fg="#FF9B9B",
            )
            return

        self.exibir_circuito(str(circuito))
        escala = f" com escala 10^{casas_decimais}" if casas_decimais else ""
        descricao = (
            f"A={a}, B={b}, op.={operacao}, resultado={valor}{escala}; "
            f"{largura} qubits por número."
        )
        self.registradores.configure(
            text=(
                f"A: q0–q{largura - 1}  |  "
                f"B: q{largura}–q{2 * largura - 1}  |  "
                f"op.: q{2 * largura}–q{2 * largura + 1}  |  "
                f"resultado: q{2 * largura + 2}–q{3 * largura + 1}"
            )
        )
        self.circuito_estado.configure(text=descricao, fg=self.cores["ciano"])

    def exibir_circuito(self, texto: str) -> None:
        self.circuito_texto.configure(state="normal")
        self.circuito_texto.delete("1.0", tk.END)
        self.circuito_texto.insert("1.0", texto)
        self.circuito_texto.configure(state="disabled")

    def atualizar(self) -> None:
        self.primeiro_valor.delete(0, tk.END)
        self.primeiro_valor.insert(0, "10")
        self.segundo_valor.delete(0, tk.END)
        self.segundo_valor.insert(0, "2")
        self.selecionar_operacao("+")
        self.selecionar_base(10)
        self.resultado.configure(
            text="Informe os valores e clique em Calcular.",
            fg=self.cores["texto"],
        )
        self.registradores.configure(text="Registradores: A | B | operação | resultado")
        self.circuito_estado.configure(
            text="Circuito aguardando cálculo", fg=self.cores["texto_sutil"]
        )
        self.exibir_circuito("Faça um cálculo para gerar o circuito correspondente.")
        self.primeiro_valor.focus_set()

    @staticmethod
    def _escalar_decimais(
        valores: tuple[float, float, float]
    ) -> tuple[tuple[int, int, int], int]:
        if not all(math.isfinite(valor) for valor in valores):
            raise ValueError("Não é possível codificar um resultado não finito.")
        decimais = tuple(Decimal(str(valor)) for valor in valores)
        casas_decimais = max(
            (max(0, -decimal.as_tuple().exponent) for decimal in decimais),
            default=0,
        )
        inteiros = []
        for decimal in decimais:
            sinal, digitos, expoente = decimal.as_tuple()
            coeficiente = int("".join(str(digito) for digito in digitos) or "0")
            deslocamento = expoente + casas_decimais
            inteiro = coeficiente * (10**deslocamento)
            inteiros.append(-inteiro if sinal else inteiro)
        return (inteiros[0], inteiros[1], inteiros[2]), casas_decimais

    @staticmethod
    def formatar_base(valor: int, base: int) -> str:
        if base == 10:
            return str(valor)
        digitos = "0123456789ABCDEF"
        sinal = "-" if valor < 0 else ""
        resto = abs(valor)
        if resto == 0:
            return "0"
        resultado = ""
        while resto:
            resto, digito = divmod(resto, base)
            resultado = digitos[digito] + resultado
        return sinal + resultado

    def calcular(self) -> None:
        texto_a = self.primeiro_valor.get().strip()
        texto_b = self.segundo_valor.get().strip()
        operacao = self.operacao

        if self.base == 10:
            self.calcular_decimal(texto_a, texto_b, operacao)
            return

        try:
            a = int(texto_a, self.base)
            b = int(texto_b, self.base)
        except ValueError:
            messagebox.showerror(
                "Valor inválido",
                f"Digite números inteiros válidos na base {self.base}.",
            )
            return
        limite = 2**63
        if not (-limite <= a < limite and -limite <= b < limite):
            messagebox.showerror(
                "Valor fora do limite",
                "Q# aceita valores inteiros entre -2⁶³ e 2⁶³ - 1.",
            )
            return

        try:
            valido, valor = code.CalculadoraBase(a, b, operacao)
        except QSharpError as error:
            messagebox.showerror("Erro Q#", str(error))
            return

        if valido:
            numero_a = self.formatar_base(a, self.base)
            numero_b = self.formatar_base(b, self.base)
            resultado = self.formatar_base(valor, self.base)
            self.resultado.configure(
                text=f"{numero_a}  {operacao}  {numero_b}  =  {resultado}",
                fg=self.cores["texto"],
            )
            self.atualizar_circuito(a, b, valor, operacao, 0)
        else:
            self.resultado.configure(
                text="Não é possível dividir por zero.",
                fg="#FF9B9B",
            )
            self.exibir_circuito("Divisão por zero: não existe resultado para codificar.")
            self.circuito_estado.configure(
                text="Circuito não gerado para uma operação inválida.",
                fg="#FF9B9B",
            )

    def calcular_decimal(self, texto_a: str, texto_b: str, operacao: str) -> None:
        try:
            a = float(texto_a)
            b = float(texto_b)
        except ValueError:
            messagebox.showerror(
                "Valor inválido", "Digite números decimais válidos nos dois campos."
            )
            return
        if not math.isfinite(a) or not math.isfinite(b):
            messagebox.showerror(
                "Valor inválido", "Use números finitos nos dois campos."
            )
            return

        try:
            valido, valor = code.Calculadora(a, b, operacao)
        except QSharpError as error:
            messagebox.showerror("Erro Q#", str(error))
            return

        if valido:
            self.resultado.configure(
                text=f"{a:g}  {operacao}  {b:g}  =  {valor:g}",
                fg=self.cores["texto"],
            )
            try:
                (circuito_a, circuito_b, circuito_valor), casas_decimais = (
                    self._escalar_decimais((a, b, valor))
                )
                self.atualizar_circuito(
                    circuito_a,
                    circuito_b,
                    circuito_valor,
                    operacao,
                    casas_decimais,
                )
            except (OverflowError, ValueError):
                self.exibir_circuito(
                    "Os valores decimais são grandes demais para codificar."
                )
                self.circuito_estado.configure(
                    text="O cálculo foi feito; a codificação excede o limite suportado.",
                    fg=self.cores["texto_sutil"],
                )
        else:
            self.resultado.configure(
                text="Não é possível dividir por zero.",
                fg="#FF9B9B",
            )
            self.exibir_circuito("Divisão por zero: não existe resultado para codificar.")
            self.circuito_estado.configure(
                text="Circuito não gerado para uma operação inválida.",
                fg="#FF9B9B",
            )


def main() -> None:
    qsharp_file = Path(__file__).with_name("main.qs")
    qsharp.eval(qsharp_file.read_text(encoding="utf-8"))

    root = tk.Tk()
    CalculadoraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
