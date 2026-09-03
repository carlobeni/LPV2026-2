/**
 * app.js
 * Lógica del lado del cliente para consumir la API REST de FastAPI,
 * renderizar el Árbol Nodal de Cambios en SVG e interactuar con los nodos.
 */

document.addEventListener("DOMContentLoaded", () => {
    fetchStats();
    loadNodalTree();

    const scrapeForm = document.getElementById("scrape-form");
    if (scrapeForm) {
        scrapeForm.addEventListener("submit", handleScrapeSubmit);
    }
});

async function fetchStats() {
    try {
        const response = await fetch("/api/stats");
        if (!response.ok) return;
        const data = await response.json();

        document.getElementById("stat-commits").textContent = data.total_commits;
        document.getElementById("stat-authors").textContent = data.total_authors;
        document.getElementById("stat-additions").textContent = `+${data.total_additions}`;
        document.getElementById("stat-deletions").textContent = `-${data.total_deletions}`;
    } catch (err) {
        console.error("Error al obtener estadísticas:", err);
    }
}

async function loadNodalTree() {
    try {
        const response = await fetch("/api/nodal-tree");
        if (!response.ok) return;
        const treeData = await response.json();
        
        renderSVGTree(treeData);
    } catch (err) {
        console.error("Error al cargar árbol nodal:", err);
    }
}

async function handleScrapeSubmit(event) {
    event.preventDefault();
    const btnScrape = document.getElementById("btn-scrape");
    const statusBanner = document.getElementById("status-message");
    
    const repoUrl = document.getElementById("repo-url").value;
    const maxCommits = parseInt(document.getElementById("max-commits").value, 10);

    btnScrape.disabled = true;
    btnScrape.textContent = "Scrapeando Repositorio & Procesando...";
    statusBanner.className = "status-banner hidden";

    try {
        const response = await fetch("/api/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                repo_url: repoUrl,
                max_commits: maxCommits,
                use_scraperapi_proxy: false
            })
        });

        const resData = await response.json();

        if (response.ok) {
            statusBanner.className = "status-banner success";
            statusBanner.textContent = `Scraping exitoso: ${resData.scraped_commits} commits parseados y ${resData.new_commits_inserted} nuevos commits registrados.`;
            fetchStats();
            loadNodalTree();
        } else {
            statusBanner.className = "status-banner error";
            statusBanner.textContent = `Error: ${resData.detail || "Falló el scraping."}`;
        }
    } catch (err) {
        statusBanner.className = "status-banner error";
        statusBanner.textContent = "Error de red al comunicarse con el backend FastAPI.";
    } finally {
        btnScrape.disabled = false;
        btnScrape.textContent = "Ejecutar Web Scraping & Cargar BD";
    }
}

/**
 * Renderiza el árbol/grafo nodal en un lienzo SVG interactivo.
 */
