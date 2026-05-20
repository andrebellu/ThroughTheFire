export const strumenti = {
  'Muro':   { img: 'Stone.jpg',       desc: 'Blocca',       color: 'bg-zinc-700',    activeClass: 'ring-zinc-400/30' },
  'Fuoco':  { img: 'FirePixel.png',   desc: 'Pericolo',     color: 'bg-orange-900',  activeClass: 'border-orange-500 ring-orange-500/30' },
  'Robot':  { img: 'Robot.png',       desc: 'Start',        color: 'bg-blue-900',    activeClass: 'border-blue-500 ring-blue-500/30' },
  'Civile': { img: 'CivilPixel.png',  desc: 'Target',       color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
  'Extinguisher' : { img: 'ext.png',  desc: 'Fire Extinguisher',       color: 'bg-red-900', activeClass: 'border-red-500 ring-red-500/30' },
  'Arrivo': { icon: '🏁',             desc: 'Finish Point', color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
  'Vuoto':  { icon: '',               desc: 'Cella vuota',  color: 'bg-zinc-800/50', activeClass: '' },
  'Macerie': { img: 'Rubble.png', desc: 'Ostacolo distruttibile', color: 'bg-stone-600', activeClass: 'border-stone-400 ring-stone-400/30' },
  'Piccone': { img: 'Pickaxe.png', desc: 'Rompe macerie', color: 'bg-amber-700', activeClass: 'border-amber-500 ring-amber-500/30' },
};

export const coloriMinimap = {
  'Muro':   '#3f3f46',
  'Fuoco':  '#f97316',
  'Robot':  '#60a5fa',
  'Civile': '#34d399',
  'Extinguisher': '#ef4444',
  'Arrivo': '#fbbf24',
  'Vuoto':  '#09090b',
  'Macerie': '#57534e',
  'Piccone': '#b45309',
};

export const defaultLevels = [
  {
    id: 1,
    nome: 'Through the Smoke',
    difficolta: 'Easy',
    coloreDiff: '#34d399',
    larghezza: 10,
    altezza: 8,
    schema:
        `##########
        #R.......#
        ####.###.#
        #..P...#.#
        #.####.F.#
        #C.....E.#
        #......F.#
        ########MA`
  },
  {
    id: 2,
    nome: 'Through the Fire',
    difficolta: 'Medium',
    coloreDiff: '#facc15',
    larghezza: 14,
    altezza: 10,
    schema:
        `##############
        #R.......E..P#
        ###.####.###M#
        #C..#F.....MC#
        #F###.####.###
        #.#........#.#
        #.#.######F#.#
        #..........E.#
        #F.#######.F.#
        ###########.A#`
  },
  {
    id: 3,
    nome: 'Through Hell',
    difficolta: 'Hard',
    coloreDiff: '#f87171',
    larghezza: 16,
    altezza: 12,
    schema:
        `################
        #R...F.....C...#
        #.####.###.###.#
        #.#C...F.#M#E..#
        #.######.#.#.###
        #P.....E.#...#.#
        ######M#####.#.#
        #F...#.......#.#
        #.##.#####.###.#
        #.#C.F.......F.#
        #...E.####.C...#
        ##############A#`
  },
  {
    id: 4,
    nome: 'Ultra Hell',
    difficolta: 'Ultra',
    coloreDiff: '#b91c1c',
    larghezza: 18,
    altezza: 14,
    schema:
        `##################
        #R.F......P..#...#
        #.##.#######.#M#.#
        #.#C.......F.#.#.#
        #.#.##########.#.#
        #.F.MC...#...F...#
        #####.##.#.###E#.#
        #...#..#F#...#.#.#
        #.####.#.###.#MF.#
        #.#E...#...C.#.#.#
        #...F..###.###...#
        #.####C#...F.#.###
        #......#E..#.....#
        ################A#`
  },
  {
    id: 5,
    nome: 'Ultra Ultra Hell',
    difficolta: 'Nightmare',
    coloreDiff: '#7f1d1d',
    larghezza: 20,
    altezza: 15,
    schema:
        `####################
        #R..#....MCM...#P..#
        #F..#.####M###M#F#.#
        #...#.#E.......#.#.#
        ###.#.#.######.#.#.#
        #C..F...#C...F...#.#
        #.#######M####M###M#
        #.......#.#E.......#
        #######.#.#.######.#
        #...F...#...#C...F.#
        #.#######M###.####.#
        #.#E......#......#.#
        #...F...###.C..F...#
        #..##...E.#...##...#
        ##################A#`
  }
]

