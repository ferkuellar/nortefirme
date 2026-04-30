import { useEffect, useMemo, useState } from 'react'
import {
  ArrowLeft,
  BadgeCheck,
  Eye,
  EyeOff,
  FileImage,
  ImagePlus,
  Loader2,
  LockKeyhole,
  LogOut,
  Plus,
  Star,
  UploadCloud,
} from 'lucide-react'

const API_BASE = '/api/v1'

const initialProject = {
  title: '',
  slug: '',
  short_description: '',
  description: '',
  client_name: '',
  client_is_confidential: true,
  sector: 'industrial',
  service_type: 'low_voltage_installation',
  voltage_type: 'low_voltage',
  location_city: 'Chihuahua',
  location_state: 'Chihuahua',
  status: 'completed',
  is_featured: true,
  is_published: false,
  cover_image_url: '',
  gallery_images: [],
  technical_scope: '',
  deliverables: [],
  challenges: '',
  solution: '',
  results: '',
  seo_title: '',
  seo_description: '',
  seo_keywords: [],
}

const sectors = [
  ['industrial', 'Industrial'],
  ['commercial', 'Comercial'],
  ['hospitality', 'Hoteles'],
  ['healthcare', 'Hospitales y clínicas'],
  ['public_infrastructure', 'Obra pública'],
  ['residential', 'Habitacional'],
  ['logistics', 'Logística'],
  ['corporate', 'Corporativo'],
  ['other', 'Otro'],
]

const services = [
  ['low_voltage_installation', 'Instalación baja tensión'],
  ['medium_voltage_installation', 'Instalación media tensión'],
  ['substation', 'Subestación'],
  ['transformer', 'Transformador'],
  ['electrical_panels', 'Tableros eléctricos'],
  ['grounding_system', 'Puesta a tierra'],
  ['industrial_lighting', 'Alumbrado industrial'],
  ['preventive_maintenance', 'Mantenimiento preventivo'],
  ['corrective_maintenance', 'Mantenimiento correctivo'],
  ['electrical_diagnosis', 'Diagnóstico eléctrico'],
  ['mixed_scope', 'Alcance mixto'],
]

const voltages = [
  ['low_voltage', 'Baja tensión'],
  ['medium_voltage', 'Media tensión'],
  ['low_and_medium_voltage', 'Media y baja tensión'],
  ['not_applicable', 'No aplica'],
]

const statuses = [
  ['planned', 'Planeado'],
  ['in_progress', 'En proceso'],
  ['completed', 'Completado'],
  ['on_hold', 'En pausa'],
  ['cancelled', 'Cancelado'],
]

const assetTypes = [
  ['cover_image', 'Portada'],
  ['gallery_image', 'Galería'],
  ['before_image', 'Antes'],
  ['after_image', 'Después'],
  ['delivery_evidence', 'Evidencia de entrega'],
  ['technical_document', 'Documento técnico PDF'],
]

function slugify(value) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function AdminInput({ label, className = '', ...props }) {
  return (
    <label className={`grid gap-2 text-sm font-extrabold text-navy ${className}`}>
      {label}
      <input
        {...props}
        className="rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-carbon outline-none transition focus:border-steel focus:ring-4 focus:ring-steel/10"
      />
    </label>
  )
}

function AdminSelect({ label, options, className = '', ...props }) {
  return (
    <label className={`grid gap-2 text-sm font-extrabold text-navy ${className}`}>
      {label}
      <select
        {...props}
        className="rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-carbon outline-none transition focus:border-steel focus:ring-4 focus:ring-steel/10"
      >
        {options.map(([value, text]) => (
          <option key={value} value={value}>
            {text}
          </option>
        ))}
      </select>
    </label>
  )
}

function AdminTextarea({ label, className = '', ...props }) {
  return (
    <label className={`grid gap-2 text-sm font-extrabold text-navy ${className}`}>
      {label}
      <textarea
        {...props}
        className="min-h-28 rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-semibold leading-7 text-carbon outline-none transition focus:border-steel focus:ring-4 focus:ring-steel/10"
      />
    </label>
  )
}

