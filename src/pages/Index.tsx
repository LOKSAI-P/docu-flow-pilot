
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Search, Database, CalendarCheck, Shield } from "lucide-react";
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 animate-in fade-in slide-in-from-top duration-1000">
            tGPT Documentation Hub
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom duration-1000">
            Team Guidance and Productive Tool - Your centralized hub for managing documentation and workflows
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <Card 
              key={feature.title}
              className="group bg-gray-800/50 border-gray-700 hover:bg-gray-800/70 transition-all duration-300
                       backdrop-blur-sm animate-in fade-in slide-in-from-bottom duration-1000"
              style={{ animationDelay: `${index * 200}ms` }}
            >
              <Button
                variant="ghost"
                className="w-full h-full p-8 flex flex-col items-center text-left"
                onClick={() => navigate(feature.path)}
              >
                <div className={`${feature.color} p-3 rounded-lg mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-center">{feature.description}</p>
              </Button>
            </Card>
          ))}
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-400">
          <p>Version 1.0.0 | Powered by AI</p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
