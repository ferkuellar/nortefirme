import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import TrustSection from './components/TrustSection.jsx'
import Services from './components/Services.jsx'
import Sectors from './components/Sectors.jsx'
import Differentiators from './components/Differentiators.jsx'
import Process from './components/Process.jsx'
import Projects from './components/Projects.jsx'
import SafetyCompliance from './components/SafetyCompliance.jsx'
import CTA from './components/CTA.jsx'
import ContactForm from './components/ContactForm.jsx'
import Footer from './components/Footer.jsx'
import AdminPortfolio from './components/admin/AdminPortfolio.jsx'

export default function App() {
  if (window.location.pathname.startsWith('/admin')) {
    return <AdminPortfolio />
  }

  return (
    <div className="min-h-screen bg-white text-carbon">
      <Navbar />
      <main>
        <Hero />
        <TrustSection />
        <Services />
        <Sectors />
        <Differentiators />
        <Process />
        <Projects />
        <SafetyCompliance />
        <CTA />
        <ContactForm />
      </main>
      <Footer />
    </div>
  )
}
