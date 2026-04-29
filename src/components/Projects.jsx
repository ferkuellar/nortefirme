import { motion } from 'framer-motion'
import { ArrowUpRight } from 'lucide-react'
import SectionHeader from './SectionHeader.jsx'
import { projectTypes } from '../data/content.js'

const projectImages = [
  'https://images.unsplash.com/photo-1581092921461-eab62e97a780?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1613665813446-82a78c468a1d?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1581092335397-9583eb92d232?auto=format&fit=crop&w=900&q=80',
]

export default function Projects() {
  return (
    <section id="proyectos" className="section-padding bg-white">
      <div className="container-page">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-end">
          <SectionHeader
            eyebrow="Proyectos y evidencia"
            title="Trabajo en campo, resultados medibles"
            copy="Cada proyecto se documenta con evidencia fotográfica, control de avance y criterios claros de entrega."
          />
          <p className="rounded-lg border-l-4 border-electric bg-mist p-5 text-sm font-semibold leading-7 text-slate-700">
            Esta sección está lista para integrar fotografías reales de obra, avances, tableros, canalizaciones y entregables
            técnicos cuando el portafolio se publique.
          </p>
        </div>

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-5">
          {projectTypes.map((type, index) => (
            <motion.article
              key={type}
              className="group relative min-h-72 overflow-hidden rounded-lg bg-navy shadow-sm"
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.5, delay: index * 0.05 }}
            >
              <img src={projectImages[index]} alt="" className="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-105" />
              <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/45 to-transparent" />
              <div className="relative flex h-full min-h-72 flex-col justify-end p-5">
                <ArrowUpRight className="mb-auto self-end text-electric" size={24} />
                <h3 className="text-lg font-extrabold leading-6 text-white">{type}</h3>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  )
}
