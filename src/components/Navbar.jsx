import { useState, useEffect } from 'react'
import { Menu, X, Zap } from 'lucide-react'

const navItems = [
  { label: 'Inicio', href: '#inicio' },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Sectores', href: '#sectores' },
  { label: 'Proceso', href: '#proceso' },
  { label: 'Proyectos', href: '#proyectos' },
  { label: 'Contacto', href: '#contacto' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header 
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-navy/95 backdrop-blur-md shadow-md py-3' : 'bg-transparent py-5'
      }`}
    >
      <nav className="container-page flex items-center justify-between">
        <a href="#inicio" className="flex items-center gap-2" aria-label="Norte Firme inicio">
          <span className="flex h-10 w-10 items-center justify-center rounded bg-electric text-navy">
            <Zap size={22} strokeWidth={2.5} />
          </span>
          <span className={`font-bold text-xl tracking-tight transition-colors ${scrolled ? 'text-white' : 'text-white'}`}>
            Norte Firme
          </span>
        </a>

        <div className="hidden items-center gap-8 lg:flex">
          {navItems.map((item) => (
            <a 
              key={item.href} 
              href={item.href} 
              className="text-sm font-semibold text-white/90 transition-colors hover:text-electric"
            >
              {item.label}
            </a>
          ))}
        </div>

        <div className="hidden lg:block">
          <a href="#contacto" className="btn-primary">
            Solicitar cotización
          </a>
        </div>

        <button
          type="button"
          className="inline-flex h-10 w-10 items-center justify-center rounded text-white lg:hidden"
          aria-label={open ? 'Cerrar menú' : 'Abrir menú'}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X size={24} /> : <Menu size={24} />}
        </button>
      </nav>

      {/* Mobile menu */}
      {open && (
        <div className="absolute top-full inset-x-0 border-t border-white/10 bg-navy shadow-lg lg:hidden">
          <div className="container-page grid gap-2 py-4">
            {navItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="rounded px-3 py-3 text-sm font-semibold text-white transition-colors hover:bg-white/5"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </a>
            ))}
            <div className="pt-2 pb-1">
              <a
                href="#contacto"
                className="flex w-full items-center justify-center rounded bg-electric px-4 py-3 text-sm font-bold text-navy"
                onClick={() => setOpen(false)}
              >
                Solicitar cotización
              </a>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
