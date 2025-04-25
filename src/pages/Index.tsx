
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Search, Database, CalendarCheck, Shield, Sparkles, Zap, Bot } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: "Search Results",
      description: "Query multiple Confluence pages with semantic search and QA-based answers",
      icon: Search,
      path: "/search",
      color: "bg-blue-500"
    },
    {
      title: "Data Generator",
      description: "Generate sample JSON/XML records using templates",
      icon: Database,
      path: "/generator",
      color: "bg-green-500"
    },
    {
      title: "Meeting Summarizer",
      description: "Convert meeting audio/text to summaries and update Confluence",
      icon: CalendarCheck,
      path: "/summarizer",
      color: "bg-purple-500"
    },
    {
      title: "NFR Assistant",
      description: "Capture and track Non-Functional Requirements with documentation",
      icon: Shield,
      path: "/nfr",
      color: "bg-orange-500"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-3xl -top-32 -left-32 animate-pulse" />
        <div className="absolute w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-3xl -bottom-32 -right-32 animate-pulse delay-700" />
      </div>

      {/* Neural Network Lines Animation */}
      <div className="absolute inset-0" style={{ background: `radial-gradient(circle at 50% 50%, rgba(66, 138, 255, 0.1) 0%, transparent 50%)` }}>
        {Array.from({ length: 20 }).map((_, i) => (
          <div
            key={i}
            className="absolute h-px w-32 bg-gradient-to-r from-transparent via-blue-500/50 to-transparent"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              transform: `rotate(${Math.random() * 360}deg)`,
              animation: `pulse 3s infinite ${Math.random() * 3}s`
            }}
          />
        ))}
      </div>

      <div className="container mx-auto px-4 py-16 relative z-10">
        {/* Hero Section */}
        <div className="text-center mb-16 space-y-6">
          {/* AI Icon */}
          <div className="flex justify-center mb-8">
            <div className="p-4 bg-blue-500/20 rounded-full animate-bounce">
              <Bot className="w-12 h-12 text-blue-400" />
            </div>
          </div>

          <h1 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 mb-6 animate-in fade-in slide-in-from-top duration-1000">
            tGPT Documentation Hub
          </h1>
          
          <div className="flex items-center justify-center gap-2 mb-8">
            <Sparkles className="w-5 h-5 text-yellow-400 animate-pulse" />
            <p className="text-xl text-gray-300 max-w-2xl animate-in fade-in slide-in-from-bottom duration-1000">
              Team Guidance and Productive Tool - Your AI-Powered Documentation Assistant
            </p>
            <Sparkles className="w-5 h-5 text-yellow-400 animate-pulse" />
          </div>

          {/* AI Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
            {[
              { label: "Pages Indexed", value: "10K+" },
              { label: "AI Models", value: "4+" },
              { label: "Processing Speed", value: "<1s" },
              { label: "Accuracy Rate", value: "98%" }
            ].map((stat, index) => (
              <div 
                key={stat.label}
                className="bg-gray-800/50 p-4 rounded-lg backdrop-blur-sm border border-gray-700/50"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div className="text-2xl font-bold text-blue-400">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <Card 
              key={feature.title}
              className="group bg-gray-800/50 border-gray-700 hover:bg-gray-800/70 transition-all duration-300
                       backdrop-blur-sm animate-in fade-in slide-in-from-bottom duration-1000 relative overflow-hidden"
              style={{ animationDelay: `${index * 200}ms` }}
            >
              {/* Hover Effect Background */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
              
              <Button
                variant="ghost"
                className="w-full h-full p-8 flex flex-col items-center text-left relative z-10"
                onClick={() => navigate(feature.path)}
              >
                <div className={`${feature.color} p-3 rounded-lg mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg shadow-${feature.color}/20`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-center">{feature.description}</p>
              </Button>
            </Card>
          ))}
        </div>

        {/* Footer with Glowing Effect */}
        <footer className="mt-16 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50">
            <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />
            <p className="text-gray-400">Version 1.0.0 | Powered by AI</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Index;
