import { Cloud } from 'lucide-react';

interface NavigationProps {
  onLogoClick?: () => void;
  onNavigate?: (view: 'dashboard' | 'landing') => void;
  showNav?: boolean;
}

export function Navigation({ onLogoClick, onNavigate, showNav = true }: NavigationProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-ink-800/60">
      <nav className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <button
          onClick={onLogoClick}
          className="flex items-center gap-2.5 group"
        >
          <div className="relative">
            <div className="absolute inset-0 bg-white/20 blur-lg group-hover:bg-white/30 transition-all duration-300" />
            <div className="relative w-9 h-9 rounded-xl bg-gradient-to-br from-ink-100 to-ink-300 flex items-center justify-center">
              <Cloud className="w-5 h-5 text-ink-950" strokeWidth={2.5} />
            </div>
          </div>
          <div className="flex flex-col items-start leading-none">
            <span className="text-sm font-semibold text-white tracking-tight">Shaheen</span>
            <span className="text-[10px] text-ink-400 font-medium tracking-widest uppercase">Global Cloud</span>
          </div>
        </button>

        {showNav && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate?.('landing')}
              className="btn-ghost"
            >
              Home
            </button>
            <button
              onClick={() => onNavigate?.('dashboard')}
              className="btn-ghost"
            >
              Dashboard
            </button>
            <button
              onClick={() => onNavigate?.('dashboard')}
              className="btn-primary"
            >
              Launch Console
            </button>
          </div>
        )}
      </nav>
    </header>
  );
}
