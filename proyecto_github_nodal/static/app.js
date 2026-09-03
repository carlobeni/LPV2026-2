/**
 * app.js
 * Visualizador de Serie Temporal de Commits e Hilos Paralelos de Ramas.
 * Consume la API REST de FastAPI y renderiza la secuencia cronológica en un lienzo SVG sobrio.
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
        
        renderTimeSeriesGraph(treeData);
    } catch (err) {
        console.error("Error al cargar grafo de commits:", err);
    }
}

async function handleScrapeSubmit(event) {
    event.preventDefault();
    const btnScrape = document.getElementById("btn-scrape");
    const statusBanner = document.getElementById("status-message");
    
    const repoUrl = document.getElementById("repo-url").value;
    const maxCommits = parseInt(document.getElementById("max-commits").value, 10);

    btnScrape.disabled = true;
    btnScrape.textContent = "Analizando & Reiniciando BD...";
    statusBanner.className = "alert hidden";

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
            statusBanner.className = "alert success";
            statusBanner.textContent = `Base de Datos reiniciada. Se insertaron ${resData.new_commits_inserted} commits del repositorio ${resData.repo_url}.`;
            fetchStats();
            loadNodalTree();
        } else {
            statusBanner.className = "alert error";
            statusBanner.textContent = `Error: ${resData.detail || "Falló el procesamiento."}`;
        }
    } catch (err) {
        statusBanner.className = "alert error";
        statusBanner.textContent = "Error de red al comunicarse con el backend FastAPI.";
    } finally {
        btnScrape.disabled = false;
        btnScrape.textContent = "Analizar & Cargar Repositorio";
    }
}

/**
 * Renderiza la Serie Temporal y los Hilos Paralelos de Ramas en el lienzo SVG.
 */
function renderTimeSeriesGraph(roots) {
    const svg = document.getElementById("timeline-svg");
    if (!svg) return;
    svg.innerHTML = "";
    const detailPanel = document.getElementById("commit-detail-content");

    if (!roots || roots.length === 0) {
        svg.innerHTML = `<text x="50%" y="50%" text-anchor="middle" fill="#94a3b8" font-size="13">No hay ningún repositorio cargado. Ingrese una URL arriba y presione 'Analizar & Cargar Repositorio'.</text>`;
        if (detailPanel) {
            detailPanel.innerHTML = `<p class="placeholder-text">Ingresa una URL de GitHub arriba y ejecuta el análisis para visualizar el grafo nodal de cambios.</p>`;
        }
        return;
    }

    // 1. Aplanar los nodos recursivamente
    const allNodesList = [];
    function flatten(node) {
        allNodesList.push(node);
        if (node.children && node.children.length > 0) {
            node.children.forEach(flatten);
        }
    }
    roots.forEach(flatten);

    // 2. Ordenar cronológicamente (Serie Temporal X-axis)
    allNodesList.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    // 3. Extraer ramas únicas para calcular los hilos paralelos (Y-axis)
    const branches = Array.from(new Set(allNodesList.map(n => n.branch || "main")));
    // Asegurar que 'main' o 'master' esté en el hilo principal 0
    branches.sort((a, b) => (a === "main" || a === "master" ? -1 : 1));

    const branchLanes = {};
    const laneHeight = 85;
    const startY = 75;

    branches.forEach((bName, index) => {
        branchLanes[bName] = startY + index * laneHeight;
    });

    // Configuración del espacio de la Serie Temporal
    const wrapper = document.getElementById("svg-wrapper");
    const containerWidth = wrapper ? wrapper.clientWidth : 750;

    const marginX = 120;
    const availableWidth = Math.max(300, containerWidth - marginX * 2);
    const stepX = allNodesList.length > 1 
        ? Math.max(110, availableWidth / (allNodesList.length - 1))
        : 150;

    // Asignar coordenadas X, Y a cada nodo
    const nodesMapByHash = {};
    allNodesList.forEach((node, idx) => {
        const posX = marginX + idx * stepX;
        const posY = branchLanes[node.branch || "main"] || startY;
        
        nodesMapByHash[node.hash] = {
            data: node,
            x: posX,
            y: posY
        };
    });

    const totalWidth = Math.max(containerWidth, marginX * 2 + (allNodesList.length - 1) * stepX + 60);
    const totalHeight = Math.max(460, startY + branches.length * laneHeight + 50);
    svg.setAttribute("width", totalWidth);
    svg.setAttribute("height", totalHeight);

    // 4. Dibujar Hilos Paralelos de Guias de Ramas (Parallel Swimlanes)
    branches.forEach(bName => {
        const laneY = branchLanes[bName];

        // Linea guía horizontal de la rama
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", 30);
        line.setAttribute("y1", laneY);
        line.setAttribute("x2", totalWidth - 40);
        line.setAttribute("y2", laneY);
        line.setAttribute("stroke", "#334155");
        line.setAttribute("stroke-dasharray", "4 4");
        line.setAttribute("stroke-width", "1");
        svg.appendChild(line);

        // Etiqueta de la Rama en el margen izquierdo
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", 25);
        label.setAttribute("y", laneY - 10);
        label.setAttribute("fill", getBranchColor(bName));
        label.setAttribute("font-size", "11px");
        label.setAttribute("font-family", "var(--font-mono)");
        label.setAttribute("font-weight", "600");
        label.textContent = `[rama: ${bName}]`;
        svg.appendChild(label);
    });

    // 5. Dibujar Conexiones de Padres a Hijos (Arcos/Rutas SVG entre Hilos)
    allNodesList.forEach(node => {
        const currObj = nodesMapByHash[node.hash];
        if (node.parent_hash && nodesMapByHash[node.parent_hash]) {
            const parentObj = nodesMapByHash[node.parent_hash];

            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            const dx = (currObj.x - parentObj.x) / 2;
            const pathD = `M ${parentObj.x} ${parentObj.y} C ${parentObj.x + dx} ${parentObj.y}, ${currObj.x - dx} ${currObj.y}, ${currObj.x} ${currObj.y}`;
            
            path.setAttribute("d", pathD);
            path.setAttribute("fill", "none");
            path.setAttribute("stroke", getBranchColor(node.branch || "main"));
            path.setAttribute("stroke-width", "2");
            path.setAttribute("opacity", "0.7");
            svg.appendChild(path);
        }
    });

    // 6. Dibujar Nodos de Commits (Circulos y Etiquetas sobre la Serie Temporal)
    allNodesList.forEach(node => {
        const nodeObj = nodesMapByHash[node.hash];

        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.style.cursor = "pointer";

        // Círculo del commit
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", nodeObj.x);
        circle.setAttribute("cy", nodeObj.y);
        circle.setAttribute("r", 7);
        circle.setAttribute("fill", getAuthorColor(node.author.username));
        circle.setAttribute("stroke", "#ffffff");
        circle.setAttribute("stroke-width", "1.5");
        circle.classList.add("commit-node");

        // Etiqueta de Hash corto
        const textHash = document.createElementNS("http://www.w3.org/2000/svg", "text");
        textHash.setAttribute("x", nodeObj.x);
        textHash.setAttribute("y", nodeObj.y - 14);
        textHash.setAttribute("text-anchor", "middle");
        textHash.classList.add("commit-text");
        textHash.textContent = node.short_hash;

        // Etiqueta de Autor
        const textAuthor = document.createElementNS("http://www.w3.org/2000/svg", "text");
        textAuthor.setAttribute("x", nodeObj.x);
        textAuthor.setAttribute("y", nodeObj.y + 20);
        textAuthor.setAttribute("text-anchor", "middle");
        textAuthor.classList.add("commit-author-text");
        textAuthor.textContent = `@${node.author.username}`;

        group.appendChild(circle);
        group.appendChild(textHash);
        group.appendChild(textAuthor);

        group.addEventListener("click", () => displayCommitDetails(node));
        svg.appendChild(group);
    });

    // Eje de Tiempo (Timeline X-Axis) al pie
    const timeAxisY = totalHeight - 30;
    const axisLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axisLine.setAttribute("x1", 30);
    axisLine.setAttribute("y1", timeAxisY);
    axisLine.setAttribute("x2", totalWidth - 40);
    axisLine.setAttribute("y2", timeAxisY);
    axisLine.setAttribute("stroke", "#475569");
    axisLine.setAttribute("stroke-width", "1");
    svg.appendChild(axisLine);

    const axisLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    axisLabel.setAttribute("x", 30);
    axisLabel.setAttribute("y", timeAxisY + 18);
    axisLabel.setAttribute("fill", "#64748b");
    axisLabel.setAttribute("font-size", "10px");
    axisLabel.setAttribute("font-family", "var(--font-mono)");
    axisLabel.textContent = "Eje Cronológico de Serie Temporal (Secuencia Histórica de Cambios →)";
    svg.appendChild(axisLabel);

    // Mostrar detalles del primer nodo por defecto
    if (allNodesList.length > 0) {
        displayCommitDetails(allNodesList[0]);
    }
}

