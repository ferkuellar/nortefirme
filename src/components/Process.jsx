import { processSteps } from '../data/processSteps.js'
import AnimatedSection from './AnimatedSection.jsx'

export default function Process() {
  return (
    <section id="proceso" className="section-padding bg-navy text-white overflow-hidden">
      <div className="container-page">
        <AnimatedSection className="mb-16">
          <h2 className="section-title text-white">Un proceso claro para evitar improvisaciones</h2>
        </AnimatedSection>

        <div className="relative mt-12">
          {/* Horizontal line for desktop */}
          <div className="hidden lg:block absolute top-[28px] left-0 w-full h-[2px] bg-white/10" />
          
          {/* Vertical line for mobile */}
          <div className="lg:hidden absolute top-0 bottom-0 left-[28px] w-[2px] bg-white/10" />

          <div className="grid gap-10 lg:grid-cols-6 lg:gap-6 relative z-10">
            {processSteps.map((step, index) => (
              <AnimatedSection 
                key={step.step} 
                delay={index * 0.1}
                className="relative flex flex-col pl-16 lg:pl-0"
              >
                {/* Node */}
                <div className="absolute left-0 lg:static flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-steel border-4 border-navy text-white font-bold text-lg mb-6 shadow-sm z-10">
                  {step.step}
                </div>
                
                <h3 className="font-bold text-white mb-3">{step.title}</h3>
                <p className="text-sm text-mist/80 leading-relaxed">{step.description}</p>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
