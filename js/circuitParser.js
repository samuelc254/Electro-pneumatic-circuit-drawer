const LETTER_SIGNAL_PATTERN = /^([a-z][+-])+$/;

export function normalizeSequence(rawValue) {
    if (typeof rawValue !== "string") {
        return "";
    }

    return rawValue.replace(/\s+/g, "").toLowerCase();
}

export function parseSequence(rawValue) {
    const sequence = normalizeSequence(rawValue);

    if (!sequence) {
        throw new Error("Informe uma sequencia de circuito.");
    }

    if (sequence.length % 2 !== 0) {
        throw new Error("A sequencia deve alternar letra e sinal (+ ou -).");
    }

    if (!LETTER_SIGNAL_PATTERN.test(sequence)) {
        throw new Error("Formato invalido. Exemplo valido: A+B-A-B+");
    }

    const steps = [];
    for (let i = 0; i < sequence.length; i += 2) {
        steps.push({
            actuator: sequence[i],
            signal: sequence[i + 1],
        });
    }

    return {
        normalized: sequence,
        steps,
        etapas: steps.length + 1,
    };
}

export function actuatorNumber(letter) {
    const code = letter.charCodeAt(0) - 96;
    if (code < 1 || code > 26) {
        throw new Error("Atuador invalido.");
    }
    return String(code);
}

export function actuatorSignal(signal) {
    if (signal === "-") {
        return "1";
    }
    if (signal === "+") {
        return "2";
    }
    throw new Error("Sinal invalido.");
}
