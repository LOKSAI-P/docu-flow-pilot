
import { useState } from "react";
import { FileJson, FileCode } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

const Generator = () => {
  const [template, setTemplate] = useState("");
  const [count, setCount] = useState(1);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch("/generator/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          template_id: "custom",
          template_content: template,
          count
        })
      });

      if (!response.ok) throw new Error("Generation failed");

      toast({
        title: "Data Generated",
        description: "Sample data has been generated successfully"
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to generate data. Please check your template."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <Card className="bg-white/10 backdrop-blur-lg border-gray-800">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-white">
              Sample Data Generator
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <Textarea
                placeholder="Enter your JSON/XML template..."
                value={template}
                onChange={(e) => setTemplate(e.target.value)}
                className="min-h-[200px] bg-white/5 border-gray-700 text-white"
              />
              <div className="flex gap-4">
                <Button
                  onClick={() => setTemplate(JSON.stringify({ name: "$name", email: "$email", age: "$number" }, null, 2))}
                  variant="outline"
                  className="flex-1"
                >
                  <FileJson className="mr-2 h-4 w-4" />
                  Load JSON Template
                </Button>
                <Button
                  onClick={() => setTemplate('<?xml version="1.0"?>\n<user>\n  <name>$name</name>\n  <email>$email</email>\n  <age>$number</age>\n</user>')}
                  variant="outline"
                  className="flex-1"
                >
                  <FileCode className="mr-2 h-4 w-4" />
                  Load XML Template
                </Button>
              </div>
              <Button 
                onClick={handleGenerate}
                disabled={loading || !template}
                className="w-full bg-green-600 hover:bg-green-700"
              >
                Generate Sample Data
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Generator;
