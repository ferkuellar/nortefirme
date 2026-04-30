import AnimatedSection from './AnimatedSection.jsx'
import { CheckCircle2 } from 'lucide-react'

const checklist = [
  'Uso de materiales adecuados al tipo de instalación',
  'Identificación y orden en tableros y canalizaciones',
  'Revisión de cargas y capacidades',
  'Protección eléctrica y puesta a tierra',
  'Entrega ordenada de información técnica'
]

export default function SafetyCompliance() {
  return (
    <section className="section-padding bg-navy text-white">
      <div className="container-page">
        <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr] items-center">
          
          <AnimatedSection>
            <h2 className="section-title text-white">
              Seguridad, orden y cumplimiento en cada instalación
            </h2>
            <p className="mt-6 text-lg text-mist leading-relaxed max-w-2xl">
              Trabajamos con enfoque en seguridad eléctrica, continuidad operativa y buenas prácticas aplicables a instalaciones de media y baja tensión.
            </p>
          </AnimatedSection>

          <AnimatedSection staggerChildren={true} className="grid gap-4 bg-white/5 border border-white/10 p-8 rounded">
            {checklist.map((item, index) => (
              <AnimatedSection key={index} as="div" className="flex items-start gap-4">
                <CheckCircle2 className="text-electric shrink-0 mt-0.5" size={24} />
                <span className="text-white font-medium">{item}</span>
              </AnimatedSection>
            ))}
          </AnimatedSection>

        </div>
      </div>
    </section>
  )
}
