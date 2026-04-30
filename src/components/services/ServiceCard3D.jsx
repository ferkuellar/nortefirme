import { motion } from 'framer-motion'
import usePrefersReducedMotion from '../../hooks/usePrefersReducedMotion.js'

export default function ServiceCard3D({ service, index }) {
  const Icon = service.icon
  const reducedMotion = usePrefersReducedMotion()

  return (
    <motion.article
      className="group service-card-3d relative min-h-56 overflow-hidden rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      whileHover={reducedMotion ? undefined : { y: -6, rotateX: 1.5, rotateY: -1.5 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.45, delay: (index % 3) * 0.05, ease: 'easeOut' }}
    >
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-electric to-transparent opacity-80" />
      <div className="absolute -right-12 -top-12 h-36 w-36 rounded-full bg-electric/0 blur-3xl transition group-hover:bg-electric/10" />
      <div className="relative flex items-start justify-between gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-md bg-steel/10 text-steel ring-1 ring-steel/10">
          <Icon size={24} />
        </div>
        <span className="mt-2 h-1.5 w-14 rounded-full bg-electric/85 shadow-[0_0_22px_rgba(245,180,0,0.25)]" />
      </div>
      <h3 className="relative mt-5 text-lg font-extrabold leading-6 text-navy">{service.title}</h3>
      <p className="relative mt-3 text-sm leading-7 text-slate-600">{service.description}</p>
    </motion.article>
  )
}
