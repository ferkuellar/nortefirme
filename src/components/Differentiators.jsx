import { motion } from 'framer-motion'
import { CheckCircle2 } from 'lucide-react'
import SectionHeader from './SectionHeader.jsx'
import { differentiators } from '../data/content.js'

export default function Differentiators() {
  return (
    <section className="section-padding bg-navy text-white">
      <div className="container-page grid gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:items-start">
        <SectionHeader
          eyebrow="Por qué elegir Norte Firme"
          title="Respuesta técnica para obra real"
          copy="Trabajamos con claridad desde la primera visita para que cada decisión eléctrica tenga sustento técnico, costo defendible y ejecución controlada."
          className="[&_.eyebrow]:text-electric [&_.section-copy]:text-slate-300 [&_.section-title]:text-white"
        />

        <div className="grid gap-4 sm:grid-cols-2">
          {differentiators.map((item, index) => (
            <motion.div
              key={item}
              className="flex gap-3 rounded-lg border border-white/10 bg-white/8 p-5 backdrop-blur"
              initial={{ opacity: 0, x: 18 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.45, delay: (index % 4) * 0.05 }}
            >
              <CheckCircle2 className="mt-0.5 shrink-0 text-electric" size={21} />
              <p className="font-semibold leading-7 text-slate-100">{item}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
