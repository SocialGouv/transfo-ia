/* Diaporama : dépliage des slides, cadre, navigation, notes, planche de contrôle.
   Fichier technique : ne pas le lire ni le modifier pour faire un deck.
   Clavier : flèches ou espace pour avancer · F plein écran · N notes · P imprimer.
   Adresses utiles : deck.html?planche (toutes les slides sur une page, débordements signalés en rouge),
   deck.html?controle (navigation normale, débordements signalés), deck.html?shot (sans aide ni barre). */
(() => {
  const SPRITE = '<svg class="sprite" aria-hidden="true" focusable="false"><symbol id="i-alert" viewBox="0 0 24 24"><path d="m12.866 3 9.526 16.5a1 1 0 0 1-.866 1.5H2.474a1 1 0 0 1-.866-1.5L11.134 3a1 1 0 0 1 1.732 0Zm-8.66 16h15.588L12 5.5 4.206 19ZM11 16h2v2h-2v-2Zm0-7h2v5h-2V9Z"/></symbol><symbol id="i-arrow-down" viewBox="0 0 24 24"><path d="m13 16.172 5.364-5.364 1.414 1.414L12 20l-7.778-7.778 1.414-1.414L11 16.172V4h2v12.172Z"/></symbol><symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="m16.172 11-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2h12.172Z"/></symbol><symbol id="i-award" viewBox="0 0 24 24"><path d="M12 1.001a8 8 0 0 1 5 14.245v6.871a.5.5 0 0 1-.757.429L12 20l-4.243 2.546a.5.5 0 0 1-.757-.43v-6.87a8 8 0 0 1 5-14.245Zm3 15.417A7.978 7.978 0 0 1 12 17a7.978 7.978 0 0 1-3-.582v3.05l3-1.8 3 1.8v-3.05ZM12 3a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z"/></symbol><symbol id="i-check" viewBox="0 0 24 24"><path d="m10 15.172 9.192-9.193 1.415 1.414L10 18l-6.364-6.364 1.414-1.414 4.95 4.95Z"/></symbol><symbol id="i-cloud-off" viewBox="0 0 24 24"><path d="M3.51472 2.10051L22.6066 21.1924L21.1924 22.6066L19.1782 20.5924C18.503 20.8556 17.7684 21 17 21H7C3.68629 21 1 18.3137 1 15C1 12.3846 2.67346 10.16 5.00804 9.33857C5.0027 9.22639 5 9.11351 5 9C5 8.22228 5.12683 7.47418 5.36094 6.77527L2.10051 3.51472L3.51472 2.10051ZM7 9C7 9.08147 7.00193 9.16263 7.00578 9.24344L7.07662 10.7309L5.67183 11.2252C4.0844 11.7837 3 13.2889 3 15C3 17.2091 4.79086 19 7 19H17C17.1858 19 17.3687 18.9873 17.5478 18.9628L7.03043 8.44519C7.01032 8.62736 7 8.81247 7 9ZM12 2C15.866 2 19 5.13401 19 9C19 9.11351 18.9973 9.22639 18.992 9.33857C21.3265 10.16 23 12.3846 23 15C23 16.0883 22.7103 17.1089 22.2037 17.9889L20.7111 16.4955C20.8974 16.0335 21 15.5287 21 15C21 12.79 19.21 11 17 11C16.4711 11 15.9661 11.1027 15.5039 11.2892L14.0111 9.7964C14.8912 9.28978 15.9118 9 17 9C17 6.23858 14.7614 4 12 4C10.9295 4 9.93766 4.33639 9.12428 4.90922L7.69418 3.48056C8.88169 2.55284 10.3763 2 12 2Z"/></symbol><symbol id="i-code" viewBox="0 0 24 24"><path d="m24 12-5.657 5.657-1.414-1.414L21.172 12l-4.243-4.243 1.414-1.414L24 12ZM2.828 12l4.243 4.243-1.414 1.414L0 12l5.657-5.657L7.07 7.757 2.828 12Zm6.96 9H7.66l6.552-18h2.128L9.788 21Z"/></symbol><symbol id="i-compasses" viewBox="0 0 24 24"> <path d="M16.3303 13.4969C17.9562 12.215 19 10.2277 19 7.99658H21C21 10.9686 19.5595 13.6042 17.3385 15.2431L19.8661 19.621C20.4183 20.5775 20.0906 21.8007 19.134 22.353L15.6073 16.2446C14.5029 16.7282 13.2828 16.9966 12 16.9966C10.7172 16.9966 9.49712 16.7282 8.39278 16.2446L4.86606 22.353C3.90947 21.8007 3.58172 20.5775 4.13401 19.621L9.19751 10.8507C8.45844 10.1249 8.00003 9.11427 8.00003 7.99658C8.00003 6.13274 9.2748 4.56664 11 4.1226V1.99658H13V4.1226C14.7253 4.56664 16 6.13274 16 7.99658C16 9.11427 15.5416 10.1249 14.8025 10.8507L16.3303 13.4969ZM14.599 14.4982L13.071 11.8516C12.7302 11.9461 12.371 11.9966 12 11.9966C11.6291 11.9966 11.2699 11.9461 10.929 11.8516L9.40101 14.4982C10.2046 14.8197 11.0817 14.9966 12 14.9966C12.9184 14.9966 13.7955 14.8197 14.599 14.4982ZM12 9.99658C13.1046 9.99658 14 9.10115 14 7.99658C14 6.89201 13.1046 5.99658 12 5.99658C10.8955 5.99658 10 6.89201 10 7.99658C10 9.10115 10.8955 9.99658 12 9.99658Z"/> </symbol><symbol id="i-computer" viewBox="0 0 24 24"><path d="M21.008 3c.548 0 .992.449.992 1.007v12.986c0 .556-.455 1.007-.992 1.007H13v2h4v2H7v-2h4v-2H2.992A.998.998 0 0 1 2 16.993V4.007C2 3.451 2.455 3 2.992 3h18.016ZM20 5H4v11h16V5Z"/></symbol><symbol id="i-eye-off" viewBox="0 0 24 24"><path d="M17.882 19.297A10.949 10.949 0 0 1 12 21c-5.392 0-9.878-3.88-10.819-9a10.982 10.982 0 0 1 3.34-6.066L1.392 2.808l1.415-1.415 19.799 19.8-1.415 1.414-3.31-3.31h.001ZM5.935 7.35A8.965 8.965 0 0 0 3.223 12a9.005 9.005 0 0 0 13.201 5.838l-2.028-2.028A4.5 4.5 0 0 1 8.19 9.604L5.935 7.35Zm6.979 6.978-3.242-3.242a2.5 2.5 0 0 0 3.241 3.241l.001.001Zm7.893 2.264-1.431-1.43A8.935 8.935 0 0 0 20.777 12 9.005 9.005 0 0 0 9.552 5.338L7.974 3.76C9.221 3.27 10.58 3 12 3c5.392 0 9.878 3.88 10.819 9a10.947 10.947 0 0 1-2.012 4.592Zm-9.084-9.084a4.5 4.5 0 0 1 4.769 4.769l-4.77-4.769h.001Z"/></symbol><symbol id="i-flashlight" viewBox="0 0 24 24"><path d="M13 0v9h8L11 24v-9H4l9-15Zm-2 7.22L7.532 13H13v4.394L17.263 11H11V7.22Z"/></symbol><symbol id="i-palette" viewBox="0 0 24 24"><path d="M12 2c5.522 0 10 3.978 10 8.889a5.558 5.558 0 0 1-5.556 5.555h-1.966c-.922 0-1.667.745-1.667 1.667 0 .422.167.811.422 1.1.267.3.434.689.434 1.122C13.667 21.256 12.9 22 12 22 6.478 22 2 17.522 2 12S6.478 2 12 2Zm0 2a8 8 0 0 0-.676 15.972 3.648 3.648 0 0 1-.513-1.86v-.001a3.664 3.664 0 0 1 3.667-3.667h1.966A3.558 3.558 0 0 0 20 10.89C20 7.139 16.468 4 12 4ZM7.5 9a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm9 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 6a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/></symbol><symbol id="i-refresh" viewBox="0 0 24 24"><path d="M5.46 4.43a10 10 0 0 1 14.73 13.3L17 12.01h3A8 8 0 0 0 6.46 6.23l-1-1.8zm13.08 15.14A10 10 0 0 1 3.8 6.27L7 11.99H4a8 8 0 0 0 13.54 5.77l1 1.8z"/></symbol><symbol id="i-scales" viewBox="0 0 24 24"><path d="M13 2v1.278l5 1.668 3.632-1.21.633 1.896-3.032 1.011 3.096 8.512A5.986 5.986 0 0 1 18 17a5.985 5.985 0 0 1-4.329-1.845l3.094-8.512L13 5.387V19h4v2H7v-2h4V5.387L7.232 6.643l3.096 8.512A5.982 5.982 0 0 1 6 17a5.985 5.985 0 0 1-4.329-1.845l3.094-8.512-3.03-1.01.633-1.898L6 4.945l5-1.667V2h2Zm5 7.103-1.958 5.386A3.975 3.975 0 0 0 18 15c.7 0 1.37-.18 1.958-.51L18 9.102v.001Zm-12 0-1.958 5.386A3.975 3.975 0 0 0 6 15c.7 0 1.37-.18 1.958-.51L6 9.102v.001Z"/></symbol><symbol id="i-server" viewBox="0 0 24 24"><path d="M20 3a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h16Zm-1 10H5v6h14v-6Zm-9 2v2H7v-2h3Zm9-10H5v6h14V5Zm-9 2v2H7V7h3Z"/></symbol><symbol id="i-settings" viewBox="0 0 24 24"><path d="M14.06 2.213c-.13 1.11.237 2.08 1.001 2.396.765.317 1.71-.108 2.403-.986a9.945 9.945 0 0 1 2.913 2.913c-.877.692-1.303 1.638-.986 2.403.317.765 1.286 1.132 2.396 1.001a9.945 9.945 0 0 1 0 4.12c-1.11-.13-2.08.237-2.396 1.001-.317.765.108 1.71.986 2.403a9.945 9.945 0 0 1-2.913 2.913c-.692-.877-1.638-1.303-2.403-.986-.765.317-1.132 1.286-1.001 2.396a9.945 9.945 0 0 1-4.12 0c.13-1.11-.237-2.08-1.001-2.396-.765-.317-1.71.108-2.403.986a9.945 9.945 0 0 1-2.913-2.913c.877-.692 1.303-1.638.986-2.403-.317-.765-1.286-1.132-2.396-1.001a9.945 9.945 0 0 1 0-4.12c1.11.13 2.08-.237 2.396-1.001.317-.765-.108-1.71-.986-2.403a9.945 9.945 0 0 1 2.913-2.913c.692.877 1.638 1.303 2.403.986.765-.317 1.132-1.286 1.001-2.396a9.945 9.945 0 0 1 4.12 0ZM11.79 4c-.305 1.1-1.002 2.007-2.086 2.457-1.085.449-2.22.3-3.212-.262a6.932 6.932 0 0 0-.297.297c.562.993.71 2.127.262 3.212C6.007 10.788 5.1 11.485 4 11.79c-.004.14-.004.28 0 .42 1.1.305 2.007 1.002 2.457 2.086.449 1.085.3 2.22-.262 3.212.096.102.195.201.297.297.993-.562 2.127-.71 3.212-.262 1.084.45 1.781 1.357 2.086 2.457.14.004.28.004.42 0 .305-1.1 1.002-2.007 2.086-2.457 1.085-.449 2.22-.3 3.212.262.102-.096.201-.195.297-.297-.562-.993-.71-2.127-.262-3.212.45-1.084 1.357-1.781 2.457-2.086.004-.14.004-.28 0-.42-1.1-.305-2.007-1.002-2.457-2.086-.449-1.085-.3-2.22.262-3.212a7.935 7.935 0 0 0-.297-.297c-.993.562-2.127.71-3.212.262C13.212 6.007 12.515 5.1 12.21 4a7.935 7.935 0 0 0-.42 0ZM12 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2Z"/></symbol><symbol id="i-shield" viewBox="0 0 24 24"><path d="m12 1 8.217 1.826a1 1 0 0 1 .783.976v9.987a6 6 0 0 1-2.672 4.992L12 23l-6.328-4.219A6 6 0 0 1 3 13.79V3.802a1 1 0 0 1 .783-.976L12 1Zm0 2.05L5 4.604v9.185a4 4 0 0 0 1.781 3.328L12 20.597l5.219-3.48A4 4 0 0 0 19 13.79V4.604L12 3.05Z"/></symbol><symbol id="i-team" viewBox="0 0 24 24"><path d="M12 11a5 5 0 0 1 5 5v6h-2v-6a3 3 0 0 0-2.824-2.995L12 13a3 3 0 0 0-2.995 2.824L9 16v6H7v-6a5 5 0 0 1 5-5Zm-6.5 3c.279 0 .55.033.81.094a5.947 5.947 0 0 0-.301 1.575L6 16v.086a1.492 1.492 0 0 0-.356-.08L5.5 16a1.5 1.5 0 0 0-1.493 1.356L4 17.5V22H2v-4.5A3.5 3.5 0 0 1 5.5 14Zm13 0a3.5 3.5 0 0 1 3.5 3.5V22h-2v-4.5a1.5 1.5 0 0 0-1.356-1.493L18.5 16c-.175 0-.343.03-.5.085V16c0-.666-.108-1.306-.309-1.904A3.42 3.42 0 0 1 18.5 14Zm-13-6a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5Zm13 0a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5Zm-13 2a.5.5 0 1 0 0 1 .5.5 0 0 0 0-1Zm13 0a.5.5 0 1 0 0 1 .5.5 0 0 0 0-1ZM12 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8Zm0 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z"/></symbol><symbol id="i-user" viewBox="0 0 24 24"><path d="M12 14a8 8 0 0 1 8 8h-2a6 6 0 1 0-12 0H4a8 8 0 0 1 8-8Zm0-13c3.315 0 6 2.685 6 6s-2.685 6-6 6-6-2.685-6-6 2.685-6 6-6Zm0 2C9.79 3 8 4.79 8 7s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4Z"/></symbol><symbol id="i-links" viewBox="0 0 24 24"><path d="m12.89 7.939 1.414 1.415a7 7 0 0 1 0 9.9l-.354.353a7 7 0 0 1-9.9-9.9l1.415 1.415a5 5 0 1 0 7.071 7.07l.354-.353a5 5 0 0 0 0-7.07l-1.415-1.415L12.89 7.94v-.001Zm6.717 6.01-1.414-1.413a5 5 0 1 0-7.07-7.071l-.355.354a5 5 0 0 0 0 7.07l1.415 1.415-1.415 1.414-1.414-1.414a7 7 0 0 1 0-9.9l.354-.353a7 7 0 1 1 9.9 9.9v-.001Z"/></symbol><symbol id="i-go-back" viewBox="0 0 24 24"><path d="m5.828 7 2.536 2.536L6.95 10.95 2 6l4.95-4.95 1.414 1.414L5.828 5H13a8 8 0 1 1 0 16H4v-2h9a6 6 0 1 0 0-12H5.828Z"/></symbol><symbol id="i-roadmap" viewBox="0 0 24 24"><path d="M21.775 4.341A.5.5 0 0 1 22 4.76V19l-7 3-6-3-6.303 2.701a.5.5 0 0 1-.697-.46V7l2-.857v12.824l5.065-2.17 6 3L20 17.68V4.857l1.303-.558a.5.5 0 0 1 .472.042Zm-5.532-1.583a6 6 0 0 1 0 8.485L12 15.485l-4.243-4.242a6 6 0 0 1 8.486-8.485ZM12 2.999a4 4 0 0 0-2.828 6.829L12 12.657l2.828-2.829A4 4 0 0 0 12 2.999Z"/></symbol><symbol id="i-line-chart" viewBox="0 0 24 24"><path d="M5 3v16h16v2H3V3h2Zm15.293 3.293 1.414 1.414L16 13.414l-3-2.999-4.293 4.292-1.414-1.414L13 7.586l3 2.999 4.293-4.292Z"/></symbol></svg>';
  document.body.insertAdjacentHTML('afterbegin', SPRITE);

  const meta = n => (document.querySelector(`meta[name="${n}"]`)?.content || '').trim();
  const params = new URLSearchParams(location.search);
  const planche = params.has('planche');
  const controle = planche || params.has('controle');
  const shot = params.has('shot') || planche;
  const stage = document.querySelector('.stage');
  const slides = Array.from(stage.querySelectorAll(':scope > section'));
  const total = slides.length;
  const deckTitle = document.title;
  const HORS_CADRE = ['couverture', 'conclusion'];
  let cur = -1;

  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const panel = el('div', 'notes-panel'); panel.id = 'notes-panel'; panel.hidden = true; panel.setAttribute('aria-live', 'polite');
  const annonce = el('p', 'sr'); annonce.id = 'annonce'; annonce.setAttribute('aria-live', 'polite');
  document.body.append(panel, annonce);
  const marque = (meta('deck-marque') || 'République / Française').split('/').map(s => s.trim()).filter(Boolean);
  const pied = meta('deck-pied');
  const temps = meta('deck-fil').split('|').map(s => s.trim()).filter(Boolean);

  function poserMarque(p) {
    p.classList.add('bm');
    p.textContent = '';
    marque.forEach((ligne, i) => { if (i) p.append(document.createElement('br')); p.append(ligne); });
  }
  function poserPied(span) {
    span.textContent = '';
    const i = pied.indexOf(' · ');
    if (i < 0) { span.append(el('strong', '', pied)); return; }
    span.append(el('strong', '', pied.slice(0, i)), pied.slice(i));
  }

  /* Dépliage. Une slide s'écrit en écriture courte : des emplacements (data-slot), des éléments répétés
     (data-item), des notes (data-note). On construit ici la structure que les styles attendent ;
     ce qui n'est ni emplacement, ni élément, ni note n'est pas affiché. */
  const svg = nom => `<svg class="ico"><use href="#${nom}"/></svg>`;
  function deplier(s) {
    const src = el('div');
    src.append(...s.childNodes);
    const E = (tag, cls, ...enfants) => { const e = el(tag, cls); e.append(...enfants.flat(Infinity).filter(Boolean)); return e; };
    const attr = (e, nom, valeur = '') => { e.setAttribute(nom, valeur); return e; };
    const slot = (dans, nom, tag, cls) => Array.from(dans.querySelectorAll(`[data-slot="${nom}"]`))
      .filter(e => dans !== src || !e.closest('[data-item]'))
      .map(e => { const n = el(tag, cls); n.dataset.slot = nom; n.append(...e.childNodes); return n; });
    const items = (nom, tag, cls, contenu) => Array.from(src.querySelectorAll(`[data-item="${nom}"]`)).map(it => {
      const n = E(tag, cls, contenu(it));
      n.dataset.item = nom;
      if (it.dataset.ton) n.dataset.ton = it.dataset.ton;
      if (it.dataset.valeur != null) n.dataset.valeur = it.dataset.valeur;
      if (it.hasAttribute('data-retenir')) n.setAttribute('data-retenir', '');
      return n;
    });
    /* Graphiques : le nombre tracé vient de data-valeur ; l'axe part de zéro. */
    const nombre = e => Math.max(0, parseFloat(String(e.dataset.valeur || '').replace(/\s/g, '').replace(',', '.')) || 0);
    const parts = liste => { const max = Math.max(0, ...liste.map(nombre)) || 1; return liste.map(e => nombre(e) / max); };
    const icone = (it, cls) => { const sp = attr(el('span', cls), 'aria-hidden', 'true'); sp.innerHTML = svg(it.dataset.icone || 'i-check'); return sp; };
    const tete = () => [slot(src, 'titre', 'h2', 'title'), slot(src, 'chapo', 'p', 's-lead')];
    const corps = (cls, ...enfants) => E('div', cls ? `s-body ${cls}` : 's-body', enfants);
    const marqueVide = () => attr(el('p'), 'data-marque');
    const B = {
      couverture: () => {
        s.classList.add('split', 'cover');
        return [
          E('div', 'cover__main', marqueVide(),
            E('div', 'cover__heading', slot(src, 'surtitre', 'p', 'cover__kicker'), slot(src, 'titre', 'h1', 'cover__title'), slot(src, 'accroche', 'p', 'cover__lead')),
            attr(el('div', 'cover__rule'), 'aria-hidden', 'true'),
            slot(src, 'auteur', 'p', 'cover__name'), slot(src, 'fonction', 'p', 'cover__role')),
          E('div', 'cover__aside', slot(src, 'plan-intitule', 'p', 'label'),
            E('ol', 'plan', items('temps', 'li', '', it => E('div', '', slot(it, 'temps-titre', 'strong'), slot(it, 'temps-texte', 'p'))))),
        ];
      },
      enonce: () => corps('c-enonce', slot(src, 'titre', 'h2'), slot(src, 'appui', 'p')),
      section: () => corps('c-section', slot(src, 'numero', 'p', 'c-section__n'), E('div', '', slot(src, 'titre', 'h2'), slot(src, 'chapo', 'p'))),
      chiffres: () => [tete(), corps('', E('ul', 'c-chiffres', items('chiffre', 'li', '', it =>
        [slot(it, 'valeur', 'p', 'c-chiffres__val'), slot(it, 'libelle', 'p', 'c-chiffres__lib'), slot(it, 'detail', 'p', 'c-chiffres__det')])))],
      cartes: () => [tete(), corps('', E('ul', 'c-cartes', items('carte', 'li', '', it =>
        [icone(it, 'sq'), slot(it, 'carte-titre', 'h3'), slot(it, 'carte-texte', 'p')])))],
      contraste: () => {
        const cotes = items('cote', 'div', 'c-contraste__cote', it =>
          [slot(it, 'etiquette', 'p', 'tag'), slot(it, 'cote-titre', 'h3'), E('ul', '', slot(it, 'point', 'li'))]);
        const fleche = attr(el('span', 'c-contraste__fleche'), 'aria-hidden', 'true');
        fleche.innerHTML = svg('i-arrow-right');
        return [tete(), corps('', E('div', 'c-contraste', cotes[0], cotes.length > 1 ? fleche : null, cotes.slice(1)))];
      },
      etapes: () => [tete(), corps('', E('ol', 'c-etapes', items('etape', 'li', '', it =>
        [slot(it, 'etape-titre', 'h3'), slot(it, 'etape-texte', 'p')])))],
      liste: () => [tete(), corps('', E('ul', 'c-liste', items('ligne', 'li', '', it =>
        [icone(it, 'c-liste__ico'), E('div', '', slot(it, 'ligne-titre', 'strong'), slot(it, 'ligne-texte', 'p'))])))],
      tableau: () => {
        const entetes = slot(src, 'entete', 'th').map(th => attr(th, 'scope', 'col'));
        const rangees = items('rangee', 'tr', '', it => slot(it, 'cellule', 'td').map((td, k) => {
          if (k) return td;
          const th = attr(el('th'), 'scope', 'row'); th.dataset.slot = 'cellule'; th.append(...td.childNodes); return th;
        }));
        return [tete(), corps('', E('div', 'c-tableau', E('table', '', E('thead', '', E('tr', '', entetes)), E('tbody', '', rangees))))];
      },
      frise: () => [tete(), corps('', E('ol', 'c-frise', items('jalon', 'li', '', it =>
        [slot(it, 'jalon-date', 'p', 'c-frise__date'), attr(el('span', 'c-frise__pt'), 'aria-hidden', 'true'), slot(it, 'jalon-titre', 'h3'), slot(it, 'jalon-texte', 'p', 'c-frise__txt')])))],
      barres: () => {
        const lis = items('barre', 'li', '', it => [slot(it, 'barre-libelle', 'p', 'c-barres__lib'),
          E('span', 'c-barres__piste', attr(el('span', 'c-barres__barre'), 'aria-hidden', 'true'), slot(it, 'barre-valeur', 'strong', 'c-barres__val'))]);
        parts(lis).forEach((f, k) => lis[k].style.setProperty('--v', `${(f * 100).toFixed(2)}%`));
        const accent = lis.some(li => li.hasAttribute('data-retenir'));
        return [tete(), corps('', E('ul', accent ? 'c-barres is-accent' : 'c-barres', lis), slot(src, 'source', 'p', 'c-source'))];
      },
      courbe: () => {
        const pts = items('point', 'li', '', it => [attr(el('span', 'c-courbe__pt'), 'aria-hidden', 'true'),
          slot(it, 'point-valeur', 'strong', 'c-courbe__val'), slot(it, 'point-libelle', 'p', 'c-courbe__lib')]);
        const f = parts(pts);
        pts.forEach((li, k) => li.style.setProperty('--f', f[k].toFixed(4)));
        const trace = f.map((v, k) => `${((k + 0.5) / f.length * 100).toFixed(2)},${(100 - v * 100).toFixed(2)}`).join(' ');
        const dessin = el('div', 'c-courbe');
        dessin.innerHTML = `<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="${trace}"/></svg>`;
        dessin.append(E('ol', '', pts));
        return [tete(), corps('', dessin, slot(src, 'source', 'p', 'c-source'))];
      },
      flux: () => {
        const sources = Array.from(src.querySelectorAll('[data-item="bloc"]'));
        const blocs = items('bloc', 'li', '', it => [icone(it, 'sq'), slot(it, 'bloc-titre', 'h3'), slot(it, 'bloc-texte', 'p')]);
        const suite = [];
        blocs.forEach((bloc, k) => {
          suite.push(bloc);
          if (k === blocs.length - 1) return;
          const lien = E('li', 'c-flux__lien', slot(sources[k], 'bloc-vers', 'span'));
          lien.insertAdjacentHTML('beforeend', '<svg class="ico" aria-hidden="true"><use href="#i-arrow-right"/></svg>');
          suite.push(lien);
        });
        return [tete(), corps('', E('ol', 'c-flux', suite))];
      },
      couloirs: () => {
        const role = (e, r) => attr(e, 'role', r);
        const etapes = slot(src, 'etape-nom', 'span').map(e => role(e, 'columnheader'));
        const rangs = items('couloir', 'div', 'c-couloirs__rang', it => [
          slot(it, 'couloir-nom', 'span', 'c-couloirs__nom').map(e => role(e, 'rowheader')),
          slot(it, 'case', 'span', 'c-couloirs__noeud').map(n => role(E('span', 'c-couloirs__case', n.textContent.trim() ? n : null), 'cell'))]);
        const grille = role(E('div', 'c-couloirs', role(E('div', 'c-couloirs__tete', role(el('span'), 'cell'), etapes), 'row'), rangs.map(r => role(r, 'row'))), 'table');
        grille.style.setProperty('--n', String(etapes.length || 1));
        return [tete(), corps('', grille)];
      },
      citation: () => [tete(), corps('', E('figure', 'c-citation', E('blockquote', '', slot(src, 'citation', 'p')),
        E('figcaption', '', slot(src, 'auteur', 'strong'), slot(src, 'contexte', 'span'))))],
      conclusion: () => {
        s.classList.add('split', 'end');
        return [
          E('div', 'split__main', marqueVide(),
            E('div', 'split__heading', slot(src, 'surtitre', 'p', 'kicker'), slot(src, 'titre', 'h2', 'split__title')),
            E('ul', 'beats', items('gain', 'li', '', it => [icone(it, 'sq'), E('div', '', slot(it, 'gain-titre', 'strong'), slot(it, 'gain-texte', 'p'))])),
            E('p', 'split__foot', attr(el('span'), 'data-pied'), attr(el('span', 's-foot__page'), 'data-page'))),
          E('div', 'split__aside', slot(src, 'demande-intitule', 'p', 'label'),
            E('ol', 'ask', items('demande', 'li', '', it => [slot(it, 'demande-quand', 'span', 'ask__when'), slot(it, 'demande-texte', 'strong')]))),
        ];
      },
    };
    s.classList.add('slide');
    const construire = B[s.dataset.composition];
    if (!construire) { s.append(...src.childNodes); return; }
    const notes = Array.from(src.querySelectorAll('[data-note]'));
    s.append(...[construire()].flat(Infinity).filter(Boolean));
    if (notes.length) s.append(E('aside', 'notes', E('ul', '', notes.map(n => E('li', '', ...n.childNodes)))));
    insecables(s);
  }
  /* Typographie française : pas de retour à la ligne avant : ; ! ? » % €, après «, ni au milieu d'un nombre. */
  function insecables(racine) {
    const marche = document.createTreeWalker(racine, NodeFilter.SHOW_TEXT);
    for (let n = marche.nextNode(); n; n = marche.nextNode()) {
      n.nodeValue = n.nodeValue
        .replace(/ ([:;!?»%€])/g, '\u00a0$1')
        .replace(/« /g, '«\u00a0')
        .replace(/(\d) (?=\d{3}(?!\d))/g, '$1\u00a0');
    }
  }
  slides.forEach(deplier);

  /* Cadre : bloc-marque, rubrique, fil de l'histoire, pied de page. La slide n'écrit que son contenu. */
  slides.forEach((s, i) => {
    const comp = s.dataset.composition || '';
    const titre = s.querySelector('[data-slot="titre"]');
    if (titre) { if (!titre.id) titre.id = `t${i + 1}`; s.setAttribute('aria-labelledby', titre.id); }
    if (!s.dataset.title) s.dataset.title = titre ? titre.textContent.replace(/\s+/g, ' ').trim() : comp;

    if (!HORS_CADRE.includes(comp)) {
      const top = el('header', 's-top');
      const bm = el('p'); poserMarque(bm);
      const sep = el('span', 's-top__sep'); sep.setAttribute('aria-hidden', 'true');
      top.append(bm, sep);
      if (s.dataset.rubrique) {
        const k = el('p', 'kicker', s.dataset.rubrique);
        if (s.dataset.ton === 'risque') k.classList.add('kicker--warn');
        if (s.dataset.ton === 'acquis') k.classList.add('kicker--done');
        top.append(k);
      }
      const actif = parseInt(s.dataset.temps, 10);
      if (temps.length > 1 && actif >= 1 && actif <= temps.length) {
        const fil = el('ol', 'fil'); fil.setAttribute('aria-label', 'Le fil de la présentation');
        temps.forEach((t, j) => {
          const li = el('li'); li.append(el('b', '', String(j + 1)), t);
          if (j + 1 === actif) { li.className = 'is-on'; li.setAttribute('aria-current', 'step'); }
          fil.append(li);
        });
        top.append(fil);
      }
      const tete = Array.from(s.children).filter(c => c.matches('.title,.s-lead'));
      s.prepend(top);
      if (tete.length) { const head = el('div', 's-head'); top.after(head); head.append(...tete); }
      const foot = el('footer', 's-foot');
      const gauche = el('span'); poserPied(gauche);
      const page = el('span', 's-foot__page'); page.setAttribute('data-page', '');
      foot.append(gauche, page);
      const notes = s.querySelector(':scope > .notes');
      if (notes) notes.before(foot); else s.append(foot);
    }
    s.querySelectorAll('[data-marque]').forEach(poserMarque);
    s.querySelectorAll('[data-pied]').forEach(poserPied);
    s.querySelectorAll('[data-page]').forEach(e => { e.textContent = `${i + 1} / ${total}`; });
  });

  /* Débordements : un contenu qui sort de sa zone, de son bloc ou de la slide. */
  function mesurer(s) {
    const out = new Set();
    const R = s.getBoundingClientRect();
    const tol = 2;
    s.querySelectorAll('.s-top,.s-body,.split__main,.split__aside,.cover__main,.cover__aside').forEach(z => {
      const dy = z.scrollHeight - z.clientHeight, dx = z.scrollWidth - z.clientWidth;
      if (dy > 1 || dx > 1) out.add(`${z.className.split(' ')[0]} (+${Math.max(dy, dx)} px)`);
    });
    s.querySelectorAll('[data-slot],[data-item]').forEach(e => {
      const r = e.getBoundingClientRect();
      if (!r.width && !r.height) return;
      const nom = e.dataset.slot || e.dataset.item;
      if (r.right > R.right + tol || r.bottom > R.bottom + tol || r.left < R.left - tol || r.top < R.top - tol) out.add(nom);
      const bloc = e.parentElement && e.parentElement.closest('[data-item]');
      if (bloc) {
        const b = bloc.getBoundingClientRect();
        if (r.right > b.right + tol || r.bottom > b.bottom + tol) out.add(nom);
      }
    });
    const cible = s.parentElement.classList.contains('vignette') ? [s, s.parentElement] : [s];
    cible.forEach(c => { if (out.size) c.dataset.debordement = Array.from(out).join(', '); else delete c.dataset.debordement; });
    return out.size;
  }
  function mesurerTout() {
    const n = slides.filter(s => mesurer(s) > 0).length;
    document.documentElement.dataset.debordements = String(n);
  }

  if (planche) {
    document.documentElement.classList.add('mode-planche');
    slides.forEach((s, i) => {
      const v = el('div', 'vignette');
      v.dataset.n = String(i + 1);
      v.dataset.c = s.dataset.composition || '';
      s.before(v); v.append(s);
    });
    const apres = () => mesurerTout();
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(apres);
    window.addEventListener('load', apres);
    return;
  }

  const hint = el('div', 'deck-hint', '← → pour naviguer · F plein écran · N notes · P imprimer');
  const progress = el('div', 'deck-progress');
  if (!shot) document.body.append(hint, progress);

  function fit() {
    const h = window.innerHeight * (document.body.classList.contains('with-notes') ? 0.7 : 1);
    stage.style.setProperty('--scale', Math.min(window.innerWidth / 1920, h / 1080));
  }
  function renderNotes() {
    const n = slides[cur].querySelector('.notes');
    panel.textContent = '';
    panel.append(el('h2', '', 'Notes · ' + (slides[cur].dataset.title || '')));
    if (n) panel.insertAdjacentHTML('beforeend', n.innerHTML); else panel.append(el('p', '', 'Pas de note pour cette slide.'));
  }
  function go(n) {
    if (!total) return;
    n = Math.max(0, Math.min(total - 1, n));
    if (n === cur) return;
    if (cur >= 0) slides[cur].classList.remove('is-active');
    slides[n].classList.add('is-active');
    cur = n;
    progress.style.width = `${total > 1 ? (cur / (total - 1)) * 100 : 100}%`;
    if (location.hash !== `#${cur + 1}`) history.replaceState(null, '', `#${cur + 1}`);
    const t = slides[cur].dataset.title || '';
    document.title = `${t} · ${deckTitle}`;
    annonce.textContent = `Diapositive ${cur + 1} sur ${total} : ${t}`;
    if (!panel.hidden) renderNotes();
    if (controle) mesurer(slides[cur]);
  }
  function fromHash() { const n = parseInt(location.hash.slice(1), 10); return Number.isFinite(n) ? n - 1 : 0; }
  function toggleNotes() {
    panel.hidden = !panel.hidden;
    document.body.classList.toggle('with-notes', !panel.hidden);
    if (!panel.hidden) renderNotes();
    fit();
  }

  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => go(fromHash()));
  document.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(k)) { e.preventDefault(); go(cur + 1); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') go(0);
    else if (k === 'End') go(total - 1);
    else if (k === 'f' || k === 'F') { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen?.(); }
    else if (k === 'n' || k === 'N') toggleNotes();
    else if (k === 'p' || k === 'P') window.print();
    else if (k === '?' || k === 'h' || k === 'H') { hint.classList.add('is-visible'); setTimeout(() => hint.classList.remove('is-visible'), 2600); }
  });
  document.querySelector('.deck').addEventListener('click', e => {
    if (e.clientX < window.innerWidth / 3) go(cur - 1); else go(cur + 1);
  });
  let x0 = null;
  document.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });

  fit();
  go(fromHash());
  if (controle && document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (cur >= 0) mesurer(slides[cur]); });
  if (!shot) { hint.classList.add('is-visible'); setTimeout(() => hint.classList.remove('is-visible'), 3200); }
})();
