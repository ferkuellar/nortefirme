import { motion } from 'framer-motion'
import { CheckCircle2 } from 'lucide-react'
import SectionHeader from '../SectionHeader.jsx'
import { processSteps } from '../../data/content.js'
import usePrefersReducedMotion from '../../hooks/usePrefersReducedMotion.js'

export default function ProcessTimeline3D() {
  const reducedMotion = usePrefersReducedMotion()

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
          <div className="absolute left-6 top-0 h-full w-px bg-gradient-to-b from-steel/20 via-electric/70 to-steel/20 lg:left-0 lg:top-12 lg:h-px lg:w-full" />
          <div className="grid gap-5 lg:grid-cols-6">
            {processSteps.map((step, index) => (
              <motion.article
                key={step}
                className="group relative rounded-lg border border-slate-200 bg-white p-5 shadow-sm ring-1 ring-transparent"
                initial={{ opacity: 0, y: 22 }}
                whileInView={{ opacity: 1, y: 0 }}
                whileHover={reducedMotion ? undefined : { y: -5, rotateX: 1.2 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.45, delay: index * 0.05 }}
              >
                <div className="absolute inset-x-5 top-0 h-px bg-gradient-to-r from-transparent via-electric/70 to-transparent" />
                <span className="flex h-12 w-12 items-center justify-center rounded-md bg-navy text-base font-extrabold text-electric shadow-[0_14px_30px_rgba(11,31,51,0.22)]">
                  {String(index + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-5 text-base font-extrabold leading-6 text-navy">{step}</h3>
                <div className="mt-5 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.14em] text-slate-500">
                  <CheckCircle2 size={16} className="text-electric" />
                  Control técnico
                </div>
              </motion.article>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
