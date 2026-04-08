export class PanZoomController {
    constructor(canvas, renderer) {
        this.canvas = canvas;
        this.renderer = renderer;
        this.isDragging = false;
        this.lastX = 0;
        this.lastY = 0;
    }

    attach() {
        this.canvas.addEventListener("wheel", (event) => {
            event.preventDefault();

            const zoomFactor = event.deltaY < 0 ? 1.1 : 0.9;
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = event.clientX - rect.left;
            const mouseY = event.clientY - rect.top;

            const current = this.renderer.getTransform();
            const nextScale = Math.max(current.minScale, Math.min(current.maxScale, current.scale * zoomFactor));
            const ratio = nextScale / current.scale;

            const offsetX = mouseX - (mouseX - current.offsetX) * ratio;
            const offsetY = mouseY - (mouseY - current.offsetY) * ratio;

            this.renderer.setTransform({
                scale: nextScale,
                offsetX,
                offsetY,
            });
        });

        this.canvas.addEventListener("pointerdown", (event) => {
            this.isDragging = true;
            this.lastX = event.clientX;
            this.lastY = event.clientY;
            this.canvas.setPointerCapture(event.pointerId);
            this.canvas.style.cursor = "grabbing";
        });

        this.canvas.addEventListener("pointermove", (event) => {
            if (!this.isDragging) {
                return;
            }

            const dx = event.clientX - this.lastX;
            const dy = event.clientY - this.lastY;
            this.lastX = event.clientX;
            this.lastY = event.clientY;

            const current = this.renderer.getTransform();
            this.renderer.setTransform({
                offsetX: current.offsetX + dx,
                offsetY: current.offsetY + dy,
            });
        });

        const stopDragging = (event) => {
            if (!this.isDragging) {
                return;
            }

            this.isDragging = false;
            if (event.pointerId !== undefined) {
                this.canvas.releasePointerCapture(event.pointerId);
            }
            this.canvas.style.cursor = "grab";
        };

        this.canvas.addEventListener("pointerup", stopDragging);
        this.canvas.addEventListener("pointercancel", stopDragging);
        this.canvas.addEventListener("pointerleave", stopDragging);
        this.canvas.style.cursor = "grab";
    }
}
