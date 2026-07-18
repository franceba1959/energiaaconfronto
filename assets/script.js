/* Energia a Confronto — Script globale */

// Toggle menu di navigazione mobile
function toggleMobileMenu() {
  const links = document.querySelector('.nav-links');
  const btn = document.querySelector('.nav-hamburger');
  if (!links || !btn) return;
  const isOpen = links.classList.toggle('open');
  btn.innerHTML = isOpen
    ? '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="5" x2="19" y2="19"/><line x1="19" y1="5" x2="5" y2="19"/></svg>'
    : '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
  btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
}

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
