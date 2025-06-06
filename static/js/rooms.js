window.addEventListener("scroll", function () {
    let navbar = document.querySelector(".navbar"); // Selecciona el navbar
    let h1 = document.querySelector("h1"); // Selecciona el H1

    // Calculamos la posición real de h1 en relación con la ventana
    let h1Position = h1.getBoundingClientRect().top;

    // Cambia el navbar a naranja cuando el H1 está a 100px del top
    if (h1Position <= 100) {  
        navbar.style.background = "orange";  // Cambia a color naranja sólido
        navbar.style.boxShadow = "0 8px 32px 0 rgba(0, 0, 0, 0.2)"; // Ajusta sombra
        navbar.style.backdropFilter = "none"; // Quita el efecto blur
        navbar.style.webkitBackdropFilter = "none"; // Para Safari
        navbar.style.border = "none"; // Quita el borde
    } else {  
        navbar.style.background = "rgba(255, 255, 255, 0.3)"; // Vuelve a glassmorphism
        navbar.style.boxShadow = "0 8px 32px 0 rgba(31, 38, 135, 0.37)";
        navbar.style.backdropFilter = "blur(0px)"; // Aplica desenfoque de vuelta
        navbar.style.webkitBackdropFilter = "blur(0px)";
        navbar.style.border = "1px solid rgba(255, 255, 255, 0.18)";
    }
});

