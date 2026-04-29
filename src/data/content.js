import {
  BadgeCheck,
  Bolt,
  Building2,
  Cable,
  CircleGauge,
  ClipboardCheck,
  Factory,
  FileCheck2,
  Gauge,
  HardHat,
  Hospital,
  Hotel,
  Landmark,
  Lightbulb,
  MapPinned,
  Network,
  PanelsTopLeft,
  ShieldCheck,
  Store,
  TimerReset,
  Warehouse,
  Wrench,
  Zap,
} from 'lucide-react'

export const navItems = [
  { label: 'Inicio', href: '#inicio' },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Sectores', href: '#sectores' },
  { label: 'Proceso', href: '#proceso' },
  { label: 'Proyectos', href: '#proyectos' },
  { label: 'Nosotros', href: '#nosotros' },
  { label: 'Contacto', href: '#contacto' },
]

export const metrics = [
  'Media y baja tensión',
  'Atención industrial y comercial',
  'Cumplimiento normativo',
  'Respuesta en obra',
]

export const trustCards = [
  {
    title: 'Seguridad eléctrica',
    description: 'Instalaciones ejecutadas con protecciones, identificación y criterios de operación segura.',
    icon: ShieldCheck,
  },
  {
    title: 'Planeación y control de obra',
    description: 'Alcances claros, coordinación en campo y seguimiento para reducir retrabajos y atrasos.',
    icon: ClipboardCheck,
  },
  {
    title: 'Cumplimiento técnico y normativo',
    description: 'Revisión de capacidades, cargas, canalizaciones y entrega técnica ordenada.',
    icon: FileCheck2,
  },
]

export const services = [
  {
    title: 'Instalaciones eléctricas en baja tensión',
    description: 'Distribución, fuerza, alumbrado y contactos para operación comercial, industrial y de servicios.',
    icon: Bolt,
  },
  {
    title: 'Media tensión',
    description: 'Infraestructura de alimentación y distribución para proyectos con demanda eléctrica especializada.',
    icon: Zap,
  },
  {
    title: 'Subestaciones eléctricas',
    description: 'Instalación, adecuación y puesta en marcha de subestaciones para continuidad operativa.',
    icon: Factory,
  },
  {
    title: 'Transformadores',
    description: 'Montaje, conexión, revisión y mantenimiento de transformadores según requerimiento de carga.',
    icon: CircleGauge,
  },
  {
    title: 'Tableros generales y derivados',
    description: 'Armado, ordenamiento, conexión e identificación de tableros para distribución confiable.',
    icon: PanelsTopLeft,
  },
  {
    title: 'Canalizaciones eléctricas',
    description: 'Charola, tubería, registros y rutas eléctricas limpias, accesibles y coordinadas con obra.',
    icon: Cable,
  },
  {
    title: 'Alumbrado industrial y comercial',
    description: 'Sistemas de iluminación funcional para áreas productivas, comerciales, exteriores y servicios.',
    icon: Lightbulb,
  },
  {
    title: 'Sistemas de puesta a tierra',
    description: 'Soluciones de protección, continuidad y seguridad para equipos, tableros e infraestructura.',
    icon: Network,
  },
  {
    title: 'Mantenimiento eléctrico preventivo y correctivo',
    description: 'Inspecciones, correcciones y atención a fallas para conservar disponibilidad y seguridad.',
    icon: Wrench,
  },
  {
    title: 'Diagnóstico, levantamientos y adecuaciones',
    description: 'Revisión en sitio, detección de riesgos y definición de alcances antes de intervenir.',
    icon: Gauge,
  },
  {
    title: 'Alimentadores eléctricos',
    description: 'Cableado, canalización y conexión de alimentadores principales y derivados de potencia.',
    icon: Cable,
  },
  {
    title: 'Obra eléctrica para construcción',
    description: 'Ejecución eléctrica para naves industriales, comercios, edificios y desarrollos en obra.',
    icon: HardHat,
  },
]

export const sectors = [
  { title: 'Naves industriales', icon: Factory },
  { title: 'Comercios', icon: Store },
  { title: 'Edificios corporativos', icon: Building2 },
  { title: 'Hoteles', icon: Hotel },
  { title: 'Hospitales y clínicas', icon: Hospital },
  { title: 'Desarrollos habitacionales', icon: MapPinned },
  { title: 'Obra pública', icon: Landmark },
  { title: 'Parques industriales', icon: Network },
  { title: 'Bodegas y centros logísticos', icon: Warehouse },
]

export const differentiators = [
  'Atención técnica desde el levantamiento',
  'Presupuestos claros y defendibles',
  'Ejecución ordenada en obra',
  'Seguridad para personal e instalaciones',
  'Coordinación con contratistas y residentes',
  'Documentación de entrega',
  'Capacidad para proyectos de construcción e infraestructura',
  'Respuesta rápida ante requerimientos críticos',
]

export const processSteps = [
  'Levantamiento técnico',
  'Diagnóstico y alcance',
  'Propuesta técnica y económica',
  'Planeación de obra',
  'Ejecución y supervisión',
  'Pruebas, revisión y entrega',
]

export const projectTypes = [
  'Instalaciones eléctricas industriales',
  'Tableros y canalizaciones',
  'Subestaciones y transformadores',
  'Alumbrado y fuerza',
  'Mantenimiento eléctrico',
]

export const compliancePoints = [
  'Uso de materiales adecuados al tipo de instalación',
  'Identificación y orden en tableros y canalizaciones',
  'Revisión de cargas y capacidades',
  'Protección eléctrica y puesta a tierra',
  'Entrega ordenada de información técnica',
]

export const quickStats = [
  { value: '24 h', label: 'respuesta inicial', icon: TimerReset },
  { value: 'MT/BT', label: 'infraestructura eléctrica', icon: BadgeCheck },
  { value: 'Obra', label: 'coordinación en campo', icon: HardHat },
]
