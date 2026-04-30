import AnimatedSection from './AnimatedSection.jsx'
import { ArrowRight, ChevronDown, CheckCircle2 } from 'lucide-react'

const heroImage = 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1800&q=80'

const badges = [
  'Media y baja tensión',
  'Instalaciones industriales',
  'Respuesta técnica',
  'Cumplimiento y seguridad'
]

export default function Hero() {
  return (
    <section id="inicio" className="relative min-h-[90vh] bg-navy pt-20 flex items-center">
      {/* Background Image with Dark Overlay */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-40 mix-blend-luminosity" 
        style={{ backgroundImage: `url(${heroImage})` }} 
      />
      <div className="absolute inset-0 z-0 bg-gradient-to-r from-navy via-navy/90 to-navy/40" />

      <div className="container-page relative z-10 grid gap-12 py-16 lg:grid-cols-[1.1fr_0.9fr] lg:py-24 items-center">
        
        {/* Left Content */}
        <AnimatedSection delay={0.1}>
          <div className="max-w-3xl">
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl leading-[1.1]">
              Instalaciones eléctricas de media y baja tensión para proyectos que no pueden fallar
            </h1>
            <p className="mt-6 text-xl font-semibold text-mist leading-snug">
              Diseñamos, instalamos y mantenemos infraestructura eléctrica segura, ordenada y confiable para proyectos industriales, comerciales y de construcción.
            </p>
            <p className="mt-4 text-lg text-gray leading-relaxed">
              Trabajamos con criterio técnico, control de obra y enfoque en cumplimiento desde el levantamiento hasta la entrega final.
            </p>
            
            <div className="mt-10 flex flex-col sm:flex-row gap-4">
              <a href="#contacto" className="btn-primary">
                Solicitar cotización
                <ArrowRight size={18} />
              </a>
              <a href="#servicios" className="btn-secondary-white">
                Ver servicios
                <ChevronDown size={18} />
              </a>
            </div>
          </div>
        </AnimatedSection>

        {/* Right Content - 2D Floating Cards */}
        <AnimatedSection delay={0.3} staggerChildren={true} className="grid gap-4 sm:grid-cols-2 lg:justify-self-end w-full max-w-lg">
          {badges.map((badge, index) => (
            <AnimatedSection key={badge} as="div" className="flex items-center gap-3 bg-white/5 border border-white/10 p-5 rounded backdrop-blur-sm">
              <CheckCircle2 className="text-electric shrink-0" size={24} />
              <span className="font-semibold text-white">{badge}</span>
            </AnimatedSection>
          ))}
          
          {/* Main callout card */}
          <AnimatedSection as="div" className="sm:col-span-2 bg-white p-6 rounded shadow-lg mt-2 border-l-4 border-electric">
            <h3 className="font-extrabold text-navy text-xl">Atención especializada</h3>
            <p className="mt-2 text-gray text-sm leading-relaxed">
              Nuestros ingenieros y técnicos están capacitados para resolver requerimientos complejos en entornos industriales operativos sin interrumpir su producción.
            </p>
          </AnimatedSection>
        </AnimatedSection>

      </div>
    </section>
  )
}
