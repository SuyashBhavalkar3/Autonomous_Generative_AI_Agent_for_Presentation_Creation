import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { 
  Presentation, 
  ArrowRight, 
  Sparkles, 
  Zap, 
  Download,
  CheckCircle2,
  Play
} from 'lucide-react';

export default function Index() {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Magic',
      description: 'Our advanced AI understands context and creates compelling, structured content automatically.',
    },
    {
      icon: Zap,
      title: 'Instant Generation',
      description: 'Generate complete, polished presentations in under 30 seconds.',
    },
    {
      icon: Download,
      title: 'One-Click Export',
      description: 'Download your presentation in PowerPoint format, ready to present.',
    },
  ];

  return (
    <div className="min-h-screen bg-background overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass">
        <div className="container mx-auto px-4 sm:px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 gradient-primary rounded-xl blur-lg opacity-50"></div>
              <div className="relative p-2.5 rounded-xl gradient-primary shadow-glow">
                <Presentation className="h-6 w-6 text-primary-foreground" />
              </div>
            </div>
            <span className="text-xl font-display font-bold text-foreground">SlideCraft</span>
          </div>
          
          <div className="flex items-center gap-3">
            <Button variant="ghost" asChild className="hidden sm:inline-flex">
              <Link to="/login">Sign in</Link>
            </Button>
            <Button variant="gradient" asChild>
              <Link to="/register">
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </nav>
      
      {/* Hero Section */}
      <section className="relative pt-32 pb-24 lg:pt-44 lg:pb-36 overflow-hidden">
        {/* Background mesh gradient */}
        <div className="absolute inset-0 gradient-mesh opacity-70"></div>
        
        {/* Animated orbs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-32 -right-32 w-[500px] h-[500px] rounded-full gradient-primary opacity-10 blur-3xl animate-float"></div>
          <div className="absolute top-1/2 -left-48 w-[400px] h-[400px] rounded-full bg-accent opacity-8 blur-3xl animate-float-delayed"></div>
          <div className="absolute -bottom-32 right-1/4 w-[350px] h-[350px] rounded-full gradient-primary opacity-8 blur-3xl animate-pulse-glow"></div>
        </div>
        
        {/* Grid pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(hsl(var(--foreground)/0.02)_1px,transparent_1px),linear-gradient(90deg,hsl(var(--foreground)/0.02)_1px,transparent_1px)] bg-[size:64px_64px]"></div>
        
        <div className="container mx-auto px-4 sm:px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full glass border border-primary/20 text-sm font-medium mb-8 animate-fade-in shadow-lg">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 gradient-primary"></span>
              </span>
              <span className="text-foreground">Powered by Advanced AI</span>
            </div>
            
            {/* Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-display font-bold text-foreground mb-6 leading-[1.1] animate-slide-up">
              Create Stunning{' '}
              <br className="hidden sm:block" />
              <span className="text-gradient">Presentations</span>
              {' '}in Seconds
            </h1>
            
            <p className="text-lg lg:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 animate-slide-up leading-relaxed" style={{ animationDelay: '100ms' }}>
              Transform your ideas into professional PowerPoint presentations with the power of AI. 
              Just describe your topic and watch the magic happen.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '200ms' }}>
              <Button variant="hero" size="xl" asChild className="w-full sm:w-auto">
                <Link to="/register">
                  Start Creating Free
                  <ArrowRight className="h-5 w-5" />
                </Link>
              </Button>
              <Button variant="glass" size="xl" asChild className="w-full sm:w-auto">
                <Link to="/login">
                  <Play className="h-4 w-4" />
                  Watch Demo
                </Link>
              </Button>
            </div>
            
            {/* Trust indicators */}
            <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-3 mt-12 text-sm text-muted-foreground animate-fade-in" style={{ animationDelay: '400ms' }}>
              {['No credit card required', 'Free to start', 'Export to PowerPoint'].map((text, i) => (
                <div key={i} className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-primary" />
                  <span>{text}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="py-24 lg:py-32 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-secondary/50 to-transparent"></div>
        
        <div className="container mx-auto px-4 sm:px-6 relative z-10">
          <div className="text-center mb-16">
            <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              Features
            </span>
            <h2 className="text-3xl lg:text-5xl font-display font-bold text-foreground mb-5">
              Why Choose SlideCraft?
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Everything you need to create professional presentations without the hassle.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6 lg:gap-8 max-w-6xl mx-auto">
            {features.map((feature, i) => (
              <div 
                key={i} 
                className="group relative bg-card rounded-3xl border border-border p-8 shadow-card hover-lift animate-slide-up"
                style={{ animationDelay: `${i * 100}ms` }}
              >
                {/* Gradient border on hover */}
                <div className="absolute inset-0 rounded-3xl gradient-primary opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
                
                <div className="relative">
                  <div className="w-14 h-14 rounded-2xl gradient-primary flex items-center justify-center mb-6 shadow-glow group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="h-7 w-7 text-primary-foreground" />
                  </div>
                  <h3 className="text-xl font-display font-bold text-foreground mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-24 lg:py-32">
        <div className="container mx-auto px-4 sm:px-6">
          <div className="relative max-w-5xl mx-auto rounded-[2.5rem] overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 gradient-hero"></div>
            <div className="absolute inset-0 noise"></div>
            
            {/* Decorative orbs */}
            <div className="absolute top-0 right-0 w-64 h-64 gradient-primary opacity-20 blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-accent opacity-15 blur-3xl"></div>
            
            {/* Content */}
            <div className="relative z-10 p-10 lg:p-16 text-center">
              <span className="inline-block px-4 py-1.5 rounded-full bg-primary-foreground/10 text-primary-foreground/80 text-sm font-medium mb-6 backdrop-blur-sm border border-primary-foreground/10">
                Start for free
              </span>
              
              <h2 className="text-3xl lg:text-5xl font-display font-bold text-primary-foreground mb-5 leading-tight">
                Ready to transform your ideas?
              </h2>
              <p className="text-primary-foreground/70 text-lg mb-10 max-w-xl mx-auto">
                Join thousands of professionals creating stunning presentations in seconds.
              </p>
              
              <Button 
                size="xl" 
                className="bg-accent text-accent-foreground hover:bg-accent/90 shadow-accent-glow font-bold"
                asChild
              >
                <Link to="/register">
                  Get Started Free
                  <ArrowRight className="h-5 w-5" />
                </Link>
              </Button>
              
              {/* Floating shapes */}
              <div className="absolute top-12 right-12 w-20 h-20 rounded-2xl gradient-accent opacity-25 animate-float hidden lg:block"></div>
              <div className="absolute bottom-16 left-16 w-14 h-14 rounded-xl gradient-primary opacity-30 animate-float-delayed hidden lg:block"></div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="py-10 border-t border-border">
        <div className="container mx-auto px-4 sm:px-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2.5">
              <div className="p-1.5 rounded-lg gradient-primary">
                <Presentation className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="font-display font-bold text-foreground">SlideCraft</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 SlideCraft AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
