export class CanvasRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.dpr = Math.max(1, window.devicePixelRatio || 1);
        this.transform = {
            scale: 1,
            offsetX: 40,
            offsetY: 40,
            minScale: 0.2,
            maxScale: 5,
        };
        this.layout = null;
    }

    resize() {
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = Math.floor(rect.width * this.dpr);
        this.canvas.height = Math.floor(rect.height * this.dpr);
        this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
        this.redraw();
    }

    setLayout(layout) {
        this.layout = layout;
        this.redraw();
    }

    setTransform(nextTransform) {
        this.transform = {
            ...this.transform,
            ...nextTransform,
        };
        this.redraw();
    }

    getTransform() {
        return { ...this.transform };
    }

    clear() {
        const width = this.canvas.width / this.dpr;
        const height = this.canvas.height / this.dpr;

        const gradient = this.ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, "#ffffff");
        gradient.addColorStop(1, "#f8fafc");
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, width, height);

        this.ctx.save();
        this.ctx.strokeStyle = "rgba(148, 163, 184, 0.12)";
        this.ctx.lineWidth = 1;
        for (let x = 0; x < width; x += 24) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, height);
            this.ctx.stroke();
        }
        for (let y = 0; y < height; y += 24) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(width, y);
            this.ctx.stroke();
        }
        this.ctx.restore();
    }

    redraw() {
        this.clear();

        if (!this.layout) {
            return;
        }

        this.ctx.save();
        this.ctx.translate(this.transform.offsetX, this.transform.offsetY);
        this.ctx.scale(this.transform.scale, this.transform.scale);

        for (const primitive of this.layout.primitives) {
            this.drawPrimitive(primitive);
        }

        this.ctx.restore();
    }

    drawPrimitive(primitive) {
        if (primitive.type === "line") {
            this.ctx.beginPath();
            this.ctx.strokeStyle = primitive.color;
            this.ctx.lineWidth = primitive.width;
            this.ctx.moveTo(primitive.x1, primitive.y1);
            this.ctx.lineTo(primitive.x2, primitive.y2);
            this.ctx.stroke();
            return;
        }

        if (primitive.type === "circle") {
            this.ctx.beginPath();
            this.ctx.lineWidth = primitive.lineWidth;
            this.ctx.strokeStyle = primitive.stroke;
            this.ctx.fillStyle = primitive.fill;
            this.ctx.arc(primitive.x, primitive.y, primitive.radius, 0, Math.PI * 2);
            if (primitive.fill !== "transparent") {
                this.ctx.fill();
            }
            this.ctx.stroke();
            return;
        }

        if (primitive.type === "rect") {
            this.ctx.beginPath();
            this.ctx.lineWidth = primitive.lineWidth;
            this.ctx.strokeStyle = primitive.stroke;
            this.ctx.fillStyle = primitive.fill;
            this.ctx.rect(primitive.x, primitive.y, primitive.width, primitive.height);
            if (primitive.fill !== "transparent") {
                this.ctx.fill();
            }
            this.ctx.stroke();
            return;
        }

        if (primitive.type === "text") {
            this.ctx.fillStyle = primitive.color;
            this.ctx.font = `${primitive.weight} ${primitive.size}px "Inter", "Segoe UI", sans-serif`;
            this.ctx.fillText(primitive.text, primitive.x, primitive.y);
        }
    }

    fitToLayout(padding = 28) {
        if (!this.layout) {
            return;
        }

        const viewportWidth = this.canvas.width / this.dpr;
        const viewportHeight = this.canvas.height / this.dpr;
        const scaleX = (viewportWidth - padding * 2) / this.layout.width;
        const scaleY = (viewportHeight - padding * 2) / this.layout.height;
        const nextScale = Math.max(this.transform.minScale, Math.min(this.transform.maxScale, Math.min(scaleX, scaleY)));

        const offsetX = (viewportWidth - this.layout.width * nextScale) / 2;
        const offsetY = (viewportHeight - this.layout.height * nextScale) / 2;

        this.setTransform({
            scale: nextScale,
            offsetX,
            offsetY,
        });
    }
}
