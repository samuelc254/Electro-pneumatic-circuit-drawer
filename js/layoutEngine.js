import { actuatorNumber, actuatorSignal } from "./circuitParser.js";

function createLayoutState(etapas) {
    const tamanho = 10;
    const espacamento = tamanho * 5;

    return {
        tamanho,
        espacamento,
        cor: "#334155",
        yGlobal: espacamento,
        xGlobal: espacamento * 1.5,
        xPasso: espacamento * 1.5,
        yPasso: espacamento,
        width: etapas * 100 + 300,
        height: 350,
        primitives: [],
    };
}

function addPrimitive(state, primitive) {
    state.primitives.push(primitive);
}

function addLine(state, x1, y1, x2, y2, width = 1.8) {
    addPrimitive(state, { type: "line", x1, y1, x2, y2, width, color: state.cor });
}

function addCircle(state, x, y, radius, fill = "#334155", stroke = "#334155", lineWidth = 1.4) {
    addPrimitive(state, { type: "circle", x, y, radius, fill, stroke, lineWidth });
}

function addRect(state, x, y, width, height, fill = "transparent", stroke = "#334155", lineWidth = 1.8) {
    addPrimitive(state, { type: "rect", x, y, width, height, fill, stroke, lineWidth });
}

function addText(state, text, x, y, size = 12, color = "#475569", weight = "500") {
    addPrimitive(state, { type: "text", text, x, y, size, color, weight });
}

function plug(state, text, y) {
    addCircle(state, state.espacamento / 3.7, y, state.tamanho / 2.5, "transparent", state.cor, 1.5);
    addLine(state, state.espacamento / 3, y, state.espacamento, y, 1.6);
    addText(state, text, state.espacamento / 2.5, y - state.espacamento / 16, 12);
}

function contactNA(state, x, y, name) {
    addLine(state, x, y, x, y + state.tamanho * 2.5);
    addLine(state, x - state.tamanho, y + state.tamanho * 2.5, x, y + state.tamanho * 5);
    addLine(state, x, y + state.tamanho * 5, x, y + state.tamanho * 7.5);
    addText(state, name, x + state.tamanho * 0.6, y + state.tamanho * 3.6, 12);
    state.yPasso += state.tamanho * 7.5;
}

function contactNF(state, x, y, name) {
    addLine(state, x, y, x, y + state.tamanho * 2.5);
    addLine(state, x + state.tamanho, y + state.tamanho * 2.5, x, y + state.tamanho * 2.5);
    addLine(state, x + state.tamanho, y + state.tamanho * 2.5, x, y + state.tamanho * 5);
    addLine(state, x, y + state.tamanho * 5, x, y + state.tamanho * 7.5);
    addText(state, name, x + state.tamanho * 1.6, y + state.tamanho * 3.6, 12);
    state.yPasso += state.tamanho * 7.5;
}

function contator(state, x, y, name) {
    addLine(state, x, y, x, y + state.tamanho * 2);
    addRect(
        state,
        x - state.tamanho * 2,
        y + state.tamanho * 2,
        state.tamanho * 4,
        state.tamanho * 2,
        "transparent",
        state.cor,
        1.8
    );
    addLine(state, x, y + state.tamanho * 4, x, y + state.tamanho * 6);
    addText(state, name, x + state.tamanho * 2.6, y + state.tamanho * 3, 12);
    state.yPasso += state.tamanho * 6;
}

function addConnectionDot(state) {
    addCircle(state, state.xPasso, state.yPasso, state.tamanho / 4, state.cor, state.cor, 1.2);
}

export function buildCircuitLayout(parsed, debug = false) {
    const state = createLayoutState(parsed.etapas);
    const sequence = parsed.normalized.split("");

    plug(state, "24V", state.espacamento);
    plug(state, "0V", state.espacamento * 5.2);

    for (let i = 0; i < parsed.etapas; i += 1) {
        if (i !== parsed.etapas - 1) {
            addConnectionDot(state);
        }

        if (i === 0) {
            contactNA(state, state.xPasso, state.yPasso, "S1");
            if (i !== parsed.etapas - 1) {
                addConnectionDot(state);
            }
            contactNF(state, state.xPasso, state.yPasso, `K${parsed.etapas}`);
        } else {
            const activeName = `${actuatorNumber(sequence[i * 2 - 2])}S${actuatorSignal(sequence[i * 2 - 1])}`;
            contactNA(state, state.xPasso, state.yPasso, activeName);

            if (i !== parsed.etapas - 1) {
                addConnectionDot(state);
            }

            contactNA(state, state.xPasso, state.yPasso, `K${i}`);
        }

        contator(state, state.xPasso, state.yPasso, `K${i + 1}`);

        if (i !== parsed.etapas - 1) {
            addConnectionDot(state);

            state.xPasso += state.espacamento;
            state.yPasso = state.yGlobal;

            addConnectionDot(state);
            contactNA(state, state.xPasso, state.yPasso, `K${i + 1}`);
            addLine(state, state.xPasso, state.yPasso, state.xPasso - state.espacamento, state.yPasso);
        } else {
            addLine(state, state.espacamento, state.yGlobal, state.xPasso, state.yGlobal);
            addLine(state, state.xPasso, state.yPasso, state.espacamento, state.yPasso);
        }

        state.xGlobal += state.espacamento * 2;
        state.xPasso = state.xGlobal;
        state.yPasso = state.yGlobal;
    }

    if (debug) {
        addText(state, parsed.normalized, state.espacamento * 7, state.espacamento / 1.8, 12);
    }

    addText(
        state,
        "https://github.com/samuelc254/Electro-pneumatic-circuit-drawer",
        state.espacamento,
        state.espacamento * 6,
        11,
        "#3b4b51"
    );
    addText(
        state,
        "Electro-pneumatic circuit drawer v0.1.3",
        state.espacamento,
        state.espacamento / 2.2,
        12,
        "#3b4b51"
    );

    return {
        width: state.width,
        height: state.height,
        primitives: state.primitives,
    };
}
