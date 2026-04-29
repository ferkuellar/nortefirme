import { useState } from 'react'
import { Menu, Phone, X, Zap } from 'lucide-react'
import { navItems } from '../data/content.js'

export default function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-navy/95 text-white shadow-xl shadow-slate-950/10 backdrop-blur">
      <nav className="container-page flex h-20 items-center justify-between">
        <a href="#inicio" className="flex items-center gap-3" aria-label="Norte Firme inicio">
          <span className="flex h-11 w-11 items-center justify-center rounded-md bg-electric text-navy">
            <Zap size={24} strokeWidth={2.7} />
          </span>
          <span>
            <span className="block font-sans text-lg font-extrabold leading-tight">Norte Firme</span>
            <span className="hidden text-xs font-semibold uppercase tracking-[0.18em] text-slate-300 sm:block">
              Infraestructura eléctrica
            </span>
          </span>
        </a>

        <div className="hidden items-center gap-7 lg:flex">
          {navItems.map((item) => (
            <a key={item.href} href={item.href} className="text-sm font-semibold text-slate-200 transition hover:text-electric">
              {item.label}
            </a>
          ))}
        </div>

        <a href="#contacto" className="hidden rounded-md bg-electric px-4 py-3 text-sm font-extrabold text-navy transition hover:bg-amber-400 lg:inline-flex">
          Solicitar cotización
        </a>

        <button
          type="button"
          className="inline-flex h-11 w-11 items-center justify-center rounded-md border border-white/20 lg:hidden"
          aria-label={open ? 'Cerrar menú' : 'Abrir menú'}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>

      {open && (
        <div className="border-t border-white/10 bg-navy lg:hidden">
          <div className="container-page grid gap-1 py-4">
            {navItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="rounded-md px-2 py-3 text-sm font-semibold text-slate-100"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </a>
            ))}
            <a
              href="tel:614177711"
              className="mt-3 inline-flex items-center justify-center gap-2 rounded-md bg-electric px-4 py-3 text-sm font-extrabold text-navy"
              onClick={() => setOpen(false)}
            >
              <Phone size={18} />
              Solicitar cotización
            </a>
          </div>
        </div>
      )}
    </header>
  )
}
