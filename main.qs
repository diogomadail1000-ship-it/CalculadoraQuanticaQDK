operation Calculadora(a : Double, b : Double, operacao : String) : (Bool, Double) {
    let calculo = if operacao == "+" {
        (true, a + b)
    } elif operacao == "-" {
        (true, a - b)
    } elif operacao == "*" {
        (true, a * b)
    } elif operacao == "/" {
        if b == 0.0 {
            (false, 0.0)
        } else {
            (true, a / b)
        }
    } else {
        (false, 0.0)
    };
    calculo
}

operation CalculadoraBase(a : Int, b : Int, operacao : String) : (Bool, Int) {
    let calculo = if operacao == "+" {
        (true, a + b)
    } elif operacao == "-" {
        (true, a - b)
    } elif operacao == "*" {
        (true, a * b)
    } elif operacao == "/" {
        if b == 0 {
            (false, 0)
        } else {
            (true, a / b)
        }
    } else {
        (false, 0)
    };
    calculo
}

operation CircuitoCalculadora(a : Int, b : Int, operacao : Int, resultado : Int, largura : Int) : Unit {
    use registroA = Qubit[largura];
    use registroB = Qubit[largura];
    use registroOperacao = Qubit[2];
    use registroResultado = Qubit[largura];

    for bit in 0..(largura - 1) {
        if (((a >>> bit) &&& 1) == 1) {
            X(registroA[bit]);
        }
        if (((b >>> bit) &&& 1) == 1) {
            X(registroB[bit]);
        }
        if (((resultado >>> bit) &&& 1) == 1) {
            X(registroResultado[bit]);
        }
    }

    for bit in 0..1 {
        if (((operacao >>> bit) &&& 1) == 1) {
            X(registroOperacao[bit]);
        }
    }

    ResetAll(registroA);
    ResetAll(registroB);
    ResetAll(registroOperacao);
    ResetAll(registroResultado);
}

@EntryPoint()
operation Main() : (Bool, Double) {
    Calculadora(10.0, 2.0, "+")
}