function displayCommitDetails(commit) {
    const detailPanel = document.getElementById("commit-detail-content");
    const formattedDate = new Date(commit.timestamp).toLocaleString("es-PY");

    detailPanel.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="badge-code">${commit.hash}</span>
            <span class="tag">Rama: ${escapeHtml(commit.branch)}</span>
        </div>

        <h3 style="font-size:0.95rem; margin-top:0.6rem; color:var(--text-primary);">${escapeHtml(commit.message)}</h3>

        <div style="display:flex; align-items:center; gap:0.6rem; margin-top:0.6rem;">
            <img src="${commit.author.avatar_url}" style="width:30px; height:30px; border-radius:50%;" alt="${commit.author.username}">
            <div>
                <strong style="display:block; font-size:0.85rem; color:var(--text-primary);">${escapeHtml(commit.author.display_name || commit.author.username)}</strong>
                <span style="font-size:0.75rem; color:var(--text-secondary);">@${commit.author.username}</span>
            </div>
        </div>

        <div style="display:flex; gap:1.2rem; margin-top:0.8rem; font-size:0.85rem; font-family:var(--font-mono);">
            <span>Inserciones: <strong style="color:var(--accent-green);">+${commit.additions}</strong></span>
            <span>Eliminaciones: <strong style="color:var(--accent-red);">-${commit.deletions}</strong></span>
        </div>

        <p style="font-size:0.75rem; color:var(--text-secondary); margin-top:0.4rem;">
            Commit Padre: <code class="badge-code">${commit.parent_hash ? commit.parent_hash.substring(0, 7) : 'Nodo Raíz'}</code>
        </p>
        <p style="font-size:0.75rem; color:var(--text-secondary); margin-top:0.2rem;">
            Fecha UTC: ${formattedDate}
        </p>
    `;
}

function getBranchColor(branchName) {
    if (branchName === "main" || branchName === "master") return "#3b82f6"; // Azul
    if (branchName.includes("pydantic") || branchName.includes("feature")) return "#10b981"; // Verde
    if (branchName.includes("scraper")) return "#8b5cf6"; // Violeta
    return "#f59e0b"; // Naranja
}

function getAuthorColor(username) {
    const colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899", "#06b6d4"];
    let hash = 0;
    for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
}

function escapeHtml(str) {
    return str ? str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;") : "";
}
