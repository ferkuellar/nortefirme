import AnimatedSection from './AnimatedSection.jsx'

export default function ServiceCard({ service, index }) {
  const Icon = service.icon

  return (
    <AnimatedSection
      as="article"
      delay={(index % 3) * 0.1}
      className="group relative flex flex-col bg-white p-6 rounded border border-gray/20 shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 overflow-hidden"
    >
      {/* Yellow top line on hover */}
      <div className="absolute top-0 inset-x-0 h-1 bg-electric scale-x-0 origin-left transition-transform duration-300 group-hover:scale-x-100" />
      
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded bg-navy text-white mb-5">
        <Icon size={24} />
      </div>
      
      <h3 className="text-lg font-bold text-navy mb-2">{service.title}</h3>
      <p className="text-sm text-gray leading-relaxed flex-grow">{service.description}</p>
    </AnimatedSection>
  )
}