export default function AdminPortfolio() {
  const [token, setToken] = useState(() => localStorage.getItem('nortefirme_admin_token') || '')
  const [login, setLogin] = useState({ email: 'admin@nortefirme.com.mx', password: '' })
  const [adminSeed, setAdminSeed] = useState({
    email: 'admin@nortefirme.com.mx',
    full_name: 'Administrador Norte Firme',
    password: '',
    role: 'admin',
  })
  const [projects, setProjects] = useState([])
  const [activeProjectId, setActiveProjectId] = useState('')
  const [projectForm, setProjectForm] = useState(initialProject)
  const [deliverablesText, setDeliverablesText] = useState('')
  const [assetForm, setAssetForm] = useState({ asset_type: 'cover_image', description: '', sort_order: 0, file: null })
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const headers = useMemo(() => ({ Authorization: `Bearer ${token}` }), [token])
  const activeProject = projects.find((project) => String(project.id) === String(activeProjectId))

  async function request(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
        ...(token ? headers : {}),
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || error.error || 'No fue posible procesar la solicitud.')
    }

    if (response.status === 204) return null
    return response.json()
  }

  async function loadProjects() {
    if (!token) return
    const data = await request('/admin/projects?limit=50')
    setProjects(data.items)
    if (!activeProjectId && data.items[0]) setActiveProjectId(String(data.items[0].id))
  }

  useEffect(() => {
    if (!token) return undefined
    const timer = window.setTimeout(() => {
      loadProjects().catch((error) => setMessage(error.message))
    }, 0)
    return () => window.clearTimeout(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token])

  async function submitLogin(event) {
    event.preventDefault()
    setLoading(true)
    setMessage('')
    try {
      const data = await request('/auth/login', {
        method: 'POST',
        body: JSON.stringify(login),
        headers: {},
      })
      localStorage.setItem('nortefirme_admin_token', data.access_token)
      setToken(data.access_token)
      setMessage('Sesión iniciada.')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function registerAdmin(event) {
    event.preventDefault()
    setLoading(true)
    setMessage('')
    try {
      await request('/auth/register', {
        method: 'POST',
        body: JSON.stringify(adminSeed),
        headers: {},
      })
      setMessage('Administrador inicial creado. Ahora inicia sesión.')
      setLogin({ email: adminSeed.email, password: adminSeed.password })
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function createProject(event) {
    event.preventDefault()
    setLoading(true)
    setMessage('')
    try {
      const payload = {
        ...projectForm,
        slug: projectForm.slug || slugify(projectForm.title),
        deliverables: deliverablesText
          .split('\n')
          .map((item) => item.trim())
          .filter(Boolean),
        seo_keywords: [projectForm.title, projectForm.sector, projectForm.service_type, projectForm.voltage_type],
      }
      const data = await request('/admin/projects', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      setMessage('Proyecto creado. Sube una portada para poder publicarlo.')
      setProjectForm(initialProject)
      setDeliverablesText('')
      await loadProjects()
      setActiveProjectId(String(data.id))
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function uploadAsset(event) {
    event.preventDefault()
    if (!activeProjectId || !assetForm.file) {
      setMessage('Selecciona un proyecto y un archivo.')
      return
    }
    setLoading(true)
    setMessage('')
    try {
      const formData = new FormData()
      formData.append('asset_type', assetForm.asset_type)
      formData.append('description', assetForm.description)
      formData.append('sort_order', String(assetForm.sort_order))
      formData.append('file', assetForm.file)
      await request(`/admin/projects/${activeProjectId}/assets`, {
        method: 'POST',
        body: formData,
      })
      setMessage('Archivo subido y vinculado al proyecto.')
      setAssetForm({ asset_type: 'cover_image', description: '', sort_order: 0, file: null })
      await loadProjects()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function toggleProject(project, action) {
    setLoading(true)
    setMessage('')
    try {
      await request(`/admin/projects/${project.id}/${action}`, { method: 'PATCH' })
      setMessage('Proyecto actualizado.')
      await loadProjects()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    localStorage.removeItem('nortefirme_admin_token')
    setToken('')
    setProjects([])
  }

  if (!token) {
    return (
      <main className="min-h-screen bg-mist text-carbon">
        <section className="container-page grid min-h-screen items-center py-10 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="hidden h-full min-h-[34rem] overflow-hidden rounded-lg bg-navy text-white shadow-industrial lg:block">
            <div className="relative h-full p-10">
              <div className="absolute inset-0 technical-grid opacity-35" />
              <div className="relative">
                <a href="/" className="inline-flex items-center gap-2 text-sm font-bold text-electric">
                  <ArrowLeft size={17} />
                  Volver a la landing
                </a>
                <h1 className="mt-12 text-5xl font-extrabold leading-tight">
                  Panel de portafolio Norte Firme
                </h1>
                <p className="mt-5 max-w-xl text-lg leading-8 text-slate-300">
                  Administra proyectos, evidencia fotográfica, portadas, galerías y documentación técnica para mostrar obra real con control profesional.
                </p>
              </div>
            </div>
          </div>

          <div className="mx-auto w-full max-w-3xl rounded-lg bg-white p-6 shadow-industrial sm:p-8">
            <div className="mb-7 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-extrabold uppercase tracking-[0.18em] text-steel">Acceso privado</p>
                <h2 className="mt-2 text-3xl font-extrabold text-navy">Entrar al backend</h2>
              </div>
              <LockKeyhole className="text-electric" size={34} />
            </div>

            {message && <p className="mb-5 rounded-md bg-mist px-4 py-3 text-sm font-bold text-navy">{message}</p>}

            <div className="grid gap-8 lg:grid-cols-2">
              <form onSubmit={submitLogin} className="grid gap-4">
                <h3 className="font-extrabold text-navy">Iniciar sesión</h3>
                <AdminInput label="Correo" type="email" value={login.email} onChange={(event) => setLogin({ ...login, email: event.target.value })} />
                <AdminInput label="Contraseña" type="password" value={login.password} onChange={(event) => setLogin({ ...login, password: event.target.value })} />
                <button className="btn-primary" disabled={loading}>
                  {loading ? <Loader2 className="animate-spin" size={18} /> : <LockKeyhole size={18} />}
                  Entrar
                </button>
              </form>

              <form onSubmit={registerAdmin} className="grid gap-4 rounded-lg border border-slate-200 bg-mist p-5">
                <h3 className="font-extrabold text-navy">Crear admin inicial</h3>
                <AdminInput label="Correo" type="email" value={adminSeed.email} onChange={(event) => setAdminSeed({ ...adminSeed, email: event.target.value })} />
                <AdminInput label="Nombre" value={adminSeed.full_name} onChange={(event) => setAdminSeed({ ...adminSeed, full_name: event.target.value })} />
                <AdminInput label="Contraseña" type="password" value={adminSeed.password} onChange={(event) => setAdminSeed({ ...adminSeed, password: event.target.value })} />
                <button className="inline-flex items-center justify-center gap-2 rounded-md bg-navy px-5 py-3 text-sm font-extrabold text-white transition hover:bg-steel" disabled={loading}>
                  <Plus size={18} />
                  Crear admin
                </button>
              </form>
            </div>
          </div>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-mist text-carbon">
      <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="container-page flex min-h-20 items-center justify-between gap-4">
          <div>
            <p className="text-xs font-extrabold uppercase tracking-[0.18em] text-steel">Norte Firme</p>
            <h1 className="text-xl font-extrabold text-navy">Administración de portafolio</h1>
          </div>
          <div className="flex items-center gap-3">
            <a href="/" className="hidden rounded-md border border-slate-300 px-4 py-2 text-sm font-extrabold text-navy transition hover:bg-mist sm:inline-flex">
              Ver landing
            </a>
            <button onClick={logout} className="inline-flex items-center gap-2 rounded-md bg-navy px-4 py-2 text-sm font-extrabold text-white">
              <LogOut size={17} />
              Salir
            </button>
          </div>
        </div>
      </header>

      <section className="container-page grid gap-6 py-8 xl:grid-cols-[0.9fr_1.1fr]">
        <div className="grid gap-6">
          {message && <p className="rounded-md border-l-4 border-electric bg-white px-4 py-3 text-sm font-bold text-navy shadow-sm">{message}</p>}

          <form onSubmit={createProject} className="rounded-lg bg-white p-5 shadow-sm sm:p-6">
            <div className="mb-6 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-extrabold uppercase tracking-[0.16em] text-steel">Alta de proyecto</p>
                <h2 className="mt-2 text-2xl font-extrabold text-navy">Crear proyecto para portafolio</h2>
              </div>
              <FileImage className="text-electric" size={30} />
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <AdminInput className="sm:col-span-2" label="Título" value={projectForm.title} onChange={(event) => setProjectForm({ ...projectForm, title: event.target.value, slug: slugify(event.target.value) })} required />
              <AdminInput className="sm:col-span-2" label="Slug" value={projectForm.slug} onChange={(event) => setProjectForm({ ...projectForm, slug: event.target.value })} />
              <AdminInput className="sm:col-span-2" label="Resumen para tarjeta" maxLength={250} value={projectForm.short_description} onChange={(event) => setProjectForm({ ...projectForm, short_description: event.target.value })} required />
              <AdminTextarea className="sm:col-span-2" label="Descripción completa" value={projectForm.description} onChange={(event) => setProjectForm({ ...projectForm, description: event.target.value })} required />
              <AdminInput label="Cliente" value={projectForm.client_name} onChange={(event) => setProjectForm({ ...projectForm, client_name: event.target.value })} />
              <label className="flex items-center gap-3 rounded-md border border-slate-200 bg-mist px-4 py-3 text-sm font-extrabold text-navy">
                <input type="checkbox" checked={projectForm.client_is_confidential} onChange={(event) => setProjectForm({ ...projectForm, client_is_confidential: event.target.checked })} />
                Cliente confidencial
              </label>
              <AdminSelect label="Sector" options={sectors} value={projectForm.sector} onChange={(event) => setProjectForm({ ...projectForm, sector: event.target.value })} />
              <AdminSelect label="Servicio" options={services} value={projectForm.service_type} onChange={(event) => setProjectForm({ ...projectForm, service_type: event.target.value })} />
              <AdminSelect label="Tensión" options={voltages} value={projectForm.voltage_type} onChange={(event) => setProjectForm({ ...projectForm, voltage_type: event.target.value })} />
              <AdminSelect label="Estado" options={statuses} value={projectForm.status} onChange={(event) => setProjectForm({ ...projectForm, status: event.target.value })} />
              <AdminInput label="Ciudad" value={projectForm.location_city} onChange={(event) => setProjectForm({ ...projectForm, location_city: event.target.value })} />
              <AdminInput label="Estado" value={projectForm.location_state} onChange={(event) => setProjectForm({ ...projectForm, location_state: event.target.value })} />
              <AdminTextarea className="sm:col-span-2" label="Alcance técnico" value={projectForm.technical_scope} onChange={(event) => setProjectForm({ ...projectForm, technical_scope: event.target.value })} />
              <AdminTextarea className="sm:col-span-2" label="Entregables, uno por línea" value={deliverablesText} onChange={(event) => setDeliverablesText(event.target.value)} />
              <AdminTextarea label="Solución" value={projectForm.solution} onChange={(event) => setProjectForm({ ...projectForm, solution: event.target.value })} />
              <AdminTextarea label="Resultados" value={projectForm.results} onChange={(event) => setProjectForm({ ...projectForm, results: event.target.value })} />
            </div>

            <button className="mt-6 inline-flex items-center gap-2 rounded-md bg-navy px-5 py-3 text-sm font-extrabold text-white transition hover:bg-steel" disabled={loading}>
              {loading ? <Loader2 className="animate-spin" size={18} /> : <Plus size={18} />}
              Crear proyecto
            </button>
          </form>
        </div>

        <div className="grid gap-6">
          <section className="rounded-lg bg-white p-5 shadow-sm sm:p-6">
            <div className="mb-5 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-extrabold uppercase tracking-[0.16em] text-steel">Portafolio</p>
                <h2 className="mt-2 text-2xl font-extrabold text-navy">Proyectos registrados</h2>
              </div>
              <button className="rounded-md border border-slate-300 px-4 py-2 text-sm font-extrabold text-navy" onClick={loadProjects}>
                Actualizar
              </button>
            </div>

            <div className="grid gap-3">
              {projects.map((project) => (
                <button
                  key={project.id}
                  type="button"
                  onClick={() => setActiveProjectId(String(project.id))}
                  className={`grid gap-4 rounded-lg border p-4 text-left transition sm:grid-cols-[7rem_1fr] ${
                    String(project.id) === String(activeProjectId)
                      ? 'border-electric bg-yellow-50'
                      : 'border-slate-200 bg-white hover:bg-mist'
                  }`}
                >
                  <div className="h-24 overflow-hidden rounded-md bg-navy">
                    {project.cover_image_url ? (
                      <img src={project.cover_image_url} alt={project.title} className="h-full w-full object-cover" />
                    ) : (
                      <div className="flex h-full items-center justify-center text-electric">
                        <ImagePlus size={28} />
                      </div>
                    )}
                  </div>
                  <div>
                    <div className="flex flex-wrap gap-2">
                      <span className="rounded-md bg-navy px-2 py-1 text-xs font-extrabold text-white">{project.status}</span>
                      {project.is_published ? (
                        <span className="inline-flex items-center gap-1 rounded-md bg-emerald-100 px-2 py-1 text-xs font-extrabold text-emerald-800">
                          <Eye size={13} />
                          Publicado
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-1 text-xs font-extrabold text-slate-700">
                          <EyeOff size={13} />
                          Oculto
                        </span>
                      )}
                      {project.is_featured && (
                        <span className="inline-flex items-center gap-1 rounded-md bg-yellow-100 px-2 py-1 text-xs font-extrabold text-yellow-900">
                          <Star size={13} />
                          Destacado
                        </span>
                      )}
                    </div>
                    <h3 className="mt-3 font-extrabold text-navy">{project.title}</h3>
                    <p className="mt-1 line-clamp-2 text-sm leading-6 text-slate-600">{project.short_description}</p>
                  </div>
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-lg bg-white p-5 shadow-sm sm:p-6">
            <div className="mb-5">
              <p className="text-xs font-extrabold uppercase tracking-[0.16em] text-steel">Imágenes y evidencia</p>
              <h2 className="mt-2 text-2xl font-extrabold text-navy">Subir al proyecto seleccionado</h2>
              {activeProject && <p className="mt-2 text-sm font-bold text-slate-600">{activeProject.title}</p>}
            </div>

            <form onSubmit={uploadAsset} className="grid gap-4">
              <AdminSelect label="Tipo de archivo" options={assetTypes} value={assetForm.asset_type} onChange={(event) => setAssetForm({ ...assetForm, asset_type: event.target.value })} />
              <AdminInput label="Descripción de evidencia" value={assetForm.description} onChange={(event) => setAssetForm({ ...assetForm, description: event.target.value })} />
              <AdminInput label="Orden" type="number" min="0" value={assetForm.sort_order} onChange={(event) => setAssetForm({ ...assetForm, sort_order: Number(event.target.value) })} />
              <label className="grid gap-2 text-sm font-extrabold text-navy">
                Archivo
                <input
                  type="file"
                  accept={assetForm.asset_type === 'technical_document' ? 'application/pdf' : 'image/jpeg,image/png,image/webp'}
                  onChange={(event) => setAssetForm({ ...assetForm, file: event.target.files?.[0] || null })}
                  className="rounded-md border border-dashed border-slate-300 bg-mist px-4 py-5 text-sm font-bold text-slate-700"
                />
              </label>
              <button className="btn-primary" disabled={loading || !activeProjectId}>
                {loading ? <Loader2 className="animate-spin" size={18} /> : <UploadCloud size={18} />}
                Subir archivo
              </button>
            </form>

            {activeProject?.assets?.length > 0 && (
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {activeProject.assets.map((asset) => (
                  <div key={asset.id} className="rounded-lg border border-slate-200 p-3">
                    {asset.url.endsWith('.pdf') ? (
                      <div className="flex h-28 items-center justify-center rounded-md bg-mist text-sm font-extrabold text-navy">
                        PDF técnico
                      </div>
                    ) : (
                      <img src={asset.url} alt={asset.description || asset.filename} className="h-28 w-full rounded-md object-cover" />
                    )}
                    <p className="mt-2 text-xs font-extrabold uppercase tracking-[0.12em] text-steel">{asset.asset_type}</p>
                    <p className="mt-1 text-sm font-bold text-navy">{asset.description || asset.filename}</p>
                  </div>
                ))}
              </div>
            )}

            {activeProject && (
              <div className="mt-6 flex flex-wrap gap-3">
                <button
                  className="inline-flex items-center gap-2 rounded-md bg-navy px-4 py-2 text-sm font-extrabold text-white"
                  onClick={() => toggleProject(activeProject, activeProject.is_published ? 'unpublish' : 'publish')}
                  type="button"
                >
                  <BadgeCheck size={17} />
                  {activeProject.is_published ? 'Ocultar' : 'Publicar'}
                </button>
                <button
                  className="inline-flex items-center gap-2 rounded-md border border-slate-300 px-4 py-2 text-sm font-extrabold text-navy"
                  onClick={() => toggleProject(activeProject, activeProject.is_featured ? 'unfeature' : 'feature')}
                  type="button"
                >
                  <Star size={17} />
                  {activeProject.is_featured ? 'Quitar destacado' : 'Destacar'}
                </button>
              </div>
            )}
          </section>
        </div>
      </section>
    </main>
  )
}
