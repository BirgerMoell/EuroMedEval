const seedDatasets = [
  { name: "entrance-al-sq", country: "AL", pretty: "Albania", native: true, format: "mcq", tier: "silver" },
  { name: "entrance-be-nl", country: "BE", pretty: "Belgium", native: true, format: "mcq", tier: "silver" },
  { name: "doatap-med-el", country: "GR", pretty: "Greece", native: true, format: "mcq", tier: "gold" },
  { name: "smdt-sv", country: "SE", pretty: "Sweden", native: true, format: "mcq", tier: "gold" },
  { name: "se-em-sv", country: "SE", pretty: "Sweden", native: true, format: "mcq", tier: "gold" },
  { name: "se-gp-sv", country: "SE", pretty: "Sweden", native: true, format: "mcq", tier: "silver" },
  { name: "pubmedqa-sv", country: "SE", pretty: "Sweden", native: false, format: "qa", tier: "bronze" },
  { name: "normedqa-no", country: "NO", pretty: "Norway", native: true, format: "mcq", tier: "gold" },
  { name: "head-qa-es", country: "ES", pretty: "Spain", native: true, format: "mcq", tier: "gold" },
  { name: "casimedicos-es", country: "ES", pretty: "Spain", native: true, format: "qa", tier: "silver" },
  { name: "frenchmedmcqa-fr", country: "FR", pretty: "France", native: true, format: "mcq", tier: "gold" },
  { name: "mediqal-fr", country: "FR", pretty: "France", native: true, format: "mcq", tier: "gold" },
  { name: "mediqal-oeq-fr", country: "FR", pretty: "France", native: true, format: "qa", tier: "gold" },
  { name: "medexpqa-fr", country: "FR", pretty: "France", native: false, format: "mcq", tier: "bronze" },
  { name: "medschool-test-it", country: "IT", pretty: "Italy", native: true, format: "mcq", tier: "gold" },
  { name: "medexpqa-it", country: "IT", pretty: "Italy", native: false, format: "mcq", tier: "bronze" },
  { name: "lek-pl", country: "PL", pretty: "Poland", native: true, format: "mcq", tier: "gold" },
  { name: "ldek-pl", country: "PL", pretty: "Poland", native: true, format: "mcq", tier: "gold" },
  { name: "pes-pl", country: "PL", pretty: "Poland", native: true, format: "mcq", tier: "gold" },
];

const revealNodes = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.16,
  }
);

revealNodes.forEach((node, index) => {
  node.style.transitionDelay = `${Math.min(index * 45, 240)}ms`;
  observer.observe(node);
});

function renderCountryBars() {
  const container = document.querySelector("#country-bars");
  if (!container) {
    return;
  }

  const byCountry = new Map();
  seedDatasets.forEach((dataset) => {
    const count = byCountry.get(dataset.country) ?? {
      country: dataset.country,
      pretty: dataset.pretty,
      total: 0,
    };
    count.total += 1;
    byCountry.set(dataset.country, count);
  });

  const rows = [...byCountry.values()].sort((left, right) => right.total - left.total);
  const maxCount = Math.max(...rows.map((row) => row.total), 1);

  container.innerHTML = rows
    .map((row) => {
      const width = `${(row.total / maxCount) * 100}%`;
      return `
        <div class="country-bar">
          <p class="country-bar-label">${row.country} · ${row.pretty}</p>
          <div class="country-bar-track">
            <div class="country-bar-fill" style="width: ${width}"></div>
          </div>
          <div class="country-bar-value">${row.total}</div>
        </div>
      `;
    })
    .join("");
}

function renderMixLegend() {
  const container = document.querySelector("#mix-legend");
  const nativeRing = document.querySelector("#native-ring");
  const formatRing = document.querySelector("#format-ring");
  if (!container || !nativeRing || !formatRing) {
    return;
  }

  const total = seedDatasets.length;
  const nativeCount = seedDatasets.filter((dataset) => dataset.native).length;
  const qaCount = seedDatasets.filter((dataset) => dataset.format === "qa").length;
  const mcqCount = total - qaCount;
  const goldCount = seedDatasets.filter((dataset) => dataset.tier === "gold").length;

  nativeRing.style.setProperty("--ring", `${(nativeCount / total) * 100}%`);
  formatRing.style.setProperty("--ring", `${(mcqCount / total) * 100}%`);

  const rows = [
    { label: "native", value: nativeCount, color: "linear-gradient(90deg, var(--accent), #f39a53)" },
    { label: "gold tier", value: goldCount, color: "linear-gradient(90deg, #1b6d78, #57aab3)" },
    { label: "mcq", value: mcqCount, color: "linear-gradient(90deg, #75291f, #e55c3d)" },
    { label: "qa", value: qaCount, color: "linear-gradient(90deg, #35576b, #8db5cc)" },
  ];

  container.innerHTML = rows
    .map((row) => {
      const width = `${(row.value / total) * 100}%`;
      return `
        <div class="mix-row">
          <div class="mix-row-label">${row.label}</div>
          <div class="mix-row-track">
            <div class="mix-row-fill" style="width: ${width}; background: ${row.color};"></div>
          </div>
          <div class="mix-row-value">${row.value}</div>
        </div>
      `;
    })
    .join("");
}

renderCountryBars();
renderMixLegend();

const hero = document.querySelector(".hero");
const orbitA = document.querySelector(".hero-orbit-a");
const orbitB = document.querySelector(".hero-orbit-b");

window.addEventListener(
  "scroll",
  () => {
    if (!hero || !orbitA || !orbitB) {
      return;
    }

    const rect = hero.getBoundingClientRect();
    const progress = Math.max(0, Math.min(1, 1 - rect.top / (window.innerHeight || 1)));
    orbitA.style.transform = `translate3d(0, ${progress * 18}px, 0) scale(${1 + progress * 0.04})`;
    orbitB.style.transform = `translate3d(0, ${progress * -14}px, 0) scale(${1 - progress * 0.03})`;
  },
  { passive: true }
);
