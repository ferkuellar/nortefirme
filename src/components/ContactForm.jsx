import { useState } from 'react'
import AnimatedSection from './AnimatedSection.jsx'

export default function ContactForm() {
  const [status, setStatus] = useState('idle')

  const handleSubmit = (e) => {
    e.preventDefault()
    setStatus('submitting')
    // Simulate form submission
    setTimeout(() => {
      setStatus('success')
    }, 1000)
  }

  return (
    <section id="contacto" className="section-padding bg-mist">
      <div className="container-page max-w-4xl">
        <AnimatedSection className="text-center mb-10">
          <h2 className="section-title text-navy mx-auto">Contacto</h2>
          <p className="mt-4 text-gray text-lg">
            Respondemos con enfoque técnico, no con respuestas genéricas.
          </p>
        </AnimatedSection>

        <AnimatedSection as="div" className="bg-white p-8 sm:p-10 rounded border border-gray/20 shadow-sm">
          {status === 'success' ? (
            <div className="text-center py-10">
              <h3 className="text-2xl font-bold text-navy mb-3">Mensaje enviado</h3>
              <p className="text-gray">Hemos recibido tu información. Un ingeniero se pondrá en contacto pronto.</p>
              <button 
                onClick={() => setStatus('idle')}
                className="mt-6 btn-secondary"
              >
                Enviar otro mensaje
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="grid gap-6 sm:grid-cols-2">
              <div className="flex flex-col gap-2">
                <label htmlFor="nombre" className="text-sm font-bold text-navy">Nombre *</label>
                <input 
                  type="text" 
                  id="nombre" 
                  required 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric" 
                />
              </div>
              
              <div className="flex flex-col gap-2">
                <label htmlFor="empresa" className="text-sm font-bold text-navy">Empresa *</label>
                <input 
                  type="text" 
                  id="empresa" 
                  required 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric" 
                />
              </div>
              
              <div className="flex flex-col gap-2">
                <label htmlFor="telefono" className="text-sm font-bold text-navy">Teléfono *</label>
                <input 
                  type="tel" 
                  id="telefono" 
                  required 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric" 
                />
              </div>
              
              <div className="flex flex-col gap-2">
                <label htmlFor="correo" className="text-sm font-bold text-navy">Correo *</label>
                <input 
                  type="email" 
                  id="correo" 
                  required 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric" 
                />
              </div>
              
              <div className="flex flex-col gap-2">
                <label htmlFor="proyecto" className="text-sm font-bold text-navy">Tipo de proyecto</label>
                <select 
                  id="proyecto" 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric"
                >
                  <option value="">Selecciona una opción</option>
                  <option value="nueva-instalacion">Nueva instalación</option>
                  <option value="mantenimiento">Mantenimiento</option>
                  <option value="adecuacion">Adecuación / Remodelación</option>
                  <option value="otro">Otro</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label htmlFor="ciudad" className="text-sm font-bold text-navy">Ciudad</label>
                <input 
                  type="text" 
                  id="ciudad" 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric" 
                />
              </div>
              
              <div className="sm:col-span-2 flex flex-col gap-2">
                <label htmlFor="mensaje" className="text-sm font-bold text-navy">Mensaje</label>
                <textarea 
                  id="mensaje" 
                  rows={4} 
                  className="rounded border border-gray/30 bg-white px-4 py-3 text-sm focus:border-electric focus:outline-none focus:ring-1 focus:ring-electric" 
                ></textarea>
              </div>
              
              <div className="sm:col-span-2 mt-2">
                <button 
                  type="submit" 
                  disabled={status === 'submitting'}
                  className="btn-primary w-full sm:w-auto"
                >
                  {status === 'submitting' ? 'Enviando...' : 'Enviar solicitud'}
                </button>
              </div>
            </form>
          )}
        </AnimatedSection>
      </div>
    </section>
  )
}
