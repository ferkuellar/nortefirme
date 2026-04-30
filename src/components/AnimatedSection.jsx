import { motion } from 'framer-motion'
import usePrefersReducedMotion from '../hooks/usePrefersReducedMotion.js'

export default function AnimatedSection({ 
  children, 
  className = '', 
  delay = 0, 
  as = 'div',
  staggerChildren = false
}) {
  const reducedMotion = usePrefersReducedMotion()
  const Component = motion[as] || motion.div

  const variants = staggerChildren 
    ? {
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
          transition: {
            staggerChildren: 0.08,
            delayChildren: delay
          }
        }
      }
    : {
        hidden: { opacity: 0, y: 24 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.6, delay, ease: 'easeOut' } }
      }

  if (reducedMotion) {
    return <Component className={className}>{children}</Component>
  }

  return (
    <Component
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: '-50px' }}
      variants={variants}
    >
      {children}
    </Component>
  )
}
