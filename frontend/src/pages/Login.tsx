import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Loader2, Presentation, ArrowRight, Sparkles } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left side - Hero */}
      <div className="hidden lg:flex lg:w-1/2 gradient-hero relative overflow-hidden">
        {/* Noise overlay */}
        <div className="absolute inset-0 noise"></div>
        
        {/* Grid pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(hsl(0_0%_100%/0.03)_1px,transparent_1px),linear-gradient(90deg,hsl(0_0%_100%/0.03)_1px,transparent_1px)] bg-[size:64px_64px]"></div>
        
        {/* Animated orbs */}
        <div className="absolute top-20 right-20 w-40 h-40 rounded-full gradient-primary opacity-20 blur-2xl animate-float"></div>
        <div className="absolute bottom-32 left-20 w-32 h-32 rounded-full bg-accent opacity-15 blur-2xl animate-float-delayed"></div>
        <div className="absolute top-1/2 right-32 w-24 h-24 rounded-2xl gradient-accent opacity-20 animate-pulse-glow"></div>
        
        <div className="relative z-10 flex flex-col justify-center px-12 xl:px-20">
          <div className="flex items-center gap-3 mb-10">
            <div className="relative">
              <div className="absolute inset-0 gradient-primary rounded-xl blur-lg opacity-60"></div>
              <div className="relative p-3 rounded-xl gradient-primary shadow-glow">
                <Presentation className="h-8 w-8 text-primary-foreground" />
              </div>
            </div>
            <span className="text-2xl font-display font-bold text-primary-foreground">SlideCraft</span>
          </div>
          
          <h1 className="text-4xl xl:text-5xl font-display font-bold text-primary-foreground mb-6 leading-tight">
            Create stunning presentations in seconds
          </h1>
          
          <p className="text-lg text-primary-foreground/70 mb-10 max-w-md leading-relaxed">
            Transform your ideas into professional PowerPoint presentations with the power of AI.
          </p>
          
          <div className="flex flex-col gap-4">
            {['AI-powered slide generation', 'Multiple design styles', 'Instant download'].map((feature, i) => (
              <div key={i} className="flex items-center gap-3 text-primary-foreground/80" style={{ animationDelay: `${i * 100}ms` }}>
                <div className="h-2 w-2 rounded-full bg-accent"></div>
                <span className="font-medium">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Right side - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-8 bg-background relative">
        <div className="absolute inset-0 gradient-mesh opacity-50"></div>
        
        <div className="w-full max-w-md relative z-10 animate-scale-in">
          {/* Mobile logo */}
          <div className="flex lg:hidden items-center gap-3 mb-10 justify-center">
            <div className="p-2.5 rounded-xl gradient-primary shadow-glow">
              <Presentation className="h-6 w-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-display font-bold text-foreground">SlideCraft</span>
          </div>
          
          <div className="text-center mb-8">
            <h2 className="text-3xl font-display font-bold text-foreground mb-2">Welcome back</h2>
            <p className="text-muted-foreground">Sign in to continue creating amazing presentations</p>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-sm animate-slide-up flex items-center gap-3">
                <div className="h-2 w-2 rounded-full bg-destructive"></div>
                {error}
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="email" className="text-foreground font-medium">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                className="h-12"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground font-medium">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                className="h-12"
              />
            </div>
            
            <Button 
              type="submit" 
              variant="hero" 
              size="lg" 
              className="w-full h-12"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="animate-spin" />
                  Signing in...
                </>
              ) : (
                <>
                  Sign in
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </form>
          
          <div className="mt-8 text-center">
            <p className="text-muted-foreground">
              Don't have an account?{' '}
              <Link to="/register" className="text-primary font-semibold hover:underline">
                Create one free
              </Link>
            </p>
          </div>
          
          {/* Decorative badge */}
          <div className="mt-10 flex justify-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-secondary/50 text-xs text-muted-foreground">
              <Sparkles className="h-3.5 w-3.5 text-primary" />
              <span>Trusted by 10,000+ professionals</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
