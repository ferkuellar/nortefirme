import { ShieldAlert, HardHat, FileBadge } from 'lucide-react'
import AnimatedSection from './AnimatedSection.jsx'

const blocks = [
  {
    title: 'Seguridad eléctrica',
    description: 'Evitamos riesgos operativos y garantizamos la protección del personal y las instalaciones mediante el apego a normativas.',
    icon: ShieldAlert
  },
  {
    title: 'Planeación y control de obra',
    description: 'Reducimos sobrecostos y retrasos con cronogramas claros, logística de materiales y supervisión técnica constante.',
    icon: HardHat
  },
  {
    title: 'Cumplimiento técnico',
    description: 'Aseguramos que la instalación final cumpla con los estándares requeridos para certificaciones y continuidad operativa.',
    icon: FileBadge
  }
]

export default function ProblemSection() {
  return (
    <section className="section-padding bg-white">
      <div className="container-page">
        <div className="grid gap-12 lg:grid-cols-[1fr_1fr] items-start">
          
          <AnimatedSection>
            <h2 className="section-title">
              Infraestructura eléctrica con criterio técnico y ejecución responsable
            </h2>
            <p className="section-copy">
              Una instalación eléctrica mal planeada genera retrasos, sobrecostos, riesgos operativos y problemas de seguridad. Por eso trabajamos con procesos claros, personal capacitado y enfoque en cumplimiento técnico desde el primer levantamiento hasta la entrega final.
            </p>
          </AnimatedSection>

          <AnimatedSection staggerChildren={true} className="grid gap-6">
            {blocks.map((block, index) => {
              const Icon = block.icon
              return (
                <AnimatedSection key={index} as="div" className="flex gap-4 p-6 rounded bg-mist border border-gray/10">
                  <div className="flex shrink-0 h-12 w-12 items-center justify-center rounded bg-white text-navy shadow-sm">
                    <Icon size={24} />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-navy">{block.title}</h3>
                    <p className="mt-2 text-gray text-sm leading-relaxed">{block.description}</p>
                  </div>
                </AnimatedSection>
              )
            })}
          </AnimatedSection>
          
        </div>
      </div>
    </section>
  )
}
