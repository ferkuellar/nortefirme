import { motion } from 'framer-motion'
import { ArrowRight, ChevronDown, CheckCircle2 } from 'lucide-react'
import { metrics, quickStats } from '../data/content.js'
import HeroEvidencePanel from './hero/HeroEvidencePanel.jsx'
import TechnicalGridBackground from './visual/TechnicalGridBackground.jsx'

const heroImage =
  'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1800&q=82'

export default function Hero() {
  return (
    <section id="inicio" className="relative isolate min-h-[calc(100vh-5rem)] overflow-hidden bg-navy text-white">
      <div className="absolute inset-0 -z-20 bg-cover bg-center" style={{ backgroundImage: `url(${heroImage})` }} />
      <div className="absolute inset-0 -z-10 bg-[linear-gradient(90deg,rgba(11,31,51,0.94),rgba(11,31,51,0.78)_44%,rgba(11,31,51,0.5))]" />
      <div className="absolute inset-x-0 bottom-0 -z-10 h-40 bg-gradient-to-t from-navy to-transparent" />
      <TechnicalGridBackground className="opacity-35" />

      <div className="container-page grid min-h-[calc(100vh-5rem)] items-center gap-10 py-16 lg:grid-cols-[1.05fr_0.95fr] lg:py-20">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
          <p className="inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/10 px-3 py-2 text-xs font-bold uppercase tracking-[0.18em] text-electric backdrop-blur">
            Infraestructura eléctrica MT/BT
          </p>
          <h1 className="mt-6 max-w-4xl text-4xl font-extrabold leading-[1.05] text-white sm:text-5xl lg:text-6xl">
            Instalaciones eléctricas de media y baja tensión para proyectos que no pueden fallar
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-200 sm:text-xl">
            En Norte Firme diseñamos, instalamos y mantenemos infraestructura eléctrica segura, ordenada y confiable para
            proyectos industriales, comerciales y de construcción.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <a href="#contacto" className="btn-primary">
              Solicitar cotización
              <ArrowRight size={18} />
            </a>
            <a href="#servicios" className="btn-secondary">
              Ver servicios
              <ChevronDown size={18} />
            </a>
          </div>
        </motion.div>

        <motion.div
          className="grid gap-4 lg:justify-self-end"
          initial={{ opacity: 0, x: 28 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.75, delay: 0.1 }}
        >
          <HeroEvidencePanel />
          <div className="grid gap-3 sm:grid-cols-2">
            {metrics.map((metric) => (
              <div key={metric} className="rounded-lg border border-white/18 bg-white/12 p-4 shadow-2xl shadow-slate-950/20 backdrop-blur-md">
                <CheckCircle2 className="text-electric" size={22} />
                <p className="mt-3 text-sm font-bold leading-6 text-white">{metric}</p>
              </div>
            ))}
          </div>
          <div className="grid gap-3 rounded-lg border border-white/18 bg-navy/70 p-4 backdrop-blur-md sm:grid-cols-3">
            {quickStats.map((stat) => {
              const Icon = stat.icon
              return (
                <div key={stat.label} className="flex items-center gap-3">
                  <Icon className="shrink-0 text-electric" size={22} />
                  <span>
                    <span className="block text-lg font-extrabold">{stat.value}</span>
                    <span className="block text-xs font-semibold uppercase tracking-[0.12em] text-slate-300">{stat.label}</span>
                  </span>
                </div>
              )
            })}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
