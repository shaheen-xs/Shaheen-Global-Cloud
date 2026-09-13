import { useState, useEffect } from 'react';
import {
  Cloud, Server, Shield, Zap, Globe, ArrowRight, Check, Activity,
  Cpu, HardDrive, MemoryStick, Network, Lock, Terminal,
} from 'lucide-react';
import { Navigation } from './Navigation';

interface LandingPageProps {
  onEnter: () => void;
}

export function LandingPage({ onEnter }: LandingPageProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 100);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="min-h-screen bg-ink-950">
      <Navigation
        onLogoClick={onEnter}
        onNavigate={(v) => v === 'dashboard' && onEnter()}
      />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
        {/* Animated background grid */}
        <div className="absolute inset-0 bg-gradient-mesh" />
        <div
          className="absolute inset-0 opacity-[0.15]"
          style={{
            backgroundImage: `
              linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
            maskImage: 'radial-gradient(ellipse 80% 60% at 50% 40%, black 40%, transparent 100%)',
            WebkitMaskImage: 'radial-gradient(ellipse 80% 60% at 50% 40%, black 40%, transparent 100%)',
          }}
        />

        {/* Floating orbs */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-white/[0.03] rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-white/[0.02] rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />

        {/* Hero content */}
        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
          <div
            className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass mb-8 transition-all duration-700 ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <span className="status-dot bg-emerald-400 animate-pulse-soft" />
            <span className="text-xs font-medium text-ink-300 tracking-wide">Infrastructure Platform · Phase 1 MVP</span>
          </div>

          <h1
            className={`text-5xl sm:text-6xl md:text-7xl font-bold tracking-tight mb-6 transition-all duration-700 delay-100 ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
            }`}
          >
            <span className="gradient-text">Deploy and manage</span>
            <br />
            <span className="gradient-text">cloud infrastructure</span>
            <br />
            <span className="text-ink-500 text-3xl sm:text-4xl md:text-5xl font-light italic">with elegance.</span>
          </h1>

          <p
            className={`text-lg md:text-xl text-ink-400 max-w-2xl mx-auto mb-10 leading-relaxed transition-all duration-700 delay-200 ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
            }`}
          >
            Shaheen Global Cloud provides a unified control plane for provisioning,
            monitoring, and scaling virtual machines — powered by Dagger and OpenTofu.
          </p>

          <div
            className={`flex flex-col sm:flex-row items-center justify-center gap-4 transition-all duration-700 delay-300 ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
            }`}
          >
            <button onClick={onEnter} className="btn-primary group flex items-center gap-2 px-7 py-3.5 text-base">
              Enter Console
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="btn-secondary flex items-center gap-2 px-7 py-3.5 text-base">
              <Terminal className="w-4 h-4" />
              View Documentation
            </button>
          </div>

          {/* Stats strip */}
          <div
            className={`mt-20 grid grid-cols-3 gap-8 max-w-2xl mx-auto transition-all duration-700 delay-500 ${
              mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
            }`}
          >
            {[
              { value: '99.99%', label: 'Uptime SLA' },
              { value: '< 2s', label: 'Provision Time' },
              { value: '5', label: 'Regions' },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-2xl md:text-3xl font-bold gradient-text">{stat.value}</div>
                <div className="text-xs text-ink-500 mt-1 tracking-wide uppercase">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2">
          <div className="w-6 h-10 rounded-full border-2 border-ink-700 flex items-start justify-center p-1.5">
            <div className="w-1 h-2 rounded-full bg-ink-500 animate-bounce" />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative py-32 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-3xl md:text-4xl font-bold gradient-text mb-4">
              Built for production workloads
            </h2>
            <p className="text-ink-400 max-w-2xl mx-auto">
              Every component is designed for reliability, observability, and scale.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: Server, title: 'Server Management', desc: 'Create, start, stop, and destroy virtual machines with a single click. Full lifecycle control at your fingertips.' },
              { icon: Zap, title: 'Fast Provisioning', desc: 'Dagger-powered pipelines provision infrastructure in seconds, not minutes. Async job queue keeps the UI responsive.' },
              { icon: Shield, title: 'Secure by Design', desc: 'Row-level security, API key authentication, and encrypted connections. Your infrastructure is protected.' },
              { icon: Globe, title: 'Multi-Region', desc: 'Deploy across five global regions. Low latency, high availability, and geographic redundancy.' },
              { icon: Activity, title: 'Real-time Monitoring', desc: 'Track server health, job status, and resource utilization with live updates and detailed metrics.' },
              { icon: Lock, title: 'OpenTofu Powered', desc: 'Infrastructure as code with OpenTofu. Reproducible, version-controlled, and auditable deployments.' },
            ].map((feature, i) => (
              <div
                key={feature.title}
                className="glass-card-hover p-6 group cursor-default"
                style={{ animationDelay: `${i * 50}ms` }}
              >
                <div className="w-12 h-12 rounded-xl bg-ink-800/60 flex items-center justify-center mb-4 group-hover:bg-ink-700/60 transition-colors duration-300">
                  <feature.icon className="w-6 h-6 text-ink-200" strokeWidth={1.5} />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-ink-400 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Architecture Section */}
      <section className="relative py-32 px-6 border-t border-ink-900">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-3xl md:text-4xl font-bold gradient-text mb-4">
              The pipeline
            </h2>
            <p className="text-ink-400 max-w-2xl mx-auto">
              From your browser to a running server — a transparent, observable flow.
            </p>
          </div>

          <div className="flex flex-col md:flex-row items-stretch gap-3">
            {[
              { icon: Cloud, label: 'Frontend', sub: 'React + Vite' },
              { icon: Server, label: 'FastAPI', sub: 'Python backend' },
              { icon: Activity, label: 'Redis Queue', sub: 'Job dispatch' },
              { icon: Cpu, label: 'Worker', sub: 'Async processor' },
              { icon: Terminal, label: 'Dagger', sub: 'CI engine' },
              { icon: HardDrive, label: 'OpenTofu', sub: 'IaC' },
              { icon: Network, label: 'Mock Provider', sub: 'Phase 1' },
            ].map((step, i, arr) => (
              <div key={step.label} className="flex items-center gap-3 flex-1">
                <div className="glass-card p-4 flex-1 text-center group hover:border-ink-700 transition-all duration-300">
                  <step.icon className="w-6 h-6 mx-auto mb-2 text-ink-200" strokeWidth={1.5} />
                  <div className="text-sm font-semibold text-white">{step.label}</div>
                  <div className="text-xs text-ink-500 mt-0.5">{step.sub}</div>
                </div>
                {i < arr.length - 1 && (
                  <ArrowRight className="w-4 h-4 text-ink-700 hidden md:block shrink-0" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-32 px-6 border-t border-ink-900">
        <div className="max-w-3xl mx-auto text-center">
          <div className="glass-card p-12 gradient-border">
            <h2 className="text-3xl md:text-4xl font-bold gradient-text mb-4">
              Ready to deploy?
            </h2>
            <p className="text-ink-400 mb-8 max-w-xl mx-auto">
              Launch your first server in under a minute. No credit card required for Phase 1.
            </p>
            <button onClick={onEnter} className="btn-primary group inline-flex items-center gap-2 px-8 py-4 text-base">
              Open Cloud Console
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-ink-900 py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-ink-100 to-ink-300 flex items-center justify-center">
              <Cloud className="w-4 h-4 text-ink-950" strokeWidth={2.5} />
            </div>
            <div className="flex flex-col leading-none">
              <span className="text-sm font-semibold text-white">Shaheen Global Cloud</span>
              <span className="text-[10px] text-ink-500">Phase 1 · MVP</span>
            </div>
          </div>
          <div className="flex items-center gap-6 text-xs text-ink-500">
            <span className="flex items-center gap-1.5"><Check className="w-3 h-3 text-emerald-400" /> OpenTofu</span>
            <span className="flex items-center gap-1.5"><Check className="w-3 h-3 text-emerald-400" /> Dagger</span>
            <span className="flex items-center gap-1.5"><Check className="w-3 h-3 text-emerald-400" /> FastAPI</span>
            <span className="flex items-center gap-1.5"><Check className="w-3 h-3 text-emerald-400" /> Redis</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
