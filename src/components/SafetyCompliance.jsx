import { motion } from 'framer-motion'
import { Check, ShieldCheck } from 'lucide-react'
import SectionHeader from './SectionHeader.jsx'
import { compliancePoints } from '../data/content.js'

export default function SafetyCompliance() {
  return (
    <section className="section-padding bg-mist">
      <div className="container-page grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <div>
          <SectionHeader
            eyebrow="Cumplimiento y seguridad"
            title="Seguridad, orden y cumplimiento en cada instalación"
            copy="Trabajamos con enfoque en seguridad eléctrica, continuidad operativa y cumplimiento de buenas prácticas aplicables a instalaciones de media y baja tensión."
          />
          <div className="mt-8 grid gap-3">
            {compliancePoints.map((point) => (
              <motion.div
                key={point}
                className="flex gap-3 rounded-lg bg-white p-4 shadow-sm"
                initial={{ opacity: 0, x: -12 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.4 }}
              >
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-electric text-navy">
                  <Check size={17} strokeWidth={3} />
                </span>
                <p className="font-semibold leading-7 text-slate-700">{point}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          className="relative overflow-hidden rounded-lg bg-navy p-8 text-white shadow-industrial"
          initial={{ opacity: 0, scale: 0.96 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.55 }}
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(245,180,0,0.18),transparent_28%)]" />
          <div className="relative">
            <ShieldCheck className="text-electric" size={48} />
            <h3 className="mt-8 text-3xl font-extrabold leading-tight">Control técnico antes, durante y después de la instalación.</h3>
            <p className="mt-5 leading-8 text-slate-300">
              Una instalación eléctrica debe poder revisarse, entenderse y mantenerse. Por eso damos prioridad al orden,
              identificación, protección y documentación de entrega.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
