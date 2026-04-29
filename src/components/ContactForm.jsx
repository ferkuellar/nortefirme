import { Send } from 'lucide-react'
import SectionHeader from './SectionHeader.jsx'

const inputClass =
  'w-full rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-carbon outline-none transition placeholder:text-slate-400 focus:border-steel focus:ring-4 focus:ring-steel/10'

export default function ContactForm() {
  return (
    <section id="contacto" className="section-padding bg-white">
      <div className="container-page grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">
        <div>
          <SectionHeader
            eyebrow="Contacto"
            title="Solicita una revisión técnica"
            copy="Respondemos con enfoque técnico, no con respuestas genéricas."
          />
          <div className="mt-8 rounded-lg bg-navy p-6 text-white">
            <p className="text-sm font-bold uppercase tracking-[0.18em] text-electric">Datos directos</p>
            <a href="tel:614177711" className="mt-4 block text-3xl font-extrabold">614 177 711</a>
            <a href="mailto:contacto@nortefirme.com.mx" className="mt-3 block font-semibold text-slate-200">
              contacto@nortefirme.com.mx
            </a>
            <p className="mt-3 font-semibold text-slate-300">Chihuahua, México</p>
          </div>
        </div>

        <form className="rounded-lg border border-slate-200 bg-mist p-5 shadow-sm sm:p-7">
          <div className="grid gap-5 sm:grid-cols-2">
            <label className="grid gap-2 text-sm font-bold text-navy">
              Nombre
              <input className={inputClass} type="text" name="nombre" autoComplete="name" placeholder="Nombre completo" />
            </label>
            <label className="grid gap-2 text-sm font-bold text-navy">
              Empresa
              <input className={inputClass} type="text" name="empresa" autoComplete="organization" placeholder="Empresa o proyecto" />
            </label>
            <label className="grid gap-2 text-sm font-bold text-navy">
              Teléfono
              <input className={inputClass} type="tel" name="telefono" autoComplete="tel" placeholder="Teléfono de contacto" />
            </label>
            <label className="grid gap-2 text-sm font-bold text-navy">
              Correo
              <input className={inputClass} type="email" name="correo" autoComplete="email" placeholder="correo@empresa.com" />
            </label>
            <label className="grid gap-2 text-sm font-bold text-navy">
              Tipo de proyecto
              <select className={inputClass} name="tipoProyecto" defaultValue="">
                <option value="" disabled>Seleccionar</option>
                <option>Media tensión</option>
                <option>Baja tensión</option>
                <option>Subestación o transformador</option>
                <option>Mantenimiento eléctrico</option>
                <option>Obra eléctrica en construcción</option>
              </select>
            </label>
            <label className="grid gap-2 text-sm font-bold text-navy">
              Ciudad
              <input className={inputClass} type="text" name="ciudad" autoComplete="address-level2" placeholder="Ciudad del proyecto" />
            </label>
            <label className="grid gap-2 text-sm font-bold text-navy sm:col-span-2">
              Mensaje
              <textarea className={`${inputClass} min-h-36 resize-y`} name="mensaje" placeholder="Describe el alcance, etapa de obra o requerimiento eléctrico." />
            </label>
          </div>
          <button type="submit" className="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-md bg-navy px-5 py-4 text-sm font-extrabold text-white transition hover:bg-steel sm:w-auto">
            <Send size={18} />
            Enviar solicitud
          </button>
        </form>
      </div>
    </section>
  )
}
