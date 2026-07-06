/* Energia a Confronto — Script globale */

// Toggle schede espandibili (homepage)
function toggle(row) {
  const isOpen = row.classList.contains('open');
  document.querySelectorAll('.scheda-row.open').forEach(r => r.classList.remove('open'));
  if (!isOpen) row.classList.add('open');
}

// Toggle note highlight (pagine scheda)
function toggleNote(el) {
  const note = el.querySelector('.hl-note');
  if (!note) return;
  document.querySelectorAll('.hl-note.open').forEach(n => {
    if (n !== note) n.classList.remove('open');
  });
  note.classList.toggle('open');
}

// Animazione barre mix energetico
function animateBars() {
  document.querySelectorAll('.mix-bar').forEach(bar => {
    setTimeout(() => { bar.style.width = bar.dataset.pct + '%'; }, 100);
  });
}

// Intersection Observer per animare le barre quando entrano in viewport
document.addEventListener('DOMContentLoaded', function() {
  const mixSection = document.getElementById('mixBars');
  if (mixSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateBars();
          observer.disconnect();
        }
      });
    }, { threshold: 0.3 });
    observer.observe(mixSection);
  }
});
