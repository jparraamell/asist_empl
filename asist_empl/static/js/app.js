function animateNumber(element, target) {
    if (!element) return;
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 30);
}

    // Cargar estadísticas al cargar la página
    document.addEventListener('DOMContentLoaded', function () {
        // Simular carga de datos (aquí conectarías con tu API)
        setTimeout(() => {
            animateNumber(document.getElementById('total-empleados'), 150);
            animateNumber(document.getElementById('asistencia-hoy'), 142);
            animateNumber(document.getElementById('entradas-hoy'), 98);
            animateNumber(document.getElementById('salidas-hoy'), 45);
            animateNumber(document.getElementById('presentes-ahora'), 53);
        }, 500);
    });