import AnimatedSection from './AnimatedSection.jsx'
import { MessageCircle, Mail } from 'lucide-react'

export default function CTA() {
  return (
    <section className="section-padding bg-navy text-white text-center">
      <div className="container-page">
        <AnimatedSection className="max-w-3xl mx-auto">
          <h2 className="section-title text-white mx-auto">
            ¿Tienes un proyecto eléctrico en puerta?
          </h2>
          <p className="mt-6 text-xl text-mist leading-relaxed mx-auto">
            Cuéntanos qué necesitas construir, instalar, corregir o mantener. Revisamos tu caso y te damos una propuesta clara.
          </p>
          
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <a 
              href="https://wa.me/52614177711?text=Hola%20Norte%20Firme,%20quiero%20solicitar%20una%20cotizaci%C3%B3n%20para%20un%20proyecto%20el%C3%A9ctrico." 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn-primary w-full sm:w-auto"
            >
              <MessageCircle size={20} />
              Solicitar cotización por WhatsApp
            </a>
            
            <a 
              href="mailto:contacto@nortefirme.com.mx" 
              className="btn-secondary-white w-full sm:w-auto"
            >
              <Mail size={20} />
              Enviar correo
            </a>
          </div>
        </AnimatedSection>
      </div>
    </section>
  )
}
