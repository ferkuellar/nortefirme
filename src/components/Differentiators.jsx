import { 
  ClipboardList, 
  Calculator, 
  LayoutList, 
  ShieldCheck, 
  Users, 
  FolderCheck, 
  Building2, 
  Timer 
} from 'lucide-react'
import AnimatedSection from './AnimatedSection.jsx'

const differentiators = [
  { icon: ClipboardList, text: 'Atención técnica desde el levantamiento' },
  { icon: Calculator, text: 'Presupuestos claros y defendibles' },
  { icon: LayoutList, text: 'Ejecución ordenada en obra' },
  { icon: ShieldCheck, text: 'Seguridad para personal e instalaciones' },
  { icon: Users, text: 'Coordinación con contratistas y residentes' },
  { icon: FolderCheck, text: 'Documentación de entrega' },
  { icon: Building2, text: 'Capacidad para proyectos de construcción e infraestructura' },
  { icon: Timer, text: 'Respuesta rápida ante requerimientos críticos' }
]

export default function Differentiators() {
  return (
    <section className="section-padding bg-white border-t border-gray/10">
      <div className="container-page">
        <AnimatedSection className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="section-title text-navy mx-auto">Por qué elegir Norte Firme</h2>
        </AnimatedSection>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {differentiators.map((diff, index) => {
            const Icon = diff.icon
            return (
              <AnimatedSection 
                key={index} 
                delay={index * 0.05}
                className="flex items-center gap-4 p-5 rounded border border-gray/10 bg-mist hover:bg-white hover:shadow-sm transition-all"
              >
                <div className="flex shrink-0 h-10 w-10 items-center justify-center rounded bg-navy text-electric">
                  <Icon size={20} />
                </div>
                <span className="font-semibold text-sm text-navy leading-tight">{diff.text}</span>
              </AnimatedSection>
            )
          })}
        </div>
      </div>
    </section>
  )
}
