/*
====================================================
AK-Shop Warenkorb
Zentrale Warenkorb-Logik
LocalStorage-Key: ak_cart
====================================================
*/

window.AKCart = (function () {

    const STORAGE_KEY = "ak_cart";

    /*
    ------------------------------------------
    Warenkorb laden
    ------------------------------------------
    */
    function getCart() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
        } catch (e) {
            return [];
        }
    }

    /*
    ------------------------------------------
    Warenkorb speichern
    ------------------------------------------
    */
    function saveCart(cart) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
        updateHeaderCartCount();
    }

    /*
    ------------------------------------------
    Prüfen ob Artikel vorhanden
    ------------------------------------------
    */
    function isInCart(id) {
        const cart = getCart();

        return cart.some(item =>
            String(item.id) === String(id)
        );
    }

    /*
    ------------------------------------------
    Artikel hinzufügen
    ------------------------------------------
    */
    function addToCart(item) {

        let cart = getCart();

        if (isInCart(item.id)) {
            return false;
        }

        cart.push(item);

        saveCart(cart);

        showToast("Artikel zum Warenkorb hinzugefügt");

        return true;
    }

    /*
    ------------------------------------------
    Artikel entfernen
    ------------------------------------------
    */
    function removeFromCart(id) {

        let cart = getCart();

        cart = cart.filter(item =>
            String(item.id) !== String(id)
        );

        saveCart(cart);
    }

    /*
    ------------------------------------------
    Zähler im Header
    ------------------------------------------
    */
    function updateHeaderCartCount() {

        const counter =
            document.getElementById("cartCount");

        if (!counter) {
            return;
        }

        counter.textContent =
            getCart().length;
    }

    /*
    ------------------------------------------
    Toast-Nachricht
    ------------------------------------------
    */
    function showToast(message) {

        let toast =
            document.getElementById("akToast");

        if (!toast) {

            toast = document.createElement("div");
            toast.id = "akToast";

            toast.style.position = "fixed";
            toast.style.bottom = "20px";
            toast.style.right = "20px";
            toast.style.background = "#7a4d24";
            toast.style.color = "#fff";
            toast.style.padding = "12px 18px";
            toast.style.borderRadius = "8px";
            toast.style.zIndex = "9999";
            toast.style.boxShadow =
                "0 4px 12px rgba(0,0,0,.25)";

            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.style.display = "block";

        setTimeout(() => {
            toast.style.display = "none";
        }, 2500);
    }

    /*
    ------------------------------------------
    Produktseite initialisieren
    ------------------------------------------
    */
    function initProductPage(config) {

        const button =
            document.getElementById(config.buttonId);

        if (!button) {
            return;
        }

        if (isInCart(config.id)) {

            button.disabled = true;
            button.innerText =
                "✔ Bereits im Warenkorb";

            return;
        }

        button.addEventListener("click", () => {

            const added = addToCart({
                id: config.id,
                title: config.title,
                price: config.price
            });

            if (added) {

                button.disabled = true;

                button.innerText =
                    "✔ Bereits im Warenkorb";

                const feedback =
                    document.getElementById("cart-feedback");

                if (feedback) {
                    feedback.classList.remove("hidden");
                }
            }
        });
    }

    /*
    ------------------------------------------
    Warenkorbseite rendern
    ------------------------------------------
    */
    function renderCartPage(containerId) {

        const container =
            document.getElementById(containerId);

        if (!container) {
            return;
        }

        const cart = getCart();

        if (cart.length === 0) {

            container.innerHTML = `
                <div class="empty-cart">
                    <p>Ihr Warenkorb ist derzeit leer.</p>
                    <a href="/katalog">
                        ← Zum Katalog
                    </a>
                </div>
            `;

            return;
        }

        let html = "";

        cart.forEach(item => {

            html += `
                <div class="cart-item">
                    <h3>${item.title}</h3>

                    <p>Artikelnummer:
                    ${item.id}</p>

                    <p>${item.price} €</p>

                    <button
                        onclick="AKCart.removeAndRefresh('${item.id}')">
                        Entfernen
                    </button>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    /*
    ------------------------------------------
    Entfernen + neu rendern
    ------------------------------------------
    */
    function removeAndRefresh(id) {

        removeFromCart(id);

        renderCartPage("cart-content");
    }

    /*
    ------------------------------------------
    Initialisierung
    ------------------------------------------
    */
    document.addEventListener(
        "DOMContentLoaded",
        function () {
            updateHeaderCartCount();
        }
    );

    return {

        getCart,
        saveCart,
        addToCart,
        removeFromCart,
        removeAndRefresh,
        isInCart,
        updateHeaderCartCount,
        showToast,
        initProductPage,
        renderCartPage

    };

})();