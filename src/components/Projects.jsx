import { projects } from '../data/projects.js'
import AnimatedSection from './AnimatedSection.jsx'
import { ArrowRight, MapPin, Tag } from 'lucide-react'

export default function Projects() {
  return (
    <section id="proyectos" className="section-padding bg-mist">
      <div className="container-page">
        <AnimatedSection className="max-w-3xl mb-16">
          <h2 className="section-title text-navy">Trabajo en campo, resultados medibles</h2>
          <p className="section-copy">
            Cada proyecto se documenta con evidencia fotográfica, control de avance y criterios claros de entrega.
          </p>
        </AnimatedSection>

        <div className="grid gap-8 lg:grid-cols-2 xl:grid-cols-3">
          {projects.map((project, index) => (
            <AnimatedSection 
              key={project.id} 
              delay={index * 0.1}
              className="group flex flex-col rounded bg-white border border-gray/20 shadow-sm overflow-hidden"
            >
              <div className="relative aspect-[4/3] overflow-hidden bg-gray/10">
                <img 
                  src={project.image} 
                  alt={project.title} 
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                  loading="lazy"
                />
                <div className="absolute top-4 left-4 bg-navy text-white text-xs font-bold px-3 py-1 rounded uppercase tracking-wider">
                  {project.category}
                </div>
              </div>
              
              <div className="flex flex-col flex-grow p-6">
                <h3 className="font-bold text-lg text-navy mb-3 line-clamp-2">{project.title}</h3>
                
                <div className="flex items-center gap-2 text-sm text-gray mb-2">
                  <MapPin size={16} className="shrink-0" />
                  <span className="truncate">{project.location}</span>
                </div>
                
                <div className="flex items-center gap-2 text-sm text-gray mb-4 pb-4 border-b border-gray/10">
                  <Tag size={16} className="shrink-0" />
                  <span className="truncate">{project.service}</span>
                </div>
                
                <p className="text-sm text-gray leading-relaxed mb-6 flex-grow line-clamp-3">
                  {project.description}
                </p>
                
                <div className="mt-auto">
                  <button className="flex items-center gap-2 text-sm font-bold text-electric hover:text-navy transition-colors">
                    Ver proyecto
                    <ArrowRight size={16} />
                  </button>
                </div>
              </div>
            </AnimatedSection>
          ))}
        </div>
      </div>
    </section>
  )
}
