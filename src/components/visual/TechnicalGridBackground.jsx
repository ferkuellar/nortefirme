export default function TechnicalGridBackground({ className = '' }) {
  return (
    <div className={`pointer-events-none absolute inset-0 overflow-hidden ${className}`} aria-hidden="true">
      <div className="absolute inset-0 technical-grid" />
      <svg className="absolute inset-0 h-full w-full opacity-35" viewBox="0 0 1200 700" preserveAspectRatio="none">
        <path d="M80 170H330V120H520V210H750" className="blueprint-line" />
        <path d="M140 520H420V455H680V500H1050" className="blueprint-line" />
        <path d="M900 120V300H1080V410" className="blueprint-line" />
        <circle cx="330" cy="170" r="5" className="blueprint-node" />
        <circle cx="520" cy="120" r="5" className="blueprint-node" />
        <circle cx="680" cy="455" r="5" className="blueprint-node" />
        <circle cx="900" cy="300" r="5" className="blueprint-node" />
        <path d="M82 610H180M82 610V575M260 95H360M260 95V130M1030 250H1120M1120 250V285" className="blueprint-mark" />
      </svg>
    </div>
  )
}
