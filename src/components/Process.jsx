import { motion } from 'framer-motion'
import SectionHeader from './SectionHeader.jsx'
import { processSteps } from '../data/content.js'

export default function Process() {
  return (
    <section id="proceso" className="section-padding bg-mist">
      <div className="container-page">
        <SectionHeader
          align="center"
          eyebrow="Proceso de trabajo"
          title="Un proceso claro para evitar improvisaciones"
          copy="De la visita inicial a la entrega, cada etapa se define con alcance, responsables y criterios de revisión."
        />

        <div className="relative mt-14">
          <div className="absolute left-6 top-0 hidden h-full w-px bg-slate-300 md:block lg:left-0 lg:top-10 lg:h-px lg:w-full" />
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-6">
            {processSteps.map((step, index) => (
              <motion.article
                key={step}
                className="relative rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.45, delay: index * 0.05 }}
              >
                <span className="flex h-12 w-12 items-center justify-center rounded-md bg-navy text-base font-extrabold text-electric">
                  {String(index + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-5 text-base font-extrabold leading-6 text-navy">{step}</h3>
              </motion.article>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
