import { ClipboardCheck, FileCheck2, Gauge, ShieldCheck } from 'lucide-react'

const evidenceImage =
  'https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=1100&q=82'

const controls = [
  { label: 'Levantamiento técnico', icon: ClipboardCheck },
  { label: 'Ejecución documentada', icon: FileCheck2 },
  { label: 'Revisión de cargas', icon: Gauge },
  { label: 'Seguridad eléctrica', icon: ShieldCheck },
]

export default function HeroEvidencePanel() {
  return (
    <aside className="overflow-hidden rounded-lg border border-white/14 bg-white/[0.07] shadow-2xl shadow-slate-950/20 backdrop-blur-md">
      <div className="relative h-72 overflow-hidden">
        <img src={evidenceImage} alt="" className="h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/35 to-transparent" />
        <div className="absolute inset-0 technical-grid opacity-35" />
        <div className="absolute left-5 top-5 rounded-md bg-electric px-3 py-2 text-xs font-extrabold uppercase tracking-[0.14em] text-navy">
          Obra eléctrica MT/BT
        </div>
        <div className="absolute bottom-5 left-5 right-5">
          <p className="text-sm font-bold uppercase tracking-[0.16em] text-electric">Control técnico en campo</p>
          <h2 className="mt-2 text-2xl font-extrabold leading-tight text-white">
            Instalaciones ordenadas, revisables y listas para operación.
          </h2>
        </div>
      </div>

      <div className="grid gap-4 p-5">
        <div className="grid gap-3 sm:grid-cols-2">
          {controls.map((item) => {
            const Icon = item.icon
            return (
              <div key={item.label} className="flex items-center gap-3 rounded-md border border-white/10 bg-navy/60 p-3">
                <Icon className="shrink-0 text-electric" size={20} />
                <span className="text-sm font-bold leading-5 text-slate-100">{item.label}</span>
              </div>
            )
          })}
        </div>

        <div className="grid grid-cols-3 gap-3 border-t border-white/10 pt-4">
          <div>
            <p className="text-2xl font-extrabold text-white">MT/BT</p>
            <p className="mt-1 text-xs font-bold uppercase tracking-[0.12em] text-slate-400">Tensión</p>
          </div>
          <div>
            <p className="text-2xl font-extrabold text-white">24 h</p>
            <p className="mt-1 text-xs font-bold uppercase tracking-[0.12em] text-slate-400">Respuesta</p>
          </div>
          <div>
            <p className="text-2xl font-extrabold text-white">Obra</p>
            <p className="mt-1 text-xs font-bold uppercase tracking-[0.12em] text-slate-400">Campo</p>
          </div>
        </div>
      </div>
    </aside>
  )
}
