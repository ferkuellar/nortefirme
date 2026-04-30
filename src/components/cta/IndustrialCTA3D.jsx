import { Mail, MessageCircle, Phone, ShieldCheck } from 'lucide-react'
import TechnicalGridBackground from '../visual/TechnicalGridBackground.jsx'

export default function IndustrialCTA3D() {
  return (
    <section className="relative overflow-hidden bg-navy py-16 text-white">
      <TechnicalGridBackground className="opacity-35" />
      <div className="container-page relative">
        <div className="grid gap-8 rounded-lg border border-white/10 bg-white/8 p-6 shadow-[0_24px_80px_rgba(0,0,0,0.22)] backdrop-blur-md lg:grid-cols-[1fr_auto] lg:items-center lg:p-8">
          <div>
            <p className="eyebrow text-electric">Cotización</p>
            <h2 className="mt-3 text-3xl font-extrabold leading-tight sm:text-4xl">¿Tienes un proyecto eléctrico en puerta?</h2>
            <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-200">
              Cuéntanos qué necesitas construir, instalar, corregir o mantener. Revisamos tu caso y te damos una propuesta clara.
            </p>
            <div className="mt-6 flex flex-wrap gap-4 text-sm font-bold text-slate-200">
              <span className="inline-flex items-center gap-2">
                <Phone size={18} className="text-electric" />
                614 177 711
              </span>
              <span className="inline-flex items-center gap-2">
                <Mail size={18} className="text-electric" />
                contacto@nortefirme.com.mx
              </span>
              <span className="inline-flex items-center gap-2">
                <ShieldCheck size={18} className="text-electric" />
                Respuesta técnica
              </span>
            </div>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row lg:flex-col xl:flex-row">
            <a href="https://wa.me/52614177711" className="btn-primary">
              <MessageCircle size={19} />
              Solicitar cotización por WhatsApp
            </a>
            <a href="mailto:contacto@nortefirme.com.mx" className="btn-secondary">
              <Mail size={19} />
              Enviar correo
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
