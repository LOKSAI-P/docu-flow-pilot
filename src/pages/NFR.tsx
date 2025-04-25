
import { useState } from "react";
import { FileCheck, Download, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

const NFR = () => {
  const [projectName, setProjectName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await fetch("/nfr/generate-doc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_name: projectName,
          project_description: description,
          requirements: {}
        })
      });

      if (!response.ok) throw new Error("Document generation failed");

      toast({
        title: "Document Generated",
        description: "NFR document has been generated successfully"
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to generate document. Please try again."
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
              NFR Assistant
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <Input
                placeholder="Project Name"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="bg-white/5 border-gray-700 text-white"
              />
              <Textarea
                placeholder="Project Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="min-h-[150px] bg-white/5 border-gray-700 text-white"
              />
              <div className="flex gap-4">
                <Button
                  onClick={handleSubmit}
                  disabled={loading || !projectName || !description}
                  className="flex-1 bg-orange-600 hover:bg-orange-700"
                >
                  <FileCheck className="mr-2 h-4 w-4" />
                  Generate Document
                </Button>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <Button variant="outline" className="w-full">
                  <Download className="mr-2 h-4 w-4" />
                  Export to PDF
                </Button>
                <Button variant="outline" className="w-full">
                  <Upload className="mr-2 h-4 w-4" />
                  Upload to Confluence
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default NFR;
