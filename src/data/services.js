import { 
  Zap, 
  Settings, 
  Building2, 
  BatteryCharging, 
  ShieldCheck, 
  Cable, 
  Lightbulb, 
  CheckSquare,
  Wrench,
  Search,
  Power,
  Factory
} from 'lucide-react'

export const services = [
  {
    title: 'Instalaciones eléctricas en baja tensión',
    description: 'Diseño y ejecución de redes eléctricas de distribución interna para naves y edificios.',
    icon: Zap
  },
  {
    title: 'Media tensión',
    description: 'Acometidas, transiciones y líneas de distribución en media tensión.',
    icon: Power
  },
  {
    title: 'Subestaciones eléctricas',
    description: 'Suministro, montaje y puesta en marcha de subestaciones tipo poste, pedestal y encapsuladas.',
    icon: BatteryCharging
  },
  {
    title: 'Transformadores',
    description: 'Instalación, mantenimiento y pruebas a transformadores de distribución e instrumentación.',
    icon: Settings
  },
  {
    title: 'Tableros generales y derivados',
    description: 'Armado, instalación y peinado de tableros de distribución, CCM y centros de carga.',
    icon: CheckSquare
  },
  {
    title: 'Canalizaciones eléctricas',
    description: 'Tendido de tubería conduit, charola portacable y ductos subterráneos.',
    icon: Cable
  },
  {
    title: 'Alumbrado industrial y comercial',
    description: 'Sistemas de iluminación interior y exterior, cálculo de niveles y control.',
    icon: Lightbulb
  },
  {
    title: 'Sistemas de puesta a tierra',
    description: 'Redes de tierra física, medición de resistividad y sistemas pararrayos.',
    icon: ShieldCheck
  },
  {
    title: 'Mantenimiento preventivo y correctivo',
    description: 'Limpieza, reapriete, termografía y pruebas eléctricas a infraestructura.',
    icon: Wrench
  },
  {
    title: 'Diagnóstico y levantamientos',
    description: 'Evaluación de instalaciones existentes, actualización de diagramas y peritajes.',
    icon: Search
  },
  {
    title: 'Alimentadores eléctricos',
    description: 'Cálculo, tendido y conexión de circuitos alimentadores principales.',
    icon: Zap
  },
  {
    title: 'Obra eléctrica general',
    description: 'Soluciones llave en mano para naves industriales, comercios y edificios.',
    icon: Factory
  }
]
