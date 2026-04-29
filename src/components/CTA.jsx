import { Mail, MessageCircle } from 'lucide-react'

export default function CTA() {
  return (
    <section className="bg-steel py-14 text-white">
      <div className="container-page grid gap-8 lg:grid-cols-[1fr_auto] lg:items-center">
        <div>
          <p className="eyebrow text-electric">Cotización</p>
          <h2 className="mt-3 text-3xl font-extrabold leading-tight sm:text-4xl">¿Tienes un proyecto eléctrico en puerta?</h2>
          <p className="mt-4 max-w-3xl text-lg leading-8 text-blue-50">
            Cuéntanos qué necesitas construir, instalar, corregir o mantener. Revisamos tu caso y te damos una propuesta clara.
          </p>
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
    </section>
  )
}
