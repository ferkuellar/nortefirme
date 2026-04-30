import SectionHeader from '../SectionHeader.jsx'
import TechnicalGridBackground from '../visual/TechnicalGridBackground.jsx'
import { services } from '../../data/services.js'
import ServiceCard3D from './ServiceCard3D.jsx'

export default function Services3DSection() {
  return (
    <section id="servicios" className="section-padding relative overflow-hidden bg-mist">
      <TechnicalGridBackground className="opacity-55" />
      <div className="container-page relative">
        <SectionHeader
          align="center"
          eyebrow="Servicios"
          title="Servicios eléctricos de media y baja tensión"
          copy="Soluciones técnicas para construir, adecuar, mantener y entregar infraestructura eléctrica en proyectos donde la continuidad y la seguridad son prioridad."
        />

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((service, index) => (
            <ServiceCard3D key={service.title} service={service} index={index} />
          ))}
        </div>
      </div>
    </section>
  )
}
