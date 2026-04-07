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
