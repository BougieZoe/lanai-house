/*
 * All editorial copy lives here. Room views / floor geometry stay in main.js.
 * Languages: 中文, English, 日本語, 한국어, Français, Deutsch, Español, Italiano.
 */
export const LANGUAGES = [
  { code: 'zh', label: '中文', short: '中', htmlLang: 'zh-CN' },
  { code: 'en', label: 'English', short: 'EN', htmlLang: 'en' },
  { code: 'ja', label: '日本語', short: '日', htmlLang: 'ja' },
  { code: 'ko', label: '한국어', short: '한', htmlLang: 'ko' },
  { code: 'fr', label: 'Français', short: 'FR', htmlLang: 'fr' },
  { code: 'de', label: 'Deutsch', short: 'DE', htmlLang: 'de' },
  { code: 'es', label: 'Español', short: 'ES', htmlLang: 'es' },
  { code: 'it', label: 'Italiano', short: 'IT', htmlLang: 'it' },
];

const zh = {
  meta: {
    title: 'LANAI · Hainan | A tropical courtyard villa',
    description: '一栋会呼吸的海南热带住宅：深檐、檐廊、穿堂风与泳池。Blender + three.js 交互模型。',
  },
  nav: ['概念', '空间', '材料', '气候', '图纸'],
  ui: {
    autoRotate: '自动旋转',
    panelToggle: '收起 / 展开右侧信息栏',
    panelClose: '收起信息栏',
    panelReopen: '信息',
    dock: [['全景', 'OVERVIEW'], ['入口', 'ENTRY'], ['庭院', 'GARDEN'], ['泳池', 'POOL'], ['剖切', 'CUTAWAY']],
    tools: { roam: '漫游', roof: '屋顶', floor: '二层', labels: '标签', plan: '图纸' },
    time: { label: '光线', day: '日间', dusk: '黄昏', night: '夜晚' },
    hint: '拖拽旋转 · 滚轮缩放 · 右键平移',
    roomCardFocus: '带我去看看',
    loading: { title: 'LANAI · HAINAN', sub: '正在从 Blender 搬来一栋房子' },
    error: { title: '模型没有加载成功', text: '请确认 WebGL 可用，或刷新页面重试。' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100',
      title: '平面图',
      titleEn: '/ FLOOR PLANS',
      tabs: ['1F · 生活层', '2F · 卧室层'],
      note: '单位：米 · 北向朝上',
      legend: ['墙体', '湿区', '木作 / 檐廊', '水面'],
      localNote: '本地概念图纸，非施工图。',
    },
    roam: {
      badge: '自由漫游',
      sub: 'FREE ROAM',
      exit: '退出漫游',
      hint: 'WASD / 方向键移动 · 鼠标环顾 · Shift 加速 · E 上下楼 · L 语言 · Esc 退出',
      floor: '楼层',
      f1: '一层',
      f2: '二层',
      current: '当前空间',
      up: '按 E 上楼',
      down: '按 E 下楼',
      click: '点击画面锁定鼠标',
      touch: '左侧摇杆移动 · 右侧拖动环顾',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: '把一栋会呼吸的家，<br /><em>安在海南。</em>',
    lede: '一栋会呼吸的家：深檐、穿堂风、檐廊与一池水，把日常安放在海南的热带光线里。',
    meta: ['建筑 190 m²', '3 卧', '2.5 卫', '泳池'],
    concept: {
      num: '01', title: '概念', en: 'CONCEPT',
      p1: '不是复刻动画里的平面，而是提取它的“生活原型”：一栋紧凑的两层住宅，一条能看见院子的檐廊，一个从厨房递出冰饮的窗口，以及一条晾着白衬衫的阳台。',
      p2: '海南的气候把房子向外推。屋檐出挑 1.1 米，西侧用柚木格栅过滤午后阳光；餐厅与厨房朝北连接檐廊，客厅朝南接住晨光。风从南窗进入，穿过 LDK，从北侧檐廊离开。',
      quote: '“一栋房子真正被记住的，往往不是客厅，而是屋檐下那段没有安排的时间。”',
      cite: '设计手记 / 2026.11',
    },
    spaces: { num: '02', title: '空间', en: 'PROGRAM' },
    materials: {
      num: '03', title: '材料', en: 'PALETTE',
      note: '所有材料均为程序化材质：屋面瓦、灰泥、柚木与泳池马赛克由脚本生成贴图，并随 glTF 一同打包。',
      items: [
        ['海南红陶瓦', 'ROOF TILE'], ['石灰泥墙', 'LIME PLASTER'], ['柚木', 'TEAK'],
        ['火山石', 'BASALT'], ['鼠尾草绿', 'SAGE'], ['池水', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: '气候', en: 'CLIMATE',
      items: [
        ['深檐 1.1 m', '阻断正午直射，保护墙面与窗户。'],
        ['穿堂风', '南院进风，北侧高窗与檐廊出风。'],
        ['西晒格栅', '柚木百叶与攀援植物过滤午后热辐射。'],
        ['半室外', '檐廊、凉亭与泳池把生活带到阴影里。'],
        ['雨水链', '屋面雨水经链落入石钵，减少溅水。'],
      ],
    },
    build: {
      num: '05', title: '建造', en: 'CREDITS',
      p: 'Blender 5.2 程序化建模 / glTF 2.0 导出 / three.js r181 实时渲染。动画与交互由浏览器完成，模型不包含任何外部 3D 资产。',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: '客厅 / 餐厅 / 厨房', title: '客厅 · 餐厅 · 厨房', area: 'LDK · 65 m²',
      text: '朝南的客厅、中央餐桌与靠西的厨房连成一片。午后把北侧推拉门全部打开，风从檐廊穿进来，白衬衫在阳台上慢慢晾干。',
      meta: ['约 65 m²', '南北对流', '整面推拉门'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: '后檐廊', title: '后檐廊', area: 'ENGawa · 13 m²',
      text: '这是整栋房子的气候核心：深檐下的木平台、一杯茶、一条雨水链。它把客厅与庭院之间的边界变得模糊，也让雨天变得可以停留。',
      meta: ['约 13 m²', '深檐 1.1 m', '雨水链'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: '主卧 + 南向阳台', title: '主卧 + 南向阳台', area: 'MASTER · 22 m²',
      text: '主卧占据二层西南角，早晨的阳光先落在阳台的柚木栏杆上。晒衣杆保留自旧日住宅的日常：不藏起来，阳台就是生活的一部分。',
      meta: ['约 22 m²', '南向阳台', '独立衣柜'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: '儿童房', title: '儿童房', area: 'KIDS · 15 m²',
      text: '两张低床、一张靠窗的长桌和可以乱画的墙。北窗把柔和的漫射光带进来，下午不热，适合摊开一整套蜡笔。',
      meta: ['约 15 m²', '双床', '北向漫射光'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: '书房 / 客房', title: '书房 / 客房', area: 'STUDY · 13 m²',
      text: '二层的第三间房，面向南侧树梢。书架、日床和一张够大的桌子，平日工作，朋友来时就是客房。',
      meta: ['约 13 m²', '日床', '整墙书架'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: '泳池与庭院', title: '泳池与庭院', area: 'POOL · 5.6 × 3.6 m',
      text: '5.6 × 3.6 米的泳池贴着檐廊展开，池水蒸发带走热量。凉亭、躺椅和一棵鸡蛋花，把海南的下午安放在阴影与水面之间。',
      meta: ['5.6 × 3.6 m', '深 1.45 m', '户外淋浴'],
    },
  },
  labels: {
    ldk: '客厅 / 餐厨', engawa: '后檐廊', master: '主卧', kids: '儿童房', study: '书房',
    guest: '客房', pool: '泳池', pavilion: '凉亭', carport: '车棚', shiro: '狗屋',
  },
  plan: {
    labels: {
      living: '客厅', dining: '餐厅', kitchen: '厨房', tatami: '茶室', powder: '盥洗', laundry: '家政',
      entry: '玄关', stair: '楼梯', wc: '卫生间', guest: '客房', bath: '卫浴', gardenHall: '花园门厅',
      engawa: '后檐廊', porch: '门廊', master: '主卧', kids: '儿童房', study: '书房 / 客房',
      bath2: '浴室', hall: '过厅', storage: '储物', void: '挑空', balcony: '南阳台',
      rearDeck: '后檐台', lowRoof: '低层屋面',
    },
  },
  roam: {
    rooms: {
      front: '前院', garden: '后花园', east: '东侧花园', west: '西侧花园', engawa: '后檐廊', porch: '入口门廊',
      living: '客厅', dining: '餐厅', kitchen: '厨房', tea: '茶室', powder: '盥洗', laundry: '家政',
      entry: '玄关', stair: '楼梯', wc: '卫生间', guest: '客房', guestBath: '客房卫浴', gardenHall: '花园门厅',
      carport: '车棚', pavilion: '凉亭', poolDeck: '泳池平台', master: '主卧', kids: '儿童房',
      study: '书房', bath: '浴室', hall: '过厅', storage: '储物', balcony: '南阳台', rearDeck: '后檐台',
    },
  },
};

const en = {
  meta: {
    title: 'LANAI · Hainan | A tropical courtyard villa',
    description: 'A house that breathes: deep eaves, cross ventilation, an engawa and a pool in tropical Hainan. Interactive Blender + three.js model.',
  },
  nav: ['Concept', 'Spaces', 'Materials', 'Climate', 'Drawings'],
  ui: {
    autoRotate: 'Auto rotate',
    panelToggle: 'Show / hide information panel',
    panelClose: 'Close information',
    panelReopen: 'Info',
    dock: [['Overview', 'OVERVIEW'], ['Entry', 'ENTRY'], ['Garden', 'GARDEN'], ['Pool', 'POOL'], ['Cutaway', 'CUTAWAY']],
    tools: { roam: 'Walk', roof: 'Roof', floor: 'Upper', labels: 'Labels', plan: 'Plans' },
    time: { label: 'Light', day: 'Day', dusk: 'Dusk', night: 'Night' },
    hint: 'Drag to orbit · Scroll to zoom · Right-drag to pan',
    roomCardFocus: 'Take me there',
    loading: { title: 'LANAI · Hainan', sub: 'Moving a house over from Blender' },
    error: { title: 'The model could not load', text: 'Check that WebGL is available, then refresh the page.' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100',
      title: 'Floor plans',
      titleEn: '/ 平面图',
      tabs: ['1F · Living level', '2F · Sleeping level'],
      note: 'Metres · North is up',
      legend: ['Walls', 'Wet areas', 'Timber / deck', 'Water'],
      localNote: 'Concept drawing, not for construction.',
    },
    roam: {
      badge: 'Free roam',
      sub: 'WALKTHROUGH',
      exit: 'Exit walk',
      hint: 'WASD / arrow keys to move · mouse to look · Shift to run · E floor · L language · Esc exit',
      floor: 'Level',
      f1: 'Ground',
      f2: 'Upper',
      current: 'You are in',
      up: 'E — go upstairs',
      down: 'E — go downstairs',
      click: 'Click the view to capture the mouse',
      touch: 'Left stick to move · drag right to look',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: 'A house that breathes,<br /><em>rooted in Hainan.</em>',
    lede: 'A two-storey pitched roof, a small front yard, a laundry pole and a doghouse: the everydayness of a compact family house. We kept that feeling and rewrote it for Hainan with deep eaves, cross ventilation, an engawa and a pool.',
    meta: ['190 m² GFA', '3 bedrooms', '2.5 baths', 'Pool'],
    concept: {
      num: '01', title: 'Concept', en: 'CONCEPT',
      p1: "This is not a copy of the animation's floor plan. It extracts the everyday prototype: a compact two-storey house, an engawa that sees the garden, a kitchen window for passing out cold drinks, and a balcony where a white shirt dries slowly.",
      p2: 'Hainan pushes the house outward. The roof overhangs by 1.1 m; teak screens filter the western sun. Dining and kitchen open north to the engawa, while the living room holds the southern light. Air enters from the south and leaves through the north engawa.',
      quote: '“What we remember about a house is rarely the living room. It is the unscheduled time under the eaves.”',
      cite: 'Design note / 11.2026',
    },
    spaces: { num: '02', title: 'Spaces', en: 'PROGRAM' },
    materials: {
      num: '03', title: 'Materials', en: 'PALETTE',
      note: 'Every material is procedural: roof tiles, lime plaster, teak and pool mosaic are generated as textures and packed into the glTF.',
      items: [
        ['Hainan red clay tile', 'ROOF TILE'], ['Lime plaster', 'LIME PLASTER'], ['Teak', 'TEAK'],
        ['Basalt', 'BASALT'], ['Sage green', 'SAGE'], ['Pool water', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: 'Climate', en: 'CLIMATE',
      items: [
        ['Deep eaves 1.1 m', 'Blocks the midday sun and protects walls and windows.'],
        ['Cross ventilation', 'Air enters from the south yard and leaves through high north windows and the engawa.'],
        ['West sun screen', 'Teak louvers and climbing plants filter the afternoon heat.'],
        ['Semi-outdoor life', 'The engawa, pavilion and pool move daily life into the shade.'],
        ['Rain chain', 'Roof water runs down a chain into a stone basin, reducing splash.'],
      ],
    },
    build: {
      num: '05', title: 'Build', en: 'CREDITS',
      p: 'Procedural modelling in Blender 5.2 / glTF 2.0 / real-time rendering with three.js r181. All animation and interaction happens in the browser; the model contains no external 3D assets.',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: 'LIVING / DINING / KITCHEN', title: 'Living · Dining · Kitchen', area: 'LDK · 65 m²',
      text: 'A south-facing living room, a central dining table and a kitchen against the west wall form one continuous space. Open the north sliding doors in the afternoon and the breeze moves through the engawa while a white shirt dries on the balcony.',
      meta: ['approx. 65 m²', 'cross ventilation', 'full-width slider'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: 'REAR ENGAWA', title: 'Rear engawa', area: 'ENGawa · 13 m²',
      text: 'The climate core of the house: a timber deck under a deep eave, a cup of tea, a rain chain. It softens the edge between living room and garden and makes a rainy afternoon somewhere to stay.',
      meta: ['approx. 13 m²', '1.1 m eaves', 'rain chain'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: 'MASTER + SOUTH BALCONY', title: 'Master + south balcony', area: 'MASTER · 22 m²',
      text: 'The master bedroom occupies the south-west corner upstairs. Morning light lands first on the teak balcony rail. The laundry pole stays visible: the balcony is part of living, not a place to hide.',
      meta: ['approx. 22 m²', 'south balcony', 'walk-in wardrobe'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: 'KIDS ROOM', title: "Kids' room", area: 'KIDS · 15 m²',
      text: 'Two low beds, a long desk under the window and a wall that can take a lot of crayon. The north window brings in soft, even light — cool enough in the afternoon to spread out the whole box.',
      meta: ['approx. 15 m²', 'two beds', 'north daylight'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: 'STUDY / GUEST', title: 'Study / Guest', area: 'STUDY · 13 m²',
      text: 'The third room upstairs faces the treetops to the south. Bookshelves, a daybed and a desk big enough to work at: a study on weekdays, a guest room when friends stay.',
      meta: ['approx. 13 m²', 'daybed', 'full-wall library'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: 'POOL + GARDEN', title: 'Pool + garden', area: 'POOL · 5.6 × 3.6 m',
      text: 'A 5.6 × 3.6 m pool runs along the engawa; evaporation helps cool the garden. A pavilion, loungers and a frangipani tree place the Hainan afternoon between shadow and water.',
      meta: ['5.6 × 3.6 m', '1.45 m deep', 'outdoor shower'],
    },
  },
  labels: {
    ldk: 'Living / Kitchen', engawa: 'Rear Engawa', master: 'Master', kids: 'Kids', study: 'Study',
    guest: 'Guest', pool: 'Pool', pavilion: 'Pavilion', carport: 'Carport', shiro: 'Doghouse',
  },
  plan: {
    labels: {
      living: 'Living', dining: 'Dining', kitchen: 'Kitchen', tatami: 'Tea room', powder: 'Powder', laundry: 'Laundry',
      entry: 'Entry', stair: 'Stair', wc: 'WC', guest: 'Guest', bath: 'Bath', gardenHall: 'Garden hall',
      engawa: 'Engawa', porch: 'Porch', master: 'Master', kids: 'Kids', study: 'Study / Guest',
      bath2: 'Bath', hall: 'Hall', storage: 'Storage', void: 'Void', balcony: 'Balcony',
      rearDeck: 'Rear deck', lowRoof: 'Low roof',
    },
  },
  roam: {
    rooms: {
      front: 'Front garden', garden: 'Rear garden', east: 'East garden', west: 'West garden', engawa: 'Rear engawa', porch: 'Entry porch',
      living: 'Living', dining: 'Dining', kitchen: 'Kitchen', tea: 'Tea room', powder: 'Powder', laundry: 'Laundry',
      entry: 'Entry', stair: 'Stair', wc: 'WC', guest: 'Guest', guestBath: 'Guest bath', gardenHall: 'Garden hall',
      carport: 'Carport', pavilion: 'Pavilion', poolDeck: 'Pool deck', master: 'Master bedroom', kids: "Kids' room",
      study: 'Study', bath: 'Bath', hall: 'Hall', storage: 'Storage', balcony: 'Balcony', rearDeck: 'Rear deck',
    },
  },
};

const ja = {
  meta: {
    title: 'LANAI · Hainan | A tropical courtyard villa',
    description: '風が通り抜ける海南の熱帯住宅。深い軒、縁側、プール。Blender + three.js のインタラクティブモデル。',
  },
  nav: ['コンセプト', '空間', '素材', '気候', '図面'],
  ui: {
    autoRotate: '自動回転',
    panelToggle: '情報パネルを開閉',
    panelClose: '情報を閉じる',
    panelReopen: '情報',
    dock: [['全景', 'OVERVIEW'], ['入口', 'ENTRY'], ['庭', 'GARDEN'], ['プール', 'POOL'], ['断面', 'CUTAWAY']],
    tools: { roam: '散策', roof: '屋根', floor: '2階', labels: 'ラベル', plan: '図面' },
    time: { label: '光', day: '昼', dusk: '夕暮れ', night: '夜' },
    hint: 'ドラッグで回転 · スクロールでズーム · 右ドラッグで移動',
    roomCardFocus: 'ここへ行く',
    loading: { title: 'LANAI · HAINAN', sub: 'Blenderから家を運んでいます' },
    error: { title: 'モデルを読み込めませんでした', text: 'WebGLが利用できるか確認して、ページを再読み込みしてください。' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100', title: '平面図', titleEn: '/ FLOOR PLANS',
      tabs: ['1F · 生活階', '2F · 寝室階'], note: '単位：m · 北が上', legend: ['壁', '水回り', '木部 / 縁側', '水面'],
      localNote: 'コンセプト図面です。施工図ではありません。',
    },
    roam: {
      badge: '自由散策', sub: 'WALKTHROUGH', exit: '散策を終了',
      hint: 'WASD / 矢印キーで移動 · マウスで見回す · Shiftで加速 · Eで階移動 · L 言語 · Escで終了',
      floor: '階', f1: '1階', f2: '2階', current: '現在地', up: 'E — 2階へ', down: 'E — 1階へ',
      click: '画面をクリックしてマウスを固定', touch: '左スティックで移動 · 右ドラッグで見回す',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: '風が通る家を、<br /><em>海南に。</em>',
    lede: '切妻屋根の2階建て、小さな前庭、物干し竿、犬小屋。小さな家族の家の日常をそのままに、深い軒、通り抜ける風、縁側、そして水盤で海南の住まいへと書き換えました。',
    meta: ['延床 190 m²', '3寝室', '2.5浴室', 'プール'],
    concept: {
      num: '01', title: 'コンセプト', en: 'CONCEPT',
      p1: 'アニメの平面図をそのまま写すのではなく、その「生活の原型」を取り出します。コンパクトな2階建て、庭が見える縁側、冷たい飲み物を渡せる台所の窓、白いシャツが乾いていくバルコニー。',
      p2: '海南の気候は、家を外へ開きます。軒は1.1m。西日はチークのルーバーで濾し、ダイニングとキッチンは北の縁側へ。リビングは南の光を受け、風は南から入って北の縁側へ抜けます。',
      quote: '「家の記憶に残るのは、リビングとは限らない。軒下の、予定のない時間だったりする。」',
      cite: '設計ノート / 2026.11',
    },
    spaces: { num: '02', title: '空間', en: 'PROGRAM' },
    materials: {
      num: '03', title: '素材', en: 'PALETTE',
      note: '素材はすべてプロシージャル。屋根瓦、漆喰、チーク、プールのモザイクをスクリプトで生成し、glTFに同梱しています。',
      items: [
        ['海南の赤瓦', 'ROOF TILE'], ['漆喰壁', 'LIME PLASTER'], ['チーク', 'TEAK'],
        ['玄武岩', 'BASALT'], ['セージグリーン', 'SAGE'], ['プールの水', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: '気候', en: 'CLIMATE',
      items: [
        ['深い軒 1.1 m', '真昼の直射を遮り、壁と窓を守ります。'],
        ['通り抜ける風', '南の庭から入り、北の高窓と縁側へ抜けます。'],
        ['西日スクリーン', 'チークのルーバーとつる植物が午後の熱を和らげます。'],
        ['半屋外', '縁側、パビリオン、プールが生活を日陰へ運びます。'],
        ['雨鎖', '屋根の雨水を鎖で石鉢へ。跳ね返りを抑えます。'],
      ],
    },
    build: {
      num: '05', title: '制作', en: 'CREDITS',
      p: 'Blender 5.2によるプロシージャルモデリング / glTF 2.0 / three.js r181によるリアルタイム描画。アニメーションと操作はブラウザで完結し、外部の3D素材は使用していません。',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: 'リビング / ダイニング / キッチン', title: 'リビング・ダイニング・キッチン', area: 'LDK · 65 m²',
      text: '南向きのリビング、中央のダイニングテーブル、西壁に沿ったキッチンがひとつながりになっています。午後に北側の引き戸を全開にすると、縁側から風が入り、バルコニーの白いシャツがゆっくり乾いていきます。',
      meta: ['約 65 m²', '南北の通風', '全面引き戸'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: '裏の縁側', title: '裏の縁側', area: 'ENGawa · 13 m²',
      text: 'この家の気候の核。深い軒の下の木の床、一杯のお茶、雨鎖。リビングと庭の境界を曖昧にし、雨の午後にも居場所をつくります。',
      meta: ['約 13 m²', '軒 1.1 m', '雨鎖'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: '主寝室 + 南バルコニー', title: '主寝室 + 南バルコニー', area: 'MASTER · 22 m²',
      text: '2階の南西角を占める主寝室。朝の光はまずバルコニーのチーク手すりに落ちます。物干し竿は隠さず、バルコニーを生活の一部として残しました。',
      meta: ['約 22 m²', '南バルコニー', '独立クローゼット'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: '子供部屋', title: '子供部屋', area: 'KIDS · 15 m²',
      text: '低いベッドが2台、窓際の長い机、落書きできる壁。北窓からは柔らかな拡散光が入り、午後も暑くなりすぎず、クレヨンを全部広げるのにちょうどいい。',
      meta: ['約 15 m²', '2ベッド', '北向きの拡散光'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: '書斎 / ゲスト', title: '書斎 / ゲストルーム', area: 'STUDY · 13 m²',
      text: '2階の三つ目の部屋は、南の木々に面しています。本棚、デイベッド、十分な大きさの机。平日は書斎、友人が泊まるときはゲストルームになります。',
      meta: ['約 13 m²', 'デイベッド', '壁一面の本棚'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: 'プールと庭', title: 'プールと庭', area: 'POOL · 5.6 × 3.6 m',
      text: '5.6 × 3.6 mのプールが縁側に沿って広がり、水面の蒸発が庭を冷やします。パビリオン、ラウンジャー、プルメリアの木が、海南の午後を日陰と水の間に置きます。',
      meta: ['5.6 × 3.6 m', '水深 1.45 m', '屋外シャワー'],
    },
  },
  labels: {
    ldk: 'リビング / キッチン', engawa: '裏縁側', master: '主寝室', kids: '子供部屋', study: '書斎',
    guest: 'ゲスト', pool: 'プール', pavilion: 'パビリオン', carport: 'カーポート', shiro: '犬小屋',
  },
  plan: {
    labels: {
      living: 'リビング', dining: 'ダイニング', kitchen: 'キッチン', tatami: '茶室', powder: '洗面', laundry: '家事室',
      entry: '玄関', stair: '階段', wc: 'トイレ', guest: 'ゲスト', bath: '浴室', gardenHall: '庭の間',
      engawa: '裏縁側', porch: 'ポーチ', master: '主寝室', kids: '子供部屋', study: '書斎 / ゲスト',
      bath2: '浴室', hall: 'ホール', storage: '収納', void: '吹抜', balcony: 'バルコニー',
      rearDeck: '裏デッキ', lowRoof: '下屋根',
    },
  },
  roam: {
    rooms: {
      front: '前庭', garden: '裏庭', east: '東の庭', west: '西の庭', engawa: '裏縁側', porch: '玄関ポーチ',
      living: 'リビング', dining: 'ダイニング', kitchen: 'キッチン', tea: '茶室', powder: '洗面', laundry: '家事室',
      entry: '玄関', stair: '階段', wc: 'トイレ', guest: 'ゲストルーム', guestBath: 'ゲスト浴室', gardenHall: '庭の間',
      carport: 'カーポート', pavilion: 'パビリオン', poolDeck: 'プールデッキ', master: '主寝室', kids: '子供部屋',
      study: '書斎', bath: '浴室', hall: 'ホール', storage: '収納', balcony: 'バルコニー', rearDeck: '裏デッキ',
    },
  },
};

const ko = {
  meta: {
    title: 'LANAI · Hainan | A tropical courtyard villa',
    description: '바람이 통하는 하이난의 열대 주택. 깊은 처마, 엔가와, 수영장. Blender + three.js 인터랙티브 모델.',
  },
  nav: ['콘셉트', '공간', '재료', '기후', '도면'],
  ui: {
    autoRotate: '자동 회전',
    panelToggle: '정보 패널 열기 / 닫기',
    panelClose: '정보 닫기',
    panelReopen: '정보',
    dock: [['전체', 'OVERVIEW'], ['입구', 'ENTRY'], ['정원', 'GARDEN'], ['수영장', 'POOL'], ['단면', 'CUTAWAY']],
    tools: { roam: '산책', roof: '지붕', floor: '2층', labels: '라벨', plan: '도면' },
    time: { label: '빛', day: '낮', dusk: '황혼', night: '밤' },
    hint: '드래그로 회전 · 스크롤로 확대 · 오른쪽 드래그로 이동',
    roomCardFocus: '여기로 가기',
    loading: { title: 'LANAI · HAINAN', sub: 'Blender에서 집을 옮기는 중' },
    error: { title: '모델을 불러오지 못했습니다', text: 'WebGL 사용 가능 여부를 확인한 뒤 페이지를 새로고침하세요.' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100', title: '평면도', titleEn: '/ FLOOR PLANS',
      tabs: ['1F · 생활층', '2F · 침실층'], note: '단위: m · 북쪽이 위', legend: ['벽', '습식 공간', '목재 / 덱', '수면'],
      localNote: '콘셉트 도면이며 시공도가 아닙니다.',
    },
    roam: {
      badge: '자유 산책', sub: 'WALKTHROUGH', exit: '산책 종료',
      hint: 'WASD / 방향키 이동 · 마우스 시점 · Shift 달리기 · E 층 이동 · L 언어 · Esc 종료',
      floor: '층', f1: '1층', f2: '2층', current: '현재 공간', up: 'E — 위층으로', down: 'E — 아래층으로',
      click: '화면을 클릭해 마우스 고정', touch: '왼쪽 스틱 이동 · 오른쪽 드래그 시점',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: '바람이 통하는 집을,<br /><em>하이난에.</em>',
    lede: '박공지붕 2층집, 작은 앞마당, 빨랫대, 개집. 작은 가족집의 일상을 그대로 두고 깊은 처마와 통풍, 엔가와, 물을 더해 하이난의 주거로 다시 썼습니다.',
    meta: ['연면적 190 m²', '침실 3', '욕실 2.5', '수영장'],
    concept: {
      num: '01', title: '콘셉트', en: 'CONCEPT',
      p1: '애니메이션의 평면도를 그대로 베끼는 대신 “생활의 원형”을 꺼냅니다. 작고 단단한 2층집, 정원이 보이는 엔가와, 시원한 음료를 건넬 수 있는 주방 창, 흰 셔츠가 천천히 마르는 발코니.',
      p2: '하이난의 기후는 집을 바깥으로 밀어냅니다. 처마는 1.1m, 서쪽 햇빛은 티크 루버가 거릅니다. 다이닝과 주방은 북쪽 엔가와로 열리고, 거실은 남쪽 빛을 받습니다. 바람은 남쪽에서 들어와 북쪽 엔가와로 빠져나갑니다.',
      quote: '“집을 기억하게 하는 것은 거실이 아니라, 처마 아래의 예정 없는 시간인 경우가 많다.”',
      cite: '디자인 노트 / 2026.11',
    },
    spaces: { num: '02', title: '공간', en: 'PROGRAM' },
    materials: {
      num: '03', title: '재료', en: 'PALETTE',
      note: '모든 재료는 절차적으로 생성됩니다. 기와, 석회미장, 티크, 수영장 모자이크를 스크립트로 만들고 glTF에 함께 담았습니다.',
      items: [
        ['하이난 붉은 점토 기와', 'ROOF TILE'], ['석회미장 벽', 'LIME PLASTER'], ['티크', 'TEAK'],
        ['현무암', 'BASALT'], ['세이지 그린', 'SAGE'], ['수영장 물', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: '기후', en: 'CLIMATE',
      items: [
        ['깊은 처마 1.1 m', '한낮의 직사광을 막고 벽과 창을 보호합니다.'],
        ['관통 통풍', '남쪽 마당에서 들어온 바람이 북쪽 높은 창과 엔가와로 나갑니다.'],
        ['서향 차양', '티크 루버와 덩굴 식물이 오후의 열을 거릅니다.'],
        ['반야외 생활', '엔가와, 정자, 수영장이 일상을 그늘로 옮깁니다.'],
        ['빗물 사슬', '지붕의 빗물이 사슬을 타고 돌그릇으로 내려와 튀는 물을 줄입니다.'],
      ],
    },
    build: {
      num: '05', title: '제작', en: 'CREDITS',
      p: 'Blender 5.2 절차적 모델링 / glTF 2.0 / three.js r181 실시간 렌더링. 모든 애니메이션과 상호작용은 브라우저에서 이루어지며 외부 3D 자산은 사용하지 않았습니다.',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: '거실 / 다이닝 / 주방', title: '거실 · 다이닝 · 주방', area: 'LDK · 65 m²',
      text: '남향 거실, 중앙 식탁, 서쪽 벽을 따라 놓인 주방이 하나로 이어집니다. 오후에 북쪽 미닫이문을 모두 열면 엔가와로 바람이 들어오고, 발코니의 흰 셔츠가 천천히 마릅니다.',
      meta: ['약 65 m²', '남북 통풍', '전면 미닫이'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: '뒷 엔가와', title: '뒷 엔가와', area: 'ENGawa · 13 m²',
      text: '이 집의 기후 핵심. 깊은 처마 아래의 나무 덱, 한 잔의 차, 빗물 사슬. 거실과 정원의 경계를 흐리게 만들고 비 오는 오후에도 머물 곳을 만듭니다.',
      meta: ['약 13 m²', '처마 1.1 m', '빗물 사슬'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: '안방 + 남쪽 발코니', title: '안방 + 남쪽 발코니', area: 'MASTER · 22 m²',
      text: '2층 남서쪽 모서리의 안방. 아침 햇빛이 먼저 발코니의 티크 난간에 내려앉습니다. 빨랫대는 숨기지 않았습니다. 발코니도 생활의 일부니까요.',
      meta: ['약 22 m²', '남쪽 발코니', '독립 옷장'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: '어린이방', title: '어린이방', area: 'KIDS · 15 m²',
      text: '낮은 침대 두 개, 창가의 긴 책상, 마음껏 낙서할 수 있는 벽. 북쪽 창은 부드러운 확산광을 들여오고 오후에도 덥지 않아 크레용을 전부 펼치기 좋습니다.',
      meta: ['약 15 m²', '침대 2개', '북향 확산광'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: '서재 / 게스트', title: '서재 / 게스트룸', area: 'STUDY · 13 m²',
      text: '2층의 세 번째 방은 남쪽 나무 꼭대기를 바라봅니다. 책장, 데이베드, 충분히 큰 책상. 평일에는 서재, 친구가 묵으면 게스트룸이 됩니다.',
      meta: ['약 13 m²', '데이베드', '벽면 책장'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: '수영장과 정원', title: '수영장과 정원', area: 'POOL · 5.6 × 3.6 m',
      text: '5.6 × 3.6m 수영장이 엔가와를 따라 펼쳐지고, 물이 증발하며 정원을 식힙니다. 정자, 라운저, 플루메리아 한 그루가 하이난의 오후를 그늘과 물 사이에 놓습니다.',
      meta: ['5.6 × 3.6 m', '수심 1.45 m', '야외 샤워'],
    },
  },
  labels: {
    ldk: '거실 / 주방', engawa: '뒷 엔가와', master: '안방', kids: '어린이방', study: '서재',
    guest: '게스트', pool: '수영장', pavilion: '정자', carport: '카포트', shiro: '개집',
  },
  plan: {
    labels: {
      living: '거실', dining: '다이닝', kitchen: '주방', tatami: '다실', powder: '세면', laundry: '세탁',
      entry: '현관', stair: '계단', wc: '화장실', guest: '게스트', bath: '욕실', gardenHall: '가든 홀',
      engawa: '뒷 엔가와', porch: '포치', master: '안방', kids: '어린이방', study: '서재 / 게스트',
      bath2: '욕실', hall: '홀', storage: '수납', void: '오픈 보이드', balcony: '발코니',
      rearDeck: '뒷 데크', lowRoof: '낮은 지붕',
    },
  },
  roam: {
    rooms: {
      front: '앞마당', garden: '뒷정원', east: '동쪽 정원', west: '서쪽 정원', engawa: '뒷 엔가와', porch: '입구 포치',
      living: '거실', dining: '다이닝', kitchen: '주방', tea: '다실', powder: '세면실', laundry: '세탁실',
      entry: '현관', stair: '계단', wc: '화장실', guest: '게스트룸', guestBath: '게스트 욕실', gardenHall: '가든 홀',
      carport: '카포트', pavilion: '정자', poolDeck: '수영장 데크', master: '안방', kids: '어린이방',
      study: '서재', bath: '욕실', hall: '홀', storage: '수납', balcony: '발코니', rearDeck: '뒷 데크',
    },
  },
};

const fr = {
  meta: {
    title: 'LANAI · Hainan | Une villa tropicale',
    description: 'Une maison qui respire à Hainan : grands débords, engawa, ventilation traversante et piscine. Modèle interactif Blender + three.js.',
  },
  nav: ['Concept', 'Espaces', 'Matières', 'Climat', 'Plans'],
  ui: {
    autoRotate: 'Rotation auto', panelToggle: 'Afficher / masquer le panneau', panelClose: 'Fermer les informations', panelReopen: 'Infos',
    dock: [['Vue', 'OVERVIEW'], ['Entrée', 'ENTRY'], ['Jardin', 'GARDEN'], ['Piscine', 'POOL'], ['Coupe', 'CUTAWAY']],
    tools: { roam: 'Visite', roof: 'Toit', floor: 'Étage', labels: 'Labels', plan: 'Plans' },
    time: { label: 'Lumière', day: 'Jour', dusk: 'Crépuscule', night: 'Nuit' },
    hint: 'Glisser pour tourner · molette pour zoomer · clic droit pour déplacer',
    roomCardFocus: 'M’y emmener',
    loading: { title: 'LANAI · Hainan', sub: 'La maison arrive depuis Blender' },
    error: { title: 'Le modèle n’a pas pu être chargé', text: 'Vérifiez que WebGL est disponible, puis rechargez la page.' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100', title: 'Plans', titleEn: '/ FLOOR PLANS',
      tabs: ['1F · Niveau de vie', '2F · Niveau nuit'], note: 'Mètres · Nord en haut', legend: ['Murs', 'Zones humides', 'Bois / terrasse', 'Eau'],
      localNote: 'Plan conceptuel, non destiné à la construction.',
    },
    roam: {
      badge: 'Visite libre', sub: 'WALKTHROUGH', exit: 'Quitter la visite',
      hint: 'WASD / flèches pour marcher · souris pour regarder · Maj pour courir · E étage · L langue · Échap quitter',
      floor: 'Niveau', f1: 'Rez-de-chaussée', f2: 'Étage', current: 'Vous êtes ici', up: 'E — monter', down: 'E — descendre',
      click: 'Cliquez pour capturer la souris', touch: 'Joystick gauche pour marcher · glisser à droite pour regarder',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: 'Une maison qui respire,<br /><em>posée à Hainan.</em>',
    lede: 'Un toit à deux pans, une petite cour, un fil à linge et une niche : le quotidien d’une maison familiale compacte. Nous avons gardé cette sensation et l’avons réécrite pour Hainan avec de grands débords, une ventilation traversante, un engawa et une piscine.',
    meta: ['190 m²', '3 chambres', '2,5 salles de bain', 'Piscine'],
    concept: {
      num: '01', title: 'Concept', en: 'CONCEPT',
      p1: "Il ne s’agit pas de copier le plan du dessin animé, mais d’en extraire le prototype du quotidien : une maison compacte à deux niveaux, un engawa qui regarde le jardin, une fenêtre de cuisine pour passer des boissons fraîches et un balcon où sèche une chemise blanche.",
      p2: 'Le climat de Hainan pousse la maison vers l’extérieur. Le toit déborde de 1,1 m, des claustras en teck filtrent le soleil d’ouest. La salle à manger et la cuisine s’ouvrent au nord sur l’engawa, tandis que le séjour capte la lumière du sud.',
      quote: '« Ce que l’on retient d’une maison, c’est rarement le salon. C’est le temps non programmé sous les avant-toits. »',
      cite: 'Carnet de conception / 11.2026',
    },
    spaces: { num: '02', title: 'Espaces', en: 'PROGRAMME' },
    materials: {
      num: '03', title: 'Matières', en: 'PALETTE',
      note: 'Toutes les matières sont procédurales : tuiles, enduit à la chaux, teck et mosaïque de piscine sont générés puis intégrés au glTF.',
      items: [
        ['Tuile d’argile rouge de Hainan', 'ROOF TILE'], ['Enduit à la chaux', 'LIME PLASTER'], ['Teck', 'TEAK'],
        ['Basalte', 'BASALT'], ['Vert sauge', 'SAGE'], ['Eau de la piscine', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: 'Climat', en: 'CLIMAT',
      items: [
        ['Débords de 1,1 m', 'Bloquent le soleil de midi et protègent les murs et les fenêtres.'],
        ['Ventilation traversante', 'L’air entre par la cour sud et sort par les fenêtres hautes et l’engawa.'],
        ['Filtre solaire à l’ouest', 'Claustras en teck et plantes grimpantes filtrent la chaleur de l’après-midi.'],
        ['Vie semi-extérieure', 'L’engawa, le pavillon et la piscine déplacent le quotidien à l’ombre.'],
        ['Chaîne de pluie', 'L’eau du toit descend une chaîne jusqu’à une vasque de pierre.'],
      ],
    },
    build: {
      num: '05', title: 'Fabrication', en: 'CRÉDITS',
      p: 'Modélisation procédurale sous Blender 5.2 / glTF 2.0 / rendu temps réel avec three.js r181. Animations et interactions dans le navigateur ; aucun asset 3D externe.',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: 'SÉJOUR / SALLE À MANGER / CUISINE', title: 'Séjour · Salle à manger · Cuisine', area: 'LDK · 65 m²',
      text: 'Un séjour au sud, une table centrale et une cuisine le long du mur ouest forment un seul espace. L’après-midi, ouvrez les baies coulissantes au nord : la brise traverse l’engawa pendant qu’une chemise blanche sèche sur le balcon.',
      meta: ['env. 65 m²', 'ventilation traversante', 'baie toute largeur'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: 'ENGAWA ARRIÈRE', title: 'Engawa arrière', area: 'ENGawa · 13 m²',
      text: 'Le cœur climatique de la maison : une terrasse en bois sous un grand auvent, une tasse de thé, une chaîne de pluie. Elle brouille la limite entre séjour et jardin et rend l’après-midi pluvieux habitable.',
      meta: ['env. 13 m²', 'auvent 1,1 m', 'chaîne de pluie'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: 'CHAMBRE PRINCIPALE + BALCON SUD', title: 'Chambre principale + balcon sud', area: 'MASTER · 22 m²',
      text: 'La chambre occupe l’angle sud-ouest de l’étage. Le matin, la lumière touche d’abord la rambarde en teck du balcon. Le fil à linge reste visible : le balcon fait partie de la vie, il n’est pas à cacher.',
      meta: ['env. 22 m²', 'balcon sud', 'dressing'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: 'CHAMBRE DES ENFANTS', title: 'Chambre des enfants', area: 'KIDS · 15 m²',
      text: 'Deux lits bas, un long bureau sous la fenêtre et un mur qui peut accueillir beaucoup de crayons. La fenêtre nord apporte une lumière douce et égale, assez fraîche l’après-midi pour étaler toute la boîte.',
      meta: ['env. 15 m²', 'deux lits', 'lumière nord'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: 'BUREAU / AMIS', title: 'Bureau / Chambre d’amis', area: 'STUDY · 13 m²',
      text: 'La troisième pièce de l’étage regarde la cime des arbres au sud. Bibliothèques, lit de jour et bureau assez grand pour travailler : bureau en semaine, chambre d’amis le week-end.',
      meta: ['env. 13 m²', 'lit de jour', 'bibliothèque murale'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: 'PISCINE + JARDIN', title: 'Piscine + jardin', area: 'POOL · 5,6 × 3,6 m',
      text: 'Une piscine de 5,6 × 3,6 m longe l’engawa ; l’évaporation rafraîchit le jardin. Un pavillon, des chaises longues et un frangipanier installent l’après-midi de Hainan entre l’ombre et l’eau.',
      meta: ['5,6 × 3,6 m', '1,45 m de fond', 'douche extérieure'],
    },
  },
  labels: {
    ldk: 'Séjour / Cuisine', engawa: 'Engawa arrière', master: 'Chambre principale', kids: 'Enfants', study: 'Bureau',
    guest: 'Amis', pool: 'Piscine', pavilion: 'Pavillon', carport: 'Carport', shiro: 'Niche',
  },
  plan: {
    labels: {
      living: 'Séjour', dining: 'Salle à manger', kitchen: 'Cuisine', tatami: 'Salon de thé', powder: 'Toilettes', laundry: 'Buanderie',
      entry: 'Entrée', stair: 'Escalier', wc: 'WC', guest: 'Amis', bath: 'Bain', gardenHall: 'Hall jardin',
      engawa: 'Engawa', porch: 'Porche', master: 'Chambre principale', kids: 'Enfants', study: 'Bureau / Amis',
      bath2: 'Bain', hall: 'Hall', storage: 'Rangement', void: 'Vide', balcony: 'Balcon',
      rearDeck: 'Terrasse arrière', lowRoof: 'Toit bas',
    },
  },
  roam: {
    rooms: {
      front: 'Jardin avant', garden: 'Jardin arrière', east: 'Jardin est', west: 'Jardin ouest', engawa: 'Engawa arrière', porch: 'Porche',
      living: 'Séjour', dining: 'Salle à manger', kitchen: 'Cuisine', tea: 'Salon de thé', powder: 'Toilettes', laundry: 'Buanderie',
      entry: 'Entrée', stair: 'Escalier', wc: 'WC', guest: 'Chambre d’amis', guestBath: 'Bain des amis', gardenHall: 'Hall jardin',
      carport: 'Carport', pavilion: 'Pavillon', poolDeck: 'Plage de piscine', master: 'Chambre principale', kids: 'Chambre des enfants',
      study: 'Bureau', bath: 'Salle de bain', hall: 'Hall', storage: 'Rangement', balcony: 'Balcon', rearDeck: 'Terrasse arrière',
    },
  },
};

const de = {
  meta: {
    title: 'LANAI · Hainan | Eine tropische Villa',
    description: 'Ein Haus, das atmet: tiefe Dächer, Engawa, Querlüftung und Pool in Hainan. Interaktives Blender- und three.js-Modell.',
  },
  nav: ['Konzept', 'Räume', 'Materialien', 'Klima', 'Pläne'],
  ui: {
    autoRotate: 'Auto-Rotation', panelToggle: 'Infofenster ein-/ausblenden', panelClose: 'Infos schließen', panelReopen: 'Info',
    dock: [['Gesamt', 'OVERVIEW'], ['Eingang', 'ENTRY'], ['Garten', 'GARDEN'], ['Pool', 'POOL'], ['Schnitt', 'CUTAWAY']],
    tools: { roam: 'Rundgang', roof: 'Dach', floor: 'Obergeschoss', labels: 'Labels', plan: 'Pläne' },
    time: { label: 'Licht', day: 'Tag', dusk: 'Dämmerung', night: 'Nacht' },
    hint: 'Ziehen zum Drehen · Scrollen zum Zoomen · Rechtsziehen zum Verschieben',
    roomCardFocus: 'Dorthin gehen',
    loading: { title: 'LANAI · Hainan', sub: 'Ein Haus wird aus Blender herübergeholt' },
    error: { title: 'Das Modell konnte nicht geladen werden', text: 'Prüfe, ob WebGL verfügbar ist, und lade die Seite neu.' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100', title: 'Grundrisse', titleEn: '/ FLOOR PLANS',
      tabs: ['1F · Wohnen', '2F · Schlafen'], note: 'Meter · Norden oben', legend: ['Wände', 'Nassbereiche', 'Holz / Deck', 'Wasser'],
      localNote: 'Konzeptplan, kein Ausführungsplan.',
    },
    roam: {
      badge: 'Freier Rundgang', sub: 'WALKTHROUGH', exit: 'Rundgang beenden',
      hint: 'WASD / Pfeiltasten bewegen · Maus umsehen · Shift rennen · E Etage · L Sprache · Esc beenden',
      floor: 'Etage', f1: 'Erdgeschoss', f2: 'Obergeschoss', current: 'Du bist hier', up: 'E — nach oben', down: 'E — nach unten',
      click: 'Klicken, um die Maus zu fangen', touch: 'Linker Stick bewegen · rechts ziehen zum Umsehen',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: 'Ein Haus, das atmet,<br /><em>verwurzelt in Hainan.</em>',
    lede: 'Ein zweigeschossiges Satteldach, ein kleiner Vorgarten, eine Wäscheleine und eine Hundehütte: der Alltag eines kompakten Familienhauses. Wir haben dieses Gefühl bewahrt und für Hainan neu geschrieben – mit tiefen Dächern, Querlüftung, Engawa und Pool.',
    meta: ['190 m²', '3 Schlafzimmer', '2,5 Bäder', 'Pool'],
    concept: {
      num: '01', title: 'Konzept', en: 'CONCEPT',
      p1: 'Es geht nicht um eine Kopie des Zeichentrick-Grundrisses, sondern um den Alltagsprototyp: ein kompaktes zweigeschossiges Haus, ein Engawa mit Blick in den Garten, ein Küchenfenster für kalte Getränke und ein Balkon, auf dem ein weißes Hemd trocknet.',
      p2: 'Das Klima Hainans schiebt das Haus nach außen. Das Dach kragt 1,1 m aus, Teak-Lamellen filtern die Westsonne. Essen und Küche öffnen sich nach Norden zum Engawa, während das Wohnzimmer das Südlicht einfängt.',
      quote: '„Was von einem Haus bleibt, ist selten das Wohnzimmer. Es ist die unverplante Zeit unter dem Dach.“',
      cite: 'Entwurfsnotiz / 11.2026',
    },
    spaces: { num: '02', title: 'Räume', en: 'PROGRAMM' },
    materials: {
      num: '03', title: 'Materialien', en: 'PALETTE',
      note: 'Alle Materialien sind prozedural: Dachziegel, Kalkputz, Teak und Poolmosaik werden als Texturen erzeugt und in die glTF gepackt.',
      items: [
        ['Roter Hainan-Tonziegel', 'ROOF TILE'], ['Kalkputz', 'LIME PLASTER'], ['Teak', 'TEAK'],
        ['Basalt', 'BASALT'], ['Salbeigrün', 'SAGE'], ['Poolwasser', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: 'Klima', en: 'KLIMA',
      items: [
        ['Tiefe Dächer 1,1 m', 'Blockieren die Mittagssonne und schützen Wände und Fenster.'],
        ['Querlüftung', 'Luft kommt aus dem Südgarten und verlässt das Haus über hohe Nordfenster und Engawa.'],
        ['Westschutz', 'Teak-Lamellen und Kletterpflanzen filtern die Nachmittagshitze.'],
        ['Halbdraußen', 'Engawa, Pavillon und Pool verlegen den Alltag in den Schatten.'],
        ['Regenkette', 'Dachwasser läuft über eine Kette in einen Steinbrunnen.'],
      ],
    },
    build: {
      num: '05', title: 'Umsetzung', en: 'CREDITS',
      p: 'Prozedurale Modellierung in Blender 5.2 / glTF 2.0 / Echtzeit-Rendering mit three.js r181. Animation und Interaktion laufen im Browser; keine externen 3D-Assets.',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: 'WOHNEN / ESSEN / KÜCHE', title: 'Wohnen · Essen · Küche', area: 'LDK · 65 m²',
      text: 'Ein nach Süden orientiertes Wohnzimmer, ein zentraler Esstisch und eine Küche an der Westwand bilden einen Raum. Öffnet man nachmittags die nördlichen Schiebetüren, zieht die Brise durch das Engawa, während ein weißes Hemd auf dem Balkon trocknet.',
      meta: ['ca. 65 m²', 'Querlüftung', 'raumbreite Schiebetür'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: 'HINTERES ENGAWA', title: 'Hinteres Engawa', area: 'ENGawa · 13 m²',
      text: 'Das klimatische Herz des Hauses: eine Holzterrasse unter tiefem Dach, eine Tasse Tee, eine Regenkette. Es löst die Grenze zwischen Wohnzimmer und Garten auf und macht den regnerischen Nachmittag bewohnbar.',
      meta: ['ca. 13 m²', '1,1 m Dach', 'Regenkette'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: 'ELTERNSCHLAFZIMMER + SÜDBALKON', title: 'Elternschlafzimmer + Südbalkon', area: 'MASTER · 22 m²',
      text: 'Das Schlafzimmer liegt in der südwestlichen Ecke des Obergeschosses. Morgens trifft das Licht zuerst auf das Teakgeländer des Balkons. Die Wäscheleine bleibt sichtbar: Der Balkon gehört zum Leben, er wird nicht versteckt.',
      meta: ['ca. 22 m²', 'Südbalkon', 'begehbarer Schrank'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: 'KINDERZIMMER', title: 'Kinderzimmer', area: 'KIDS · 15 m²',
      text: 'Zwei niedrige Betten, ein langer Schreibtisch am Fenster und eine Wand, die viel Kreide verträgt. Das Nordfenster bringt weiches, gleichmäßiges Licht – kühl genug, um nachmittags die ganze Kiste Buntstifte auszubreiten.',
      meta: ['ca. 15 m²', 'zwei Betten', 'Nordlicht'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: 'ARBEIT / GÄSTE', title: 'Arbeiten / Gäste', area: 'STUDY · 13 m²',
      text: 'Das dritte Zimmer im Obergeschoss blickt in die Baumkronen im Süden. Regale, ein Tagesbett und ein ausreichend großer Schreibtisch: Arbeitszimmer in der Woche, Gästezimmer am Wochenende.',
      meta: ['ca. 13 m²', 'Tagesbett', 'wandfüllendes Regal'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: 'POOL + GARTEN', title: 'Pool + Garten', area: 'POOL · 5,6 × 3,6 m',
      text: 'Ein Pool von 5,6 × 3,6 m läuft am Engawa entlang; die Verdunstung kühlt den Garten. Ein Pavillon, Liegen und ein Frangipani-Baum setzen den Hainan-Nachmittag zwischen Schatten und Wasser.',
      meta: ['5,6 × 3,6 m', '1,45 m tief', 'Außendusche'],
    },
  },
  labels: {
    ldk: 'Wohnen / Küche', engawa: 'Engawa', master: 'Eltern', kids: 'Kinder', study: 'Arbeit',
    guest: 'Gäste', pool: 'Pool', pavilion: 'Pavillon', carport: 'Carport', shiro: 'Hundehütte',
  },
  plan: {
    labels: {
      living: 'Wohnen', dining: 'Essen', kitchen: 'Küche', tatami: 'Teezimmer', powder: 'WC', laundry: 'Wäsche',
      entry: 'Eingang', stair: 'Treppe', wc: 'WC', guest: 'Gäste', bath: 'Bad', gardenHall: 'Gartenhalle',
      engawa: 'Engawa', porch: 'Porch', master: 'Eltern', kids: 'Kinder', study: 'Arbeit / Gäste',
      bath2: 'Bad', hall: 'Halle', storage: 'Abstellraum', void: 'Luftraum', balcony: 'Balkon',
      rearDeck: 'Norddeck', lowRoof: 'Niedriges Dach',
    },
  },
  roam: {
    rooms: {
      front: 'Vorgarten', garden: 'Hintergarten', east: 'Ostgarten', west: 'Westgarten', engawa: 'Engawa', porch: 'Eingangsbereich',
      living: 'Wohnen', dining: 'Essen', kitchen: 'Küche', tea: 'Teezimmer', powder: 'WC', laundry: 'Wäsche',
      entry: 'Eingang', stair: 'Treppe', wc: 'WC', guest: 'Gästezimmer', guestBath: 'Gästebad', gardenHall: 'Gartenhalle',
      carport: 'Carport', pavilion: 'Pavillon', poolDeck: 'Pooldeck', master: 'Elternschlafzimmer', kids: 'Kinderzimmer',
      study: 'Arbeitszimmer', bath: 'Bad', hall: 'Halle', storage: 'Abstellraum', balcony: 'Balkon', rearDeck: 'Norddeck',
    },
  },
};

const es = {
  meta: {
    title: 'LANAI · Hainan | Una villa tropical',
    description: 'Una casa que respira en Hainan: aleros profundos, engawa, ventilación cruzada y piscina. Modelo interactivo Blender + three.js.',
  },
  nav: ['Concepto', 'Espacios', 'Materiales', 'Clima', 'Planos'],
  ui: {
    autoRotate: 'Rotación automática', panelToggle: 'Mostrar / ocultar información', panelClose: 'Cerrar información', panelReopen: 'Info',
    dock: [['General', 'OVERVIEW'], ['Entrada', 'ENTRY'], ['Jardín', 'GARDEN'], ['Piscina', 'POOL'], ['Sección', 'CUTAWAY']],
    tools: { roam: 'Paseo', roof: 'Cubierta', floor: 'Planta alta', labels: 'Etiquetas', plan: 'Planos' },
    time: { label: 'Luz', day: 'Día', dusk: 'Atardecer', night: 'Noche' },
    hint: 'Arrastra para girar · rueda para zoom · botón derecho para desplazar',
    roomCardFocus: 'Llévame allí',
    loading: { title: 'LANAI · Hainan', sub: 'Trayendo una casa desde Blender' },
    error: { title: 'No se pudo cargar el modelo', text: 'Comprueba que WebGL esté disponible y recarga la página.' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100', title: 'Planos', titleEn: '/ FLOOR PLANS',
      tabs: ['1F · Planta de día', '2F · Planta de noche'], note: 'Metros · Norte arriba', legend: ['Muros', 'Zonas húmedas', 'Madera / deck', 'Agua'],
      localNote: 'Plano conceptual, no de obra.',
    },
    roam: {
      badge: 'Paseo libre', sub: 'WALKTHROUGH', exit: 'Salir del paseo',
      hint: 'WASD / flechas para moverte · ratón para mirar · Mayús correr · E planta · L idioma · Esc salir',
      floor: 'Planta', f1: 'Baja', f2: 'Alta', current: 'Estás en', up: 'E — subir', down: 'E — bajar',
      click: 'Haz clic para capturar el ratón', touch: 'Stick izquierdo para moverte · arrastra a la derecha para mirar',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: 'Una casa que respira,<br /><em>arraigada en Hainan.</em>',
    lede: 'Una cubierta a dos aguas, un pequeño jardín delantero, un tendedero y una caseta de perro: la cotidianidad de una casa familiar compacta. Conservamos esa sensación y la reescribimos para Hainan con aleros profundos, ventilación cruzada, engawa y piscina.',
    meta: ['190 m²', '3 dormitorios', '2,5 baños', 'Piscina'],
    concept: {
      num: '01', title: 'Concepto', en: 'CONCEPT',
      p1: 'No se trata de copiar el plano del dibujo animado, sino de extraer el prototipo de lo cotidiano: una casa compacta de dos plantas, un engawa que mira al jardín, una ventana de cocina para pasar bebidas frías y un balcón donde se seca una camisa blanca.',
      p2: 'El clima de Hainan empuja la casa hacia fuera. El alero vuela 1,1 m; las celosías de teca filtran el sol del oeste. El comedor y la cocina se abren al norte hacia el engawa, mientras el salón recibe la luz del sur.',
      quote: '«Lo que recordamos de una casa rara vez es el salón. Es el tiempo sin agenda bajo el alero.»',
      cite: 'Cuaderno de proyecto / 11.2026',
    },
    spaces: { num: '02', title: 'Espacios', en: 'PROGRAMA' },
    materials: {
      num: '03', title: 'Materiales', en: 'PALETA',
      note: 'Todos los materiales son procedurales: teja, cal, teca y mosaico de piscina se generan como texturas y se incluyen en el glTF.',
      items: [
        ['Teja de arcilla roja de Hainan', 'ROOF TILE'], ['Muro de cal', 'LIME PLASTER'], ['Teca', 'TEAK'],
        ['Basalto', 'BASALT'], ['Verde salvia', 'SAGE'], ['Agua de piscina', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: 'Clima', en: 'CLIMA',
      items: [
        ['Aleros de 1,1 m', 'Bloquean el sol de mediodía y protegen muros y ventanas.'],
        ['Ventilación cruzada', 'El aire entra por el jardín sur y sale por las ventanas altas y el engawa.'],
        ['Filtro solar oeste', 'Las celosías de teca y las trepadoras filtran el calor de la tarde.'],
        ['Vida semiexterior', 'El engawa, el pabellón y la piscina llevan la vida a la sombra.'],
        ['Cadena de lluvia', 'El agua del tejado baja por una cadena hasta una vasija de piedra.'],
      ],
    },
    build: {
      num: '05', title: 'Construcción', en: 'CRÉDITOS',
      p: 'Modelado procedural en Blender 5.2 / glTF 2.0 / render en tiempo real con three.js r181. Animación e interacción en el navegador; sin recursos 3D externos.',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: 'SALÓN / COMEDOR / COCINA', title: 'Salón · Comedor · Cocina', area: 'LDK · 65 m²',
      text: 'Un salón orientado al sur, una mesa central y una cocina junto al muro oeste forman un solo espacio. Al abrir las correderas del norte por la tarde, la brisa atraviesa el engawa mientras una camisa blanca se seca en el balcón.',
      meta: ['aprox. 65 m²', 'ventilación cruzada', 'corredera completa'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: 'ENGAWA TRASERA', title: 'Engawa trasera', area: 'ENGawa · 13 m²',
      text: 'El corazón climático de la casa: una plataforma de madera bajo un alero profundo, una taza de té, una cadena de lluvia. Difumina el límite entre salón y jardín y hace habitable una tarde de lluvia.',
      meta: ['aprox. 13 m²', 'alero 1,1 m', 'cadena de lluvia'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: 'DORMITORIO PRINCIPAL + BALCÓN SUR', title: 'Dormitorio principal + balcón sur', area: 'MASTER · 22 m²',
      text: 'El dormitorio ocupa la esquina suroeste de la planta alta. La luz de la mañana llega primero a la barandilla de teca del balcón. El tendedero sigue visible: el balcón es parte de la vida, no un lugar para esconder.',
      meta: ['aprox. 22 m²', 'balcón sur', 'vestidor'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: 'DORMITORIO INFANTIL', title: 'Dormitorio infantil', area: 'KIDS · 15 m²',
      text: 'Dos camas bajas, un escritorio largo bajo la ventana y una pared que admite muchos lápices. La ventana norte trae luz suave y uniforme, lo bastante fresca por la tarde para extender toda la caja de ceras.',
      meta: ['aprox. 15 m²', 'dos camas', 'luz norte'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: 'ESTUDIO / INVITADOS', title: 'Estudio / Invitados', area: 'STUDY · 13 m²',
      text: 'La tercera habitación de la planta alta mira a las copas de los árboles del sur. Estanterías, una cama de día y un escritorio amplio: estudio entre semana, habitación de invitados cuando vienen amigos.',
      meta: ['aprox. 13 m²', 'cama de día', 'biblioteca mural'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: 'PISCINA + JARDÍN', title: 'Piscina + jardín', area: 'POOL · 5,6 × 3,6 m',
      text: 'Una piscina de 5,6 × 3,6 m recorre el engawa; la evaporación refresca el jardín. Un pabellón, tumbonas y un frangipani colocan la tarde de Hainan entre la sombra y el agua.',
      meta: ['5,6 × 3,6 m', '1,45 m de fondo', 'ducha exterior'],
    },
  },
  labels: {
    ldk: 'Salón / Cocina', engawa: 'Engawa', master: 'Principal', kids: 'Infantil', study: 'Estudio',
    guest: 'Invitados', pool: 'Piscina', pavilion: 'Pabellón', carport: 'Cochera', shiro: 'Caseta',
  },
  plan: {
    labels: {
      living: 'Salón', dining: 'Comedor', kitchen: 'Cocina', tatami: 'Sala de té', powder: 'Aseo', laundry: 'Lavandería',
      entry: 'Entrada', stair: 'Escalera', wc: 'Aseo', guest: 'Invitados', bath: 'Baño', gardenHall: 'Vestíbulo jardín',
      engawa: 'Engawa', porch: 'Porche', master: 'Principal', kids: 'Infantil', study: 'Estudio / Invitados',
      bath2: 'Baño', hall: 'Distribuidor', storage: 'Almacén', void: 'Vacío', balcony: 'Balcón',
      rearDeck: 'Deck trasero', lowRoof: 'Cubierta baja',
    },
  },
  roam: {
    rooms: {
      front: 'Jardín delantero', garden: 'Jardín trasero', east: 'Jardín este', west: 'Jardín oeste', engawa: 'Engawa', porch: 'Porche',
      living: 'Salón', dining: 'Comedor', kitchen: 'Cocina', tea: 'Sala de té', powder: 'Aseo', laundry: 'Lavandería',
      entry: 'Entrada', stair: 'Escalera', wc: 'Aseo', guest: 'Habitación de invitados', guestBath: 'Baño de invitados', gardenHall: 'Vestíbulo jardín',
      carport: 'Cochera', pavilion: 'Pabellón', poolDeck: 'Deck de piscina', master: 'Dormitorio principal', kids: 'Dormitorio infantil',
      study: 'Estudio', bath: 'Baño', hall: 'Distribuidor', storage: 'Almacén', balcony: 'Balcón', rearDeck: 'Deck trasero',
    },
  },
};

const it = {
  meta: {
    title: 'LANAI · Hainan | Una villa tropicale',
    description: 'Una casa che respira a Hainan: ampi sporti, engawa, ventilazione trasversale e piscina. Modello interattivo Blender + three.js.',
  },
  nav: ['Concetto', 'Spazi', 'Materiali', 'Clima', 'Tavole'],
  ui: {
    autoRotate: 'Rotazione automatica', panelToggle: 'Mostra / nascondi informazioni', panelClose: 'Chiudi informazioni', panelReopen: 'Info',
    dock: [['Panoramica', 'OVERVIEW'], ['Ingresso', 'ENTRY'], ['Giardino', 'GARDEN'], ['Piscina', 'POOL'], ['Sezione', 'CUTAWAY']],
    tools: { roam: 'Visita', roof: 'Tetto', floor: 'Piano', labels: 'Etichette', plan: 'Tavole' },
    time: { label: 'Luce', day: 'Giorno', dusk: 'Tramonto', night: 'Notte' },
    hint: 'Trascina per ruotare · rotella per zoom · tasto destro per spostare',
    roomCardFocus: 'Portami lì',
    loading: { title: 'LANAI · Hainan', sub: 'Stiamo portando una casa da Blender' },
    error: { title: 'Impossibile caricare il modello', text: 'Verifica che WebGL sia disponibile e ricarica la pagina.' },
    plan: {
      eyebrow: 'DRAWINGS · 1:100', title: 'Piante', titleEn: '/ FLOOR PLANS',
      tabs: ['1F · Piano giorno', '2F · Piano notte'], note: 'Metri · Nord in alto', legend: ['Pareti', 'Zona umida', 'Legno / deck', 'Acqua'],
      localNote: 'Tavola concettuale, non esecutiva.',
    },
    roam: {
      badge: 'Visita libera', sub: 'WALKTHROUGH', exit: 'Esci dalla visita',
      hint: 'WASD / frecce per muoverti · mouse per guardare · Shift correre · E piano · L lingua · Esc uscire',
      floor: 'Piano', f1: 'Terra', f2: 'Primo', current: 'Sei in', up: 'E — sali', down: 'E — scendi',
      click: 'Clicca per catturare il mouse', touch: 'Stick sinistro per muoverti · trascina a destra per guardare',
    },
  },
  panel: {
    eyebrow: 'HAINAN · TROPICAL RESIDENCE · 2026',
    titleHtml: 'Una casa che respira,<br /><em>radicata a Hainan.</em>',
    lede: 'Un tetto a due falde, un piccolo giardino, uno stendibiancheria e una cuccia: la quotidianità di una casa familiare compatta. Abbiamo conservato quella sensazione e l’abbiamo riscritta per Hainan con sporti profondi, ventilazione trasversale, engawa e piscina.',
    meta: ['190 m²', '3 camere', '2,5 bagni', 'Piscina'],
    concept: {
      num: '01', title: 'Concetto', en: 'CONCEPT',
      p1: "Non è una copia della pianta del cartone: è l'estrazione del prototipo quotidiano. Una casa compatta su due piani, un engawa che guarda il giardino, una finestra di cucina per passare bibite fredde e un balcone dove asciuga una camicia bianca.",
      p2: 'Il clima di Hainan spinge la casa verso l’esterno. Il tetto sporge di 1,1 m, le lamelle in teak filtrano il sole a ovest. Pranzo e cucina si aprono a nord verso l’engawa, mentre il soggiorno raccoglie la luce del sud.',
      quote: '«Di una casa ricordiamo raramente il soggiorno. Ricordiamo il tempo non programmato sotto il tetto.»',
      cite: 'Note di progetto / 11.2026',
    },
    spaces: { num: '02', title: 'Spazi', en: 'PROGRAMMA' },
    materials: {
      num: '03', title: 'Materiali', en: 'PALETTE',
      note: 'Tutti i materiali sono procedurali: coppi, intonaco di calce, teak e mosaico della piscina sono generati come texture e inclusi nel glTF.',
      items: [
        ['Coppo in argilla rossa di Hainan', 'ROOF TILE'], ['Intonaco di calce', 'LIME PLASTER'], ['Teak', 'TEAK'],
        ['Basalto', 'BASALT'], ['Verde salvia', 'SAGE'], ['Acqua della piscina', 'POOL'],
      ],
    },
    climate: {
      num: '04', title: 'Clima', en: 'CLIMA',
      items: [
        ['Sporti di 1,1 m', 'Bloccano il sole di mezzogiorno e proteggono pareti e finestre.'],
        ['Ventilazione trasversale', 'L’aria entra dal giardino sud ed esce dalle finestre alte e dall’engawa.'],
        ['Filtro solare ovest', 'Lamelle in teak e piante rampicanti filtrano il calore pomeridiano.'],
        ['Vita semi-esterna', 'Engawa, padiglione e piscina portano la vita all’ombra.'],
        ['Catena di pioggia', 'L’acqua del tetto scende lungo una catena fino a una vasca di pietra.'],
      ],
    },
    build: {
      num: '05', title: 'Realizzazione', en: 'CREDITI',
      p: 'Modellazione procedurale in Blender 5.2 / glTF 2.0 / rendering realtime con three.js r181. Animazioni e interazioni nel browser; nessun asset 3D esterno.',
      disclaimer: 'A fan-made architectural study, made with affection for the Nohara house in Crayon Shin-chan. Not affiliated with the original animation.',
    },
  },
  rooms: {
    living: {
      kicker: 'SPACE 01 / LDK', name: 'SOGGIORNO / PRANZO / CUCINA', title: 'Soggiorno · Pranzo · Cucina', area: 'LDK · 65 m²',
      text: 'Un soggiorno a sud, un tavolo centrale e una cucina lungo la parete ovest formano un unico spazio. Aprendo le porte scorrevoli a nord nel pomeriggio, la brezza attraversa l’engawa mentre una camicia bianca asciuga sul balcone.',
      meta: ['circa 65 m²', 'ventilazione trasversale', 'scorrevole a tutta larghezza'],
    },
    engawa: {
      kicker: 'SPACE 02 / ENGAWA', name: 'ENGAWA POSTERIORE', title: 'Engawa posteriore', area: 'ENGawa · 13 m²',
      text: 'Il cuore climatico della casa: una piattaforma in legno sotto uno sporto profondo, una tazza di tè, una catena di pioggia. Sfuma il confine tra soggiorno e giardino e rende abitabile un pomeriggio di pioggia.',
      meta: ['circa 13 m²', 'sporto 1,1 m', 'catena di pioggia'],
    },
    master: {
      kicker: 'SPACE 03 / MASTER', name: 'CAMERA PADRONALE + BALCONE SUD', title: 'Camera padronale + balcone sud', area: 'MASTER · 22 m²',
      text: 'La camera occupa l’angolo sud-ovest del piano superiore. La mattina la luce arriva prima sulla ringhiera in teak del balcone. Lo stendibiancheria resta visibile: il balcone è parte della vita, non un luogo da nascondere.',
      meta: ['circa 22 m²', 'balcone sud', 'cabina armadio'],
    },
    kids: {
      kicker: 'SPACE 04 / KIDS', name: 'CAMERETTA', title: 'Cameretta', area: 'KIDS · 15 m²',
      text: 'Due letti bassi, una scrivania lunga sotto la finestra e una parete che sopporta molti pastelli. La finestra nord porta luce morbida e uniforme, abbastanza fresca nel pomeriggio per stendere tutta la scatola.',
      meta: ['circa 15 m²', 'due letti', 'luce nord'],
    },
    study: {
      kicker: 'SPACE 05 / STUDY', name: 'STUDIO / OSPITI', title: 'Studio / Ospiti', area: 'STUDY · 13 m²',
      text: 'La terza stanza del piano superiore guarda le chiome degli alberi a sud. Libreria, daybed e una scrivania abbastanza grande: studio in settimana, camera per gli ospiti nel fine settimana.',
      meta: ['circa 13 m²', 'daybed', 'libreria a parete'],
    },
    pool: {
      kicker: 'SPACE 06 / POOL', name: 'PISCINA + GIARDINO', title: 'Piscina + giardino', area: 'POOL · 5,6 × 3,6 m',
      text: 'Una piscina di 5,6 × 3,6 m corre lungo l’engawa; l’evaporazione rinfresca il giardino. Un padiglione, lettini e un frangipani mettono il pomeriggio di Hainan tra ombra e acqua.',
      meta: ['5,6 × 3,6 m', 'profondità 1,45 m', 'doccia esterna'],
    },
  },
  labels: {
    ldk: 'Soggiorno / Cucina', engawa: 'Engawa', master: 'Padronale', kids: 'Cameretta', study: 'Studio',
    guest: 'Ospiti', pool: 'Piscina', pavilion: 'Padiglione', carport: 'Posto auto', shiro: 'Cuccia',
  },
  plan: {
    labels: {
      living: 'Soggiorno', dining: 'Pranzo', kitchen: 'Cucina', tatami: 'Stanza del tè', powder: 'Bagno', laundry: 'Lavanderia',
      entry: 'Ingresso', stair: 'Scala', wc: 'WC', guest: 'Ospiti', bath: 'Bagno', gardenHall: 'Atrio giardino',
      engawa: 'Engawa', porch: 'Portico', master: 'Padronale', kids: 'Cameretta', study: 'Studio / Ospiti',
      bath2: 'Bagno', hall: 'Disimpegno', storage: 'Ripostiglio', void: 'Vuoto', balcony: 'Balcone',
      rearDeck: 'Deck posteriore', lowRoof: 'Tetto basso',
    },
  },
  roam: {
    rooms: {
      front: 'Giardino anteriore', garden: 'Giardino posteriore', east: 'Giardino est', west: 'Giardino ovest', engawa: 'Engawa', porch: 'Portico',
      living: 'Soggiorno', dining: 'Pranzo', kitchen: 'Cucina', tea: 'Stanza del tè', powder: 'Bagno', laundry: 'Lavanderia',
      entry: 'Ingresso', stair: 'Scala', wc: 'WC', guest: 'Camera ospiti', guestBath: 'Bagno ospiti', gardenHall: 'Atrio giardino',
      carport: 'Posto auto', pavilion: 'Padiglione', poolDeck: 'Deck piscina', master: 'Camera padronale', kids: 'Cameretta',
      study: 'Studio', bath: 'Bagno', hall: 'Disimpegno', storage: 'Ripostiglio', balcony: 'Balcone', rearDeck: 'Deck posteriore',
    },
  },
};

export const I18N = { zh, en, ja, ko, fr, de, es, it };
export const getLang = (code) => I18N[code] || I18N.zh;
