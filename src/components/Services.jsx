import { motion } from 'framer-motion'
import SectionHeader from './SectionHeader.jsx'
import { services } from '../data/content.js'

export default function Services() {
  return (
    <section id="servicios" className="section-padding bg-mist">
      <div className="container-page">
        <SectionHeader
          align="center"
          eyebrow="Servicios"
          title="Servicios eléctricos de media y baja tensión"
          copy="Soluciones técnicas para construir, adecuar, mantener y entregar infraestructura eléctrica en proyectos donde la continuidad y la seguridad son prioridad."
        />

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((service, index) => {
            const Icon = service.icon
            return (
              <motion.article
                key={service.title}
                className="card min-h-56 p-6"
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.45, delay: (index % 3) * 0.06 }}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-md bg-steel/10 text-steel">
                    <Icon size={24} />
                  </div>
                  <span className="h-1.5 w-14 rounded-full bg-electric" />
                </div>
                <h3 className="mt-5 text-lg font-extrabold leading-6 text-navy">{service.title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">{service.description}</p>
              </motion.article>
            )
          })}
        </div>
      </div>
    </section>
  )
}
