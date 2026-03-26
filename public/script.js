async function lastInnData() {
    try {
        // 1. Hent data fra serveren (GET er standard)
        const respons = await fetch('/api/data');
        const data = await respons.json();

        // 2. Finn boksen i HTML-en der notatene skal ligge
        const listeEl = document.getElementById('output');
        listeEl.innerHTML = ''; // Tømmer boksen så vi ikke får duplikater

        // 3. Gå gjennom hvert notat/liste og lag HTML
        data.forEach(item => {
            const kort = document.createElement('div');
            kort.className = 'card'; // Bruker CSS-stilen vi laget i stad

            if (item.type === 'notat') {
                // Hvis det er et vanlig notat
                kort.innerHTML = `
                    <h3>📌 ${item.tittel}</h3>
                    <p>${item.innhold}</p>
                    <small>${new Date(item.id).toLocaleString()}</small>
                `;
            } else {
                // Hvis det er en to-do liste (splitter tekst med komma)
                let oppgaveListe = item.oppgaver.map(o => `<li>${o.fullfort ? '✅' : '⬜'} ${o.tekst}</li>`).join('');
                kort.innerHTML = `
                    <h3>📝 ${item.tittel} (To-do)</h3>
                    <ul>${oppgaveListe}</ul>
                    <small>${new Date(item.id).toLocaleString()}</small>
                `;
            }
            listeEl.appendChild(kort);
        });
    } catch (feil) {
        console.error("Klarte ikke hente data:", feil);
    }
}

// KJØR DENNE NÅR SIDEN ÅPNES
window.onload = lastInnData;