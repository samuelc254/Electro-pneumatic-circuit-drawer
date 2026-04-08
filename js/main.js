import { parseSequence, normalizeSequence } from "./circuitParser.js";
import { buildCircuitLayout } from "./layoutEngine.js";
import { CanvasRenderer } from "./canvasRenderer.js";
import { PanZoomController } from "./panZoomController.js";

const defaultSequence = "a+b-a-b+";

const sequenceInput = document.getElementById("sequenceInput");
const drawButton = document.getElementById("drawButton");
const zoomInButton = document.getElementById("zoomInButton");
const zoomOutButton = document.getElementById("zoomOutButton");
const fitButton = document.getElementById("fitButton");
const resetViewButton = document.getElementById("resetViewButton");
const copyLinkButton = document.getElementById("copyLinkButton");
const statusMessage = document.getElementById("statusMessage");
const canvas = document.getElementById("circuitCanvas");

const renderer = new CanvasRenderer(canvas);
const panZoom = new PanZoomController(canvas, renderer);
panZoom.attach();

function showStatus(message, type = "ok") {
    statusMessage.textContent = message;
    statusMessage.classList.remove("ok", "error");
    statusMessage.classList.add(type);
}

function setUrlFromSequence(sequence) {
    const params = new URLSearchParams(window.location.search);
    params.set("circuit", sequence);
    const nextQuery = params.toString();
    const nextUrl = `${window.location.pathname}?${nextQuery}`;
    window.history.pushState({ circuit: sequence }, "", nextUrl);
}

function readSequenceFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const fromQuery = params.get("circuit");
    if (!fromQuery) {
        return defaultSequence;
    }

    // URLSearchParams trata '+' como espaco em alguns casos.
    return fromQuery.replace(/ /g, "+");
}

function renderCircuit(rawSequence, shouldUpdateUrl = true) {
    try {
        const parsed = parseSequence(rawSequence);
        const layout = buildCircuitLayout(parsed, false);
        renderer.setLayout(layout);
        renderer.fitToLayout();

        const upperSequence = parsed.normalized.toUpperCase();
        sequenceInput.value = upperSequence;

        if (shouldUpdateUrl) {
            setUrlFromSequence(upperSequence);
        }

        showStatus(`Circuito ${upperSequence} renderizado com sucesso.`, "ok");
    } catch (error) {
        showStatus(error.message, "error");
    }
}

function adjustZoom(step) {
    const current = renderer.getTransform();
    const rect = canvas.getBoundingClientRect();
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const nextScale = Math.max(current.minScale, Math.min(current.maxScale, current.scale + step));
    const ratio = nextScale / current.scale;

    renderer.setTransform({
        scale: nextScale,
        offsetX: centerX - (centerX - current.offsetX) * ratio,
        offsetY: centerY - (centerY - current.offsetY) * ratio,
    });
}

drawButton.addEventListener("click", () => {
    renderCircuit(sequenceInput.value, true);
});

sequenceInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        renderCircuit(sequenceInput.value, true);
    }
});

zoomInButton.addEventListener("click", () => adjustZoom(0.15));
zoomOutButton.addEventListener("click", () => adjustZoom(-0.15));
fitButton.addEventListener("click", () => renderer.fitToLayout());
resetViewButton.addEventListener("click", () => {
    renderer.setTransform({ scale: 1, offsetX: 40, offsetY: 40 });
});

copyLinkButton.addEventListener("click", async () => {
    const normalized = normalizeSequence(sequenceInput.value);
    try {
        const parsed = parseSequence(normalized);
        const params = new URLSearchParams(window.location.search);
        params.set("circuit", parsed.normalized.toUpperCase());
        const link = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
        await navigator.clipboard.writeText(link);
        showStatus("Link copiado para a area de transferencia.", "ok");
    } catch (error) {
        showStatus(error.message, "error");
    }
});

window.addEventListener("resize", () => {
    renderer.resize();
    renderer.fitToLayout();
});

window.addEventListener("popstate", () => {
    renderCircuit(readSequenceFromUrl(), false);
});

renderer.resize();
renderCircuit(readSequenceFromUrl(), false);
