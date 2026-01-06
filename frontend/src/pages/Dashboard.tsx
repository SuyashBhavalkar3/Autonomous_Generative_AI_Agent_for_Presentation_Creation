import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { 
  Presentation, 
  LogOut, 
  Sparkles, 
  Download, 
  Loader2,
  FileText,
  Palette,
  Layers,
  CheckCircle2,
  AlertCircle,
  Wand2,
  RefreshCw
} from 'lucide-react';

interface GeneratedPPT {
  id: string;
  topic: string;
  slides: number;
  style: string;
  createdAt: Date;
}

export default function Dashboard() {
  const { user, logout, getAuthHeader } = useAuth();
  const [topic, setTopic] = useState('');
  const [slideCount, setSlideCount] = useState('8');
  const [style, setStyle] = useState('professional');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPPT, setGeneratedPPT] = useState<GeneratedPPT | null>(null);
  const [error, setError] = useState('');
  const [isDownloading, setIsDownloading] = useState(false);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setGeneratedPPT(null);
    
    if (!topic.trim()) {
      setError('Please enter a topic for your presentation');
      return;
    }
    
    setIsGenerating(true);

    try {
      const API_BASE = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';

      const headers = { 'Content-Type': 'application/json', ...getAuthHeader() };

      const res = await fetch(`${API_BASE}/generate_ppt`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ prompt: topic.trim(), num_slides: parseInt(slideCount) }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error((errData && (errData.detail || errData.message)) || 'Generate failed');
      }

      const blob = await res.blob();
      // Try to extract filename from response headers
      let filename = `${topic.trim().replace(/\s+/g, '_')}.pptx`;
      const cd = res.headers.get('content-disposition');
      if (cd) {
        const match = cd.match(/filename\*=UTF-8''(.+)|filename="?([^";]+)"?/);
        if (match) {
          filename = decodeURIComponent(match[1] || match[2]);
        }
      }

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      const ppt: GeneratedPPT = {
        id: `ppt_${Date.now()}`,
        topic: topic.trim(),
        slides: parseInt(slideCount),
        style,
        createdAt: new Date(),
      };
      setGeneratedPPT(ppt);
      // Heuristic: if returned file is very small, images likely missing — retry via form POST
      if (blob.size && blob.size < 50_000) {
        // build form and post to backend with token as query param to trigger full server download
        try {
          const API_BASE = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
          const token = (getAuthHeader() as any).Authorization?.replace('Bearer ', '') || '';
          if (token) {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `${API_BASE}/generate_ppt?access_token=${encodeURIComponent(token)}`;
            form.style.display = 'none';

            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'payload';
            input.value = JSON.stringify({ prompt: topic.trim(), num_slides: parseInt(slideCount) });
            form.appendChild(input);

            document.body.appendChild(form);
            form.submit();
            form.remove();
          }
        } catch (e) {
          // ignore fallback errors
        }
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to generate presentation. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = async () => {
    if (!generatedPPT) return;
    
    setIsDownloading(true);
    
    // Simulate download
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // In a real app, this would trigger actual file download
    const fileName = `${generatedPPT.topic.replace(/\s+/g, '_')}_presentation.pptx`;
    console.log(`Downloading: ${fileName}`);
    
    setIsDownloading(false);
  };

  const styles = [
    { value: 'professional', label: 'Professional', description: 'Clean & corporate' },
    { value: 'creative', label: 'Creative', description: 'Bold & artistic' },
    { value: 'minimal', label: 'Minimal', description: 'Simple & elegant' },
    { value: 'modern', label: 'Modern', description: 'Trendy & fresh' },
    { value: 'academic', label: 'Academic', description: 'Formal & structured' },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border glass sticky top-0 z-50">
        <div className="container mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl gradient-primary shadow-glow">
              <Presentation className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-lg font-display font-bold text-foreground">SlideCraft</span>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/50 text-sm">
              <div className="h-2 w-2 rounded-full bg-primary animate-pulse"></div>
              <span className="text-muted-foreground">
                Hey, <span className="text-foreground font-medium">{user?.name}</span>
              </span>
            </div>
            <Button variant="ghost" size="sm" onClick={logout} className="gap-2">
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="container mx-auto px-4 sm:px-6 py-8 lg:py-12">
        <div className="max-w-4xl mx-auto">
          {/* Title */}
          <div className="text-center mb-10 animate-fade-in">
            <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              <Wand2 className="h-3.5 w-3.5 inline-block mr-1.5" />
              AI-Powered
            </span>
            <h1 className="text-3xl lg:text-4xl font-display font-bold text-foreground mb-3">
              Create Your Presentation
            </h1>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto">
              Describe your topic and let AI craft stunning slides for you
            </p>
          </div>
          
          {/* Generator Card */}
          <div className="bg-card rounded-3xl border border-border shadow-card p-6 lg:p-8 animate-slide-up relative overflow-hidden">
            {/* Decorative gradient */}
            <div className="absolute top-0 right-0 w-64 h-64 gradient-primary opacity-5 blur-3xl"></div>
            
            <form onSubmit={handleGenerate} className="space-y-6 relative z-10">
              {error && (
                <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-sm flex items-center gap-3 animate-slide-up">
                  <AlertCircle className="h-5 w-5 flex-shrink-0" />
                  {error}
                </div>
              )}
              
              {/* Topic Input */}
              <div className="space-y-3">
                <Label htmlFor="topic" className="text-foreground font-semibold flex items-center gap-2 text-base">
                  <div className="p-1.5 rounded-lg bg-primary/10">
                    <FileText className="h-4 w-4 text-primary" />
                  </div>
                  Presentation Topic
                </Label>
                <Textarea
                  id="topic"
                  placeholder="e.g., The Future of Renewable Energy: Trends and Innovations in 2024"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="min-h-[120px] resize-none text-base rounded-xl"
                  disabled={isGenerating}
                />
                <p className="text-xs text-muted-foreground">
                  Be specific about your topic for better results
                </p>
              </div>
              
              {/* Options Row */}
              <div className="grid sm:grid-cols-2 gap-6">
                {/* Slide Count */}
                <div className="space-y-3">
                  <Label htmlFor="slides" className="text-foreground font-semibold flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-primary/10">
                      <Layers className="h-4 w-4 text-primary" />
                    </div>
                    Number of Slides
                  </Label>
                  <Select value={slideCount} onValueChange={setSlideCount} disabled={isGenerating}>
                    <SelectTrigger className="h-12 rounded-xl">
                      <SelectValue placeholder="Select slides" />
                    </SelectTrigger>
                    <SelectContent>
                      {[5, 8, 10, 12, 15, 20].map((num) => (
                        <SelectItem key={num} value={num.toString()}>
                          {num} slides
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                {/* Style */}
                <div className="space-y-3">
                  <Label htmlFor="style" className="text-foreground font-semibold flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-primary/10">
                      <Palette className="h-4 w-4 text-primary" />
                    </div>
                    Design Style
                  </Label>
                  <Select value={style} onValueChange={setStyle} disabled={isGenerating}>
                    <SelectTrigger className="h-12 rounded-xl">
                      <SelectValue placeholder="Select style" />
                    </SelectTrigger>
                    <SelectContent>
                      {styles.map((s) => (
                        <SelectItem key={s.value} value={s.value}>
                          <div className="flex items-center gap-2">
                            <span className="font-medium">{s.label}</span>
                            <span className="text-muted-foreground text-xs">— {s.description}</span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              {/* Generate Button */}
              <Button 
                type="submit" 
                variant="hero" 
                size="xl" 
                className="w-full h-14"
                disabled={isGenerating}
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="animate-spin h-5 w-5" />
                    Generating your presentation...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5" />
                    Generate Presentation
                  </>
                )}
              </Button>
            </form>
            
            {/* Loading State */}
            {isGenerating && (
              <div className="mt-10 pt-8 border-t border-border">
                <div className="flex flex-col items-center gap-5 py-8">
                  <div className="relative">
                    <div className="w-20 h-20 rounded-2xl gradient-primary opacity-20 animate-ping absolute inset-0"></div>
                    <div className="w-20 h-20 rounded-2xl gradient-primary flex items-center justify-center relative shadow-glow">
                      <Sparkles className="h-10 w-10 text-primary-foreground animate-bounce-subtle" />
                    </div>
                  </div>
                  <div className="text-center">
                    <p className="text-foreground font-semibold text-lg mb-1">AI is crafting your slides</p>
                    <p className="text-sm text-muted-foreground">This usually takes about 15-30 seconds</p>
                  </div>
                  <div className="w-72 h-2.5 bg-secondary rounded-full overflow-hidden">
                    <div className="h-full gradient-primary animate-shimmer rounded-full"></div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Success State */}
            {generatedPPT && !isGenerating && (
              <div className="mt-10 pt-8 border-t border-border animate-slide-up">
                <div className="bg-primary/5 border border-primary/20 rounded-2xl p-6 lg:p-8">
                  <div className="flex flex-col sm:flex-row items-start gap-5">
                    <div className="p-4 rounded-2xl gradient-primary shadow-glow flex-shrink-0">
                      <CheckCircle2 className="h-8 w-8 text-primary-foreground" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-display font-bold text-foreground mb-2">
                        Presentation Ready! 🎉
                      </h3>
                      <p className="text-muted-foreground mb-6">
                        Your <span className="text-foreground font-medium">{generatedPPT.slides}-slide {generatedPPT.style}</span> presentation about <span className="text-foreground font-medium">"{generatedPPT.topic}"</span> is ready.
                      </p>
                      
                      <div className="flex flex-wrap gap-3">
                        <Button 
                          variant="gradient-accent" 
                          size="lg" 
                          onClick={handleDownload}
                          disabled={isDownloading}
                          className="gap-2 h-12"
                        >
                          {isDownloading ? (
                            <>
                              <Loader2 className="animate-spin h-5 w-5" />
                              Preparing...
                            </>
                          ) : (
                            <>
                              <Download className="h-5 w-5" />
                              Download PowerPoint
                            </>
                          )}
                        </Button>
                        
                        <Button 
                          variant="outline" 
                          size="lg"
                          onClick={() => {
                            setGeneratedPPT(null);
                            setTopic('');
                          }}
                          className="gap-2 h-12"
                        >
                          <RefreshCw className="h-4 w-4" />
                          Create Another
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Tips */}
          <div className="mt-8 grid sm:grid-cols-3 gap-4 animate-fade-in" style={{ animationDelay: '200ms' }}>
            {[
              { icon: FileText, title: 'Be Specific', desc: 'Add context and key points to your topic' },
              { icon: Layers, title: 'Right Length', desc: '8-12 slides work best for most topics' },
              { icon: Palette, title: 'Match Style', desc: 'Choose a style that fits your audience' },
            ].map((tip, i) => (
              <div key={i} className="p-5 rounded-2xl bg-card border border-border hover-lift group">
                <div className="p-2 rounded-xl bg-primary/10 w-fit mb-3 group-hover:scale-110 transition-transform duration-300">
                  <tip.icon className="h-5 w-5 text-primary" />
                </div>
                <h4 className="font-semibold text-foreground mb-1">{tip.title}</h4>
                <p className="text-sm text-muted-foreground">{tip.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
