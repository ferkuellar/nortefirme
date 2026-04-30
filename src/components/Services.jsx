import { services } from '../data/services.js'
import ServiceCard from './ServiceCard.jsx'
import AnimatedSection from './AnimatedSection.jsx'

export default function Services() {
  return (
    <section id="servicios" className="section-padding bg-mist">
      <div className="container-page">
        <AnimatedSection className="text-center max-w-3xl mx-auto mb-16">
          <p className="eyebrow mb-3">Servicios</p>
          <h2 className="section-title text-navy mx-auto">Servicios eléctricos de media y baja tensión</h2>
          <p className="section-copy mx-auto">
            Soluciones para proyectos que requieren orden, seguridad y continuidad operativa.
          </p>
        </AnimatedSection>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {services.map((service, index) => (
            <ServiceCard key={service.title} service={service} index={index} />
          ))}
        </div>
      </div>
    </section>
  )
}
