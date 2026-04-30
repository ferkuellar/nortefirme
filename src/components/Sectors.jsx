import { sectors } from '../data/sectors.js'
import AnimatedSection from './AnimatedSection.jsx'

export default function Sectors() {
  return (
    <section id="sectores" className="section-padding bg-white border-t border-gray/10">
      <div className="container-page">
        <AnimatedSection className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="section-title text-navy mx-auto">Soluciones eléctricas para infraestructura industrial, comercial y pública</h2>
        </AnimatedSection>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sectors.map((sector, index) => {
            const Icon = sector.icon
            return (
              <AnimatedSection 
                key={sector.title} 
                delay={index * 0.08}
                className="group flex gap-4 p-5 rounded border border-gray/10 bg-white transition-colors hover:bg-mist"
              >
                <div className="flex shrink-0 h-12 w-12 items-center justify-center rounded bg-mist text-steel group-hover:bg-white group-hover:text-electric transition-colors">
                  <Icon size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-navy">{sector.title}</h3>
                  <p className="mt-1 text-sm text-gray">{sector.description}</p>
                </div>
              </AnimatedSection>
            )
          })}
        </div>
      </div>
    </section>
  )
}
