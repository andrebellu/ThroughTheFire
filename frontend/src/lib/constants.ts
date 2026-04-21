export const strumenti = {
  'Muro':   { img: 'Stone.jpg',       desc: 'Blocca',       color: 'bg-zinc-700',    activeClass: 'ring-zinc-400/30' },
  'Fuoco':  { img: 'FirePixel.png',   desc: 'Pericolo',     color: 'bg-orange-900',  activeClass: 'border-orange-500 ring-orange-500/30' },
  'Robot':  { img: 'Robot.png',       desc: 'Start',        color: 'bg-blue-900',    activeClass: 'border-blue-500 ring-blue-500/30' },
  'Civile': { img: 'CivilPixel.png',  desc: 'Target',       color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
  'Extinguisher' : { img: 'ext.png',  desc: 'Fire Extinguisher',       color: 'bg-red-900', activeClass: 'border-red-500 ring-red-500/30' },
  'Arrivo': { icon: '🏁',             desc: 'Finish Point', color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
  'Vuoto':  { icon: '',               desc: 'Cella vuota',  color: 'bg-zinc-800/50', activeClass: '' }
};

export const coloriMinimap = {
  'Muro':   '#3f3f46',
  'Fuoco':  '#f97316',
  'Robot':  '#60a5fa',
  'Civile': '#34d399',
  'Arrivo': '#fbbf24',
  'Vuoto':  '#09090b'
};

export function schemaToMappa(schema: string) {
  const charMap: Record<string, string> = {
    '#': 'Muro', 'R': 'Robot', 'F': 'Fuoco',
    'C': 'Civile', 'A': 'Arrivo', '.': 'Vuoto'
  };
  return schema
    .trim()
    .split('\n')
    .map(riga => riga.trim())
    .filter(riga => riga.length > 0)
    .flatMap(riga => riga.split('').map(c => charMap[c] ?? 'Vuoto'));
}

