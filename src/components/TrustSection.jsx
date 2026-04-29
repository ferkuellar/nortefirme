import { motion } from 'framer-motion'
import SectionHeader from './SectionHeader.jsx'
import { trustCards } from '../data/content.js'

export default function TrustSection() {
  return (
    <section id="nosotros" className="section-padding bg-white">
      <div className="container-page">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-end">
          <SectionHeader
            eyebrow="Criterio técnico"
            title="Infraestructura eléctrica con criterio técnico y ejecución responsable"
            copy="Sabemos que una instalación eléctrica mal planeada genera retrasos, sobrecostos, riesgos operativos y problemas de seguridad. Por eso trabajamos con procesos claros, personal capacitado y enfoque en cumplimiento técnico desde el primer levantamiento hasta la entrega final."
          />
          <div className="rounded-lg bg-mist p-6 text-sm font-semibold leading-7 text-slate-700">
            Norte Firme instala infraestructura eléctrica segura, ordenada y confiable para proyectos que exigen control
            técnico y respuesta real.
          </div>
        </div>

        <div className="mt-12 grid gap-5 md:grid-cols-3">
          {trustCards.map((card, index) => {
            const Icon = card.icon
            return (
              <motion.article
                key={card.title}
                className="card p-6"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.5, delay: index * 0.08 }}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-md bg-navy text-electric">
                  <Icon size={24} />
                </div>
                <h3 className="mt-5 text-xl font-extrabold text-navy">{card.title}</h3>
                <p className="mt-3 leading-7 text-slate-600">{card.description}</p>
              </motion.article>
            )
          })}
        </div>
      </div>
    </section>
  )
}
