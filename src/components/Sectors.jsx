import { motion } from 'framer-motion'
import SectionHeader from './SectionHeader.jsx'
import { sectors } from '../data/content.js'

export default function Sectors() {
  return (
    <section id="sectores" className="section-padding bg-white">
      <div className="container-page">
        <SectionHeader
          eyebrow="Sectores atendidos"
          title="Soluciones eléctricas para infraestructura industrial, comercial y pública"
          copy="Atendemos proyectos nuevos, ampliaciones, correcciones y mantenimiento para inmuebles con necesidades eléctricas formales y operación activa."
        />

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sectors.map((sector, index) => {
            const Icon = sector.icon
            return (
              <motion.article
                key={sector.title}
                className="flex items-center gap-4 rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.45, delay: (index % 3) * 0.05 }}
              >
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md bg-navy text-electric">
                  <Icon size={22} />
                </span>
                <h3 className="text-base font-extrabold text-navy">{sector.title}</h3>
              </motion.article>
            )
          })}
        </div>
      </div>
    </section>
  )
}
