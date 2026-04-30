import { Zap, Factory, ShieldCheck, FileCheck } from 'lucide-react'
import AnimatedSection from './AnimatedSection.jsx'

const items = [
  { icon: Zap, text: 'Media y baja tensión' },
  { icon: Factory, text: 'Atención industrial y comercial' },
  { icon: ShieldCheck, text: 'Control técnico de obra' },
  { icon: FileCheck, text: 'Documentación de entrega' }
]

export default function TrustBar() {
  return (
    <section className="bg-mist py-8 border-b border-gray/20">
      <div className="container-page">
        <AnimatedSection staggerChildren={true} className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {items.map((item, index) => {
            const Icon = item.icon
            return (
              <AnimatedSection key={index} as="div" className="flex items-center gap-4 bg-white p-4 rounded border border-gray/10 shadow-sm">
                <div className="flex shrink-0 h-10 w-10 items-center justify-center rounded bg-navy text-electric">
                  <Icon size={20} />
                </div>
                <span className="font-semibold text-sm text-navy">{item.text}</span>
              </AnimatedSection>
            )
          })}
        </AnimatedSection>
      </div>
    </section>
  )
}