function renderSVGTree(roots) {
    const svg = document.getElementById("nodal-tree-svg");
    svg.innerHTML = ""; // Limpiar contenido previo

    if (!roots || roots.length === 0) {
        svg.innerHTML = `<text x="50%" y="50%" text-anchor="middle" fill="#9ca3af" font-size="14">No existen nodos registrados en la Base de Datos. Ejecuta un scraping para poblar el árbol.</text>`;
        return;
    }

    // Aplanar todos los nodos recursivamente asignando coordenadas de posición X, Y
    const flattenedNodes = [];
    const links = [];

    let currentY = 70;
    const startX = 120;
    const stepX = 180;

    function traverseNode(node, level = 0, parentCoords = null) {
        const coords = {
            x: startX + level * stepX,
            y: currentY
        };

        flattenedNodes.push({
            data: node,
            x: coords.x,
            y: coords.y
        });

        if (parentCoords) {
            links.push({
                x1: parentCoords.x,
                y1: parentCoords.y,
                x2: coords.x,
                y2: coords.y
            });
        }

        currentY += 80;

        if (node.children && node.children.length > 0) {
            node.children.forEach(child => traverseNode(child, level + 1, coords));
        }
    }

    roots.forEach(rootNode => traverseNode(rootNode, 0));

    // Ajustar altura del SVG dinámicamente
    svg.setAttribute("height", Math.max(450, currentY + 50));

    // 1. Renderizar Enlaces (Líneas Nodal Parent-Child)
    links.forEach(link => {
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        const dx = (link.x2 - link.x1) / 2;
        const dStr = `M ${link.x1} ${link.y1} C ${link.x1 + dx} ${link.y1}, ${link.x2 - dx} ${link.y2}, ${link.x2} ${link.y2}`;
        
        path.setAttribute("d", dStr);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", "rgba(99, 102, 241, 0.5)");
        path.setAttribute("stroke-width", "2.5");
        path.setAttribute("stroke-dasharray", "4 2");
        svg.appendChild(path);
    });

    // 2. Renderizar Nodos (Círculos y Etiquetas)
    flattenedNodes.forEach(nodeObj => {
        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.style.cursor = "pointer";

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", nodeObj.x);
        circle.setAttribute("cy", nodeObj.y);
        circle.setAttribute("r", 9);
        circle.setAttribute("fill", getAuthorColor(nodeObj.data.author.username));
        circle.setAttribute("stroke", "#ffffff");
        circle.setAttribute("stroke-width", "2");
        circle.classList.add("node-circle");

        // Etiqueta de Hash
        const textHash = document.createElementNS("http://www.w3.org/2000/svg", "text");
        textHash.setAttribute("x", nodeObj.x + 16);
        textHash.setAttribute("y", nodeObj.y - 2);
        textHash.classList.add("node-label");
        textHash.textContent = `${nodeObj.data.short_hash}`;

        // Etiqueta de Autor
        const textAuthor = document.createElementNS("http://www.w3.org/2000/svg", "text");
        textAuthor.setAttribute("x", nodeObj.x + 16);
        textAuthor.setAttribute("y", nodeObj.y + 12);
        textAuthor.classList.add("node-author");
        textAuthor.textContent = `@${nodeObj.data.author.username}`;

        group.appendChild(circle);
        group.appendChild(textHash);
        group.appendChild(textAuthor);

        group.addEventListener("click", () => displayCommitDetails(nodeObj.data));
        svg.appendChild(group);
    });

    // Mostrar detalles del primer nodo por defecto
    if (flattenedNodes.length > 0) {
        displayCommitDetails(flattenedNodes[0].data);
    }
}

function displayCommitDetails(commit) {
    const detailPanel = document.getElementById("commit-detail-content");
    const formattedDate = new Date(commit.timestamp).toLocaleString("es-PY");

    detailPanel.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="commit-hash-badge">${commit.hash}</span>
            <span class="badge">${commit.parent_hash ? "Nodo Hijo" : "Nodo Raíz"}</span>
        </div>

        <h3 style="font-size:1.05rem; margin-top:0.75rem;">${escapeHtml(commit.message)}</h3>

        <div style="display:flex; align-items:center; gap:0.75rem; margin-top:0.75rem;">
            <img src="${commit.author.avatar_url}" style="width:36px; height:36px; border-radius:50%;" alt="${commit.author.username}">
            <div>
                <strong style="display:block; font-size:0.9rem;">${escapeHtml(commit.author.display_name || commit.author.username)}</strong>
                <span style="font-size:0.8rem; color:var(--text-muted);">@${commit.author.username}</span>
            </div>
        </div>

        <div style="display:flex; gap:1.5rem; margin-top:1rem; font-size:0.875rem;">
            <span>Insersiones: <strong class="text-success">+${commit.additions}</strong></span>
            <span>Eliminaciones: <strong class="text-danger">-${commit.deletions}</strong></span>
        </div>

        <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">
            Fecha UTC: ${formattedDate}
        </p>
    `;
}

function getAuthorColor(username) {
    const colors = ["#6366f1", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#06b6d4"];
    let hash = 0;
    for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
}

function escapeHtml(str) {
    return str ? str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;") : "";
}
