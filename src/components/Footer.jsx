import { Zap } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-carbon text-white pt-16 pb-8 border-t border-white/10">
      <div className="container-page grid gap-12 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8 mb-12">
        
        <div className="lg:col-span-1">
          <a href="#inicio" className="flex items-center gap-2 mb-4" aria-label="Norte Firme inicio">
            <span className="flex h-8 w-8 items-center justify-center rounded bg-electric text-navy">
              <Zap size={18} strokeWidth={2.5} />
            </span>
            <span className="font-bold text-lg tracking-tight text-white">
              Norte Firme
            </span>
          </a>
          <p className="text-sm text-mist/70 leading-relaxed mb-2">
            Norte Firme Infraestructura y Construcción
          </p>
          <p className="text-sm font-semibold text-mist/90">
            Servicios eléctricos de media y baja tensión
          </p>
        </div>

        <div>
          <h4 className="font-bold text-white mb-4 uppercase tracking-wider text-xs">Navegación</h4>
          <ul className="grid gap-3 text-sm text-mist/70">
            <li><a href="#inicio" className="hover:text-electric transition-colors">Inicio</a></li>
            <li><a href="#servicios" className="hover:text-electric transition-colors">Servicios</a></li>
            <li><a href="#sectores" className="hover:text-electric transition-colors">Sectores</a></li>
            <li><a href="#proyectos" className="hover:text-electric transition-colors">Proyectos</a></li>
            <li><a href="#contacto" className="hover:text-electric transition-colors">Contacto</a></li>
          </ul>
        </div>

        <div>
          <h4 className="font-bold text-white mb-4 uppercase tracking-wider text-xs">Contacto</h4>
          <ul className="grid gap-3 text-sm text-mist/70">
            <li>Chihuahua, México</li>
            <li>
              <a href="mailto:contacto@nortefirme.com.mx" className="hover:text-electric transition-colors">
                contacto@nortefirme.com.mx
              </a>
            </li>
            <li>
              <a href="tel:614177711" className="hover:text-electric transition-colors">
                614 177 711
              </a>
            </li>
          </ul>
        </div>

      </div>
      
      <div className="container-page pt-8 border-t border-white/10 text-center lg:text-left">
        <p className="text-xs text-mist/50">
          © 2026 Norte Firme Infraestructura y Construcción. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  )
}
