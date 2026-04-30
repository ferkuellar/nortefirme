import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import TrustBar from './components/TrustBar.jsx'
import ProblemSection from './components/ProblemSection.jsx'
import Services from './components/Services.jsx'
import Sectors from './components/Sectors.jsx'
import Process from './components/Process.jsx'
import Projects from './components/Projects.jsx'
import SafetyCompliance from './components/SafetyCompliance.jsx'
import Differentiators from './components/Differentiators.jsx'
import CTA from './components/CTA.jsx'
import ContactForm from './components/ContactForm.jsx'
import Footer from './components/Footer.jsx'
import AdminPortfolio from './components/admin/AdminPortfolio.jsx'

export default function App() {
  if (window.location.pathname.startsWith('/admin')) {
    return <AdminPortfolio />
  }

  return (
    <div className="min-h-screen bg-white text-carbon font-sans selection:bg-electric selection:text-navy">
      <Navbar />
      <main>
        <Hero />
        <TrustBar />
        <ProblemSection />
        <Services />
        <Sectors />
        <Process />
        <Projects />
        <SafetyCompliance />
        <Differentiators />
        <CTA />
        <ContactForm />
      </main>
      <Footer />
    </div>
  )
}
