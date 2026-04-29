import { motion } from 'framer-motion'

export default function SectionHeader({ eyebrow, title, copy, align = 'left', className = '' }) {
  const alignment = align === 'center' ? 'mx-auto text-center' : ''

  return (
    <motion.div
      className={`${alignment} ${className}`}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.55, ease: 'easeOut' }}
    >
      {eyebrow && <p className="eyebrow">{eyebrow}</p>}
      <h2 className={`section-title ${alignment}`}>{title}</h2>
      {copy && <p className={`section-copy ${alignment}`}>{copy}</p>}
    </motion.div>
  )
}
