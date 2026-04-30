import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowUpRight, CheckCircle2, Gauge, MapPin, X } from 'lucide-react'
import SectionHeader from '../SectionHeader.jsx'
import { featuredProjectPlaceholders } from '../../data/projects.js'
import usePrefersReducedMotion from '../../hooks/usePrefersReducedMotion.js'

function normalizeProject(project) {
  return {
    id: project.id,
    title: project.title,
    category: project.category || project.service_type || 'Proyecto eléctrico',
    location:
      project.location ||
      [project.location_city, project.location_state].filter(Boolean).join(', ') ||
      'Chihuahua, México',
    voltageType: project.voltageType || project.voltage_type || 'Media y baja tensión',
    summary: project.summary || project.short_description || project.description,
    description: project.description || project.summary || project.short_description,
    clientName: project.clientName || project.client_name || 'Cliente industrial confidencial',
    technicalScope: project.technicalScope || project.technical_scope,
    deliverables: project.deliverables || [],
    solution: project.solution,
    results: project.results,
    image: project.image || project.cover_image_url,
    galleryImages: project.gallery_images || project.galleryImages || [],
    slug: project.slug,
  }
}

export default function ProjectShowcase3D() {
  const [projects, setProjects] = useState(featuredProjectPlaceholders)
  const [source, setSource] = useState('fallback')
  const [activeProject, setActiveProject] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const reducedMotion = usePrefersReducedMotion()

  useEffect(() => {
    const controller = new AbortController()

    async function loadProjects() {
      try {
        const response = await fetch('/api/v1/public/projects/featured', { signal: controller.signal })
        if (!response.ok) throw new Error('Featured projects unavailable')
        const data = await response.json()
        const items = Array.isArray(data.items) ? data.items : []
        if (items.length) {
          setProjects(items.map(normalizeProject))
          setSource('api')
        }
      } catch (error) {
        if (error.name !== 'AbortError') setSource('fallback')
      }
    }

    loadProjects()
    return () => controller.abort()
  }, [])

  useEffect(() => {
    if (!activeProject) return undefined

    const onKeyDown = (event) => {
      if (event.key === 'Escape') {
        setActiveProject(null)
      }
    }

    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', onKeyDown)

    return () => {
      document.body.style.overflow = ''
      window.removeEventListener('keydown', onKeyDown)
    }
  }, [activeProject])

  async function openProject(project) {
    setActiveProject(project)

    if (source !== 'api' || !project.slug) {
      return
    }

    setDetailLoading(true)
    try {
      const response = await fetch(`/api/v1/public/projects/${project.slug}`)
      if (!response.ok) throw new Error('Project detail unavailable')
      const detail = await response.json()
      setActiveProject(normalizeProject(detail))
    } catch {
      setActiveProject(project)
    } finally {
      setDetailLoading(false)
    }
  }

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
            {source === 'api'
              ? 'Proyectos destacados cargados desde el backend de Norte Firme.'
              : 'Esta sección está preparada para consumir GET /api/v1/public/projects/featured cuando el backend esté disponible.'}
          </p>
        </div>

        <div className="mt-12 grid gap-5 md:grid-cols-2 xl:grid-cols-5">
          {projects.map((project, index) => (
            <motion.article
              key={project.id}
              className="project-card-3d group relative min-h-[25rem] overflow-hidden rounded-lg bg-navy shadow-sm"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              whileHover={reducedMotion ? undefined : { y: -7, rotateX: 1.2, rotateY: index % 2 ? 1 : -1 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.5, delay: index * 0.05 }}
            >
              <button
                type="button"
                className="block h-full min-h-[25rem] w-full cursor-pointer text-left focus:outline-none focus:ring-4 focus:ring-electric/50"
                onClick={() => openProject(project)}
                aria-label={`Abrir información del proyecto ${project.title}`}
              >
                <img
                  src={project.image}
                  alt={project.title}
                  className="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/70 to-navy/10" />
                <div className="relative flex h-full min-h-[25rem] flex-col justify-between p-5">
                  <div className="flex items-start justify-between gap-3">
                    <span className="rounded-md bg-electric px-3 py-2 text-xs font-extrabold uppercase tracking-[0.12em] text-navy">
                      {project.category.replaceAll('_', ' ')}
                    </span>
                    <ArrowUpRight className="shrink-0 text-electric" size={24} />
                  </div>
                  <div>
                    <div className="mb-3 grid gap-2 text-xs font-bold uppercase tracking-[0.12em] text-slate-200">
                      <span className="inline-flex items-center gap-1.5">
                        <MapPin size={14} />
                        {project.location}
                      </span>
                      <span className="inline-flex items-center gap-1.5">
                        <Gauge size={14} />
                        {project.voltageType.replaceAll('_', ' ')}
                      </span>
                    </div>
                    <h3 className="text-lg font-extrabold leading-6 text-white">{project.title}</h3>
                    <p className="mt-3 line-clamp-4 text-sm font-medium leading-6 text-slate-200">{project.summary}</p>
                    <span className="mt-5 inline-flex items-center gap-2 rounded-md border border-white/20 px-3 py-2 text-xs font-extrabold uppercase tracking-[0.12em] text-white transition group-hover:border-electric group-hover:text-electric">
                      Ver proyecto
                      <ArrowUpRight size={14} />
                    </span>
                  </div>
                </div>
              </button>
            </motion.article>
          ))}
        </div>
      </div>

      {activeProject && (
        <div
          className="fixed inset-0 z-[80] grid place-items-center bg-navy/82 px-4 py-6 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="project-modal-title"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setActiveProject(null)
          }}
        >
          <motion.div
            className="max-h-[92vh] w-full max-w-5xl overflow-hidden rounded-lg bg-white shadow-2xl"
            initial={{ opacity: 0, y: 18, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.22 }}
          >
            <div className="grid max-h-[92vh] overflow-y-auto lg:grid-cols-[0.95fr_1.05fr]">
              <div className="relative min-h-72 bg-navy lg:min-h-full">
                <img src={activeProject.image} alt={activeProject.title} className="h-full min-h-72 w-full object-cover" />
                <div className="absolute inset-0 bg-gradient-to-t from-navy/75 to-transparent" />
                <div className="absolute bottom-5 left-5 right-5">
                  <p className="text-xs font-extrabold uppercase tracking-[0.16em] text-electric">
                    {activeProject.category.replaceAll('_', ' ')}
                  </p>
                  <p className="mt-2 inline-flex items-center gap-2 text-sm font-bold text-white">
                    <MapPin size={16} />
                    {activeProject.location}
                  </p>
                </div>
              </div>

              <div className="p-6 sm:p-8">
                <div className="flex items-start justify-between gap-5">
                  <div>
                    <p className="text-xs font-extrabold uppercase tracking-[0.18em] text-steel">
                      Evidencia de proyecto
                    </p>
                    <h3 id="project-modal-title" className="mt-3 text-3xl font-extrabold leading-tight text-navy">
                      {activeProject.title}
                    </h3>
                  </div>
                  <button
                    type="button"
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-slate-200 text-slate-600 transition hover:bg-mist hover:text-navy"
                    onClick={() => setActiveProject(null)}
                    aria-label="Cerrar información del proyecto"
                  >
                    <X size={20} />
                  </button>
                </div>

                <div className="mt-5 grid gap-3 text-sm font-bold text-slate-700 sm:grid-cols-3">
                  <span className="rounded-md bg-mist px-3 py-2">{activeProject.voltageType.replaceAll('_', ' ')}</span>
                  <span className="rounded-md bg-mist px-3 py-2">{activeProject.clientName}</span>
                  <span className="rounded-md bg-mist px-3 py-2">{detailLoading ? 'Cargando detalle...' : 'Información técnica'}</span>
                </div>

                <p className="mt-6 leading-8 text-slate-700">{activeProject.description}</p>

                {activeProject.technicalScope && (
                  <div className="mt-7 rounded-lg border border-slate-200 bg-mist p-5">
                    <h4 className="font-extrabold text-navy">Alcance técnico</h4>
                    <p className="mt-3 text-sm leading-7 text-slate-700">{activeProject.technicalScope}</p>
                  </div>
                )}

                {activeProject.deliverables?.length > 0 && (
                  <div className="mt-7">
                    <h4 className="font-extrabold text-navy">Entregables</h4>
                    <div className="mt-3 grid gap-2 sm:grid-cols-2">
                      {activeProject.deliverables.map((item) => (
                        <div key={item} className="flex gap-2 text-sm font-semibold text-slate-700">
                          <CheckCircle2 className="mt-0.5 shrink-0 text-electric" size={17} />
                          {item}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-7 grid gap-5 sm:grid-cols-2">
                  {activeProject.solution && (
                    <div>
                      <h4 className="font-extrabold text-navy">Solución</h4>
                      <p className="mt-2 text-sm leading-7 text-slate-700">{activeProject.solution}</p>
                    </div>
                  )}
                  {activeProject.results && (
                    <div>
                      <h4 className="font-extrabold text-navy">Resultado</h4>
                      <p className="mt-2 text-sm leading-7 text-slate-700">{activeProject.results}</p>
                    </div>
                  )}
                </div>

                <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                  <a href="#contacto" onClick={() => setActiveProject(null)} className="btn-primary">
                    Solicitar cotización
                    <ArrowUpRight size={17} />
                  </a>
                  <button
                    type="button"
                    className="inline-flex items-center justify-center rounded-md border border-slate-300 px-5 py-3 text-sm font-extrabold text-navy transition hover:bg-mist"
                    onClick={() => setActiveProject(null)}
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </section>
  )
}
