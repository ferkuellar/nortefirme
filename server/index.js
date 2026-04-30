import cors from 'cors'
import express from 'express'
import { readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const app = express()
const port = process.env.PORT || 4000
const projectsFile = path.join(__dirname, 'data', 'projects.json')

app.use(cors({ origin: process.env.CORS_ORIGIN || true }))
app.use(express.json({ limit: '1mb' }))

async function readProjects() {
  const file = await readFile(projectsFile, 'utf8')
  return JSON.parse(file)
}

async function writeProjects(projects) {
  await writeFile(projectsFile, `${JSON.stringify(projects, null, 2)}\n`, 'utf8')
}

function slugify(value) {
  return value
    .toString()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function cleanProject(payload, existingId) {
  const title = String(payload.title || '').trim()
  const summary = String(payload.summary || '').trim()

  if (!title || !summary) {
    return { error: 'Los campos title y summary son obligatorios.' }
  }

  return {
    id: existingId || slugify(payload.id || title),
    title,
    category: String(payload.category || 'Proyecto eléctrico').trim(),
    location: String(payload.location || 'Chihuahua, México').trim(),
    status: String(payload.status || 'En portafolio').trim(),
    summary,
    image: String(payload.image || '').trim(),
    metrics: Array.isArray(payload.metrics)
      ? payload.metrics.map((metric) => String(metric).trim()).filter(Boolean).slice(0, 4)
      : [],
    featured: Boolean(payload.featured ?? true),
  }
}

function requireApiKey(req, res, next) {
  const configuredKey = process.env.PROJECTS_API_KEY

  if (!configuredKey) {
    next()
    return
  }

  if (req.get('x-api-key') !== configuredKey) {
    res.status(401).json({ error: 'API key inválida.' })
    return
  }

  next()
}

app.get('/api/health', (req, res) => {
  res.json({ ok: true, service: 'nortefirme-projects-api' })
})

app.get('/api/projects', async (req, res, next) => {
  try {
    const projects = await readProjects()
    const visibleProjects = req.query.featured === 'false' ? projects : projects.filter((project) => project.featured)
    res.json({ projects: visibleProjects })
  } catch (error) {
    next(error)
  }
})

app.get('/api/projects/:id', async (req, res, next) => {
  try {
    const projects = await readProjects()
    const project = projects.find((item) => item.id === req.params.id)

    if (!project) {
      res.status(404).json({ error: 'Proyecto no encontrado.' })
      return
    }

    res.json({ project })
  } catch (error) {
    next(error)
  }
})

app.post('/api/projects', requireApiKey, async (req, res, next) => {
  try {
    const projects = await readProjects()
    const project = cleanProject(req.body)

    if (project.error) {
      res.status(400).json(project)
      return
    }

    if (projects.some((item) => item.id === project.id)) {
      res.status(409).json({ error: 'Ya existe un proyecto con ese id.' })
      return
    }

    projects.unshift(project)
    await writeProjects(projects)
    res.status(201).json({ project })
  } catch (error) {
    next(error)
  }
})

app.put('/api/projects/:id', requireApiKey, async (req, res, next) => {
  try {
    const projects = await readProjects()
    const index = projects.findIndex((item) => item.id === req.params.id)

    if (index === -1) {
      res.status(404).json({ error: 'Proyecto no encontrado.' })
      return
    }

    const project = cleanProject(req.body, req.params.id)

    if (project.error) {
      res.status(400).json(project)
      return
    }

    projects[index] = project
    await writeProjects(projects)
    res.json({ project })
  } catch (error) {
    next(error)
  }
})

app.delete('/api/projects/:id', requireApiKey, async (req, res, next) => {
  try {
    const projects = await readProjects()
    const nextProjects = projects.filter((item) => item.id !== req.params.id)

    if (nextProjects.length === projects.length) {
      res.status(404).json({ error: 'Proyecto no encontrado.' })
      return
    }

    await writeProjects(nextProjects)
    res.status(204).send()
  } catch (error) {
    next(error)
  }
})

app.use((error, req, res, next) => {
  console.error(error)
  res.status(500).json({ error: 'No fue posible procesar la solicitud.' })
})

app.listen(port, () => {
  console.log(`Norte Firme projects API running on http://localhost:${port}`)
})
