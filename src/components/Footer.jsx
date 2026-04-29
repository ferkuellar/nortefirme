import { Zap } from 'lucide-react'
import { navItems } from '../data/content.js'

export default function Footer() {
  return (
    <footer className="bg-carbon text-white">
      <div className="container-page grid gap-10 py-12 lg:grid-cols-[1.2fr_0.8fr_1fr]">
        <div>
          <div className="flex items-center gap-3">
            <span className="flex h-11 w-11 items-center justify-center rounded-md bg-electric text-navy">
              <Zap size={24} />
            </span>
            <div>
              <p className="font-extrabold">Norte Firme Infraestructura y Construcción</p>
              <p className="mt-1 text-sm font-semibold text-slate-400">Servicios eléctricos de media y baja tensión</p>
            </div>
          </div>
        </div>

        <div>
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-electric">Links</p>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            {navItems
              .filter((item) => ['Inicio', 'Servicios', 'Sectores', 'Proyectos', 'Contacto'].includes(item.label))
              .map((item) => (
                <a key={item.href} href={item.href} className="font-semibold text-slate-300 transition hover:text-white">
                  {item.label}
                </a>
              ))}
          </div>
        </div>

        <div>
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-electric">Datos</p>
          <div className="mt-4 grid gap-2 text-sm font-semibold text-slate-300">
            <p>Chihuahua, México</p>
            <a href="mailto:contacto@nortefirme.com.mx" className="hover:text-white">contacto@nortefirme.com.mx</a>
            <a href="tel:614177711" className="hover:text-white">614 177 711</a>
          </div>
        </div>
      </div>
      <div className="border-t border-white/10 py-5">
        <div className="container-page text-sm font-semibold text-slate-400">
          © 2026 Norte Firme Infraestructura y Construcción. Todos los derechos reservados.
        </div>
      </div>
    </footer>
  )
}
