
import { useState } from "react";
import { Upload, FileAudio, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

const Summarizer = () => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const response = await fetch("/meeting/transcribe", {
        method: "POST",
        body: formData
      });

      if (!response.ok) throw new Error("Transcription failed");

      const data = await response.json();
      setText(data.text);

      toast({
        title: "Audio Transcribed",
        description: "Your audio has been successfully transcribed"
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to transcribe audio. Please try again."
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSummarize = async () => {
    setLoading(true);
    try {
      const response = await fetch("/meeting/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      if (!response.ok) throw new Error("Summarization failed");

      toast({
        title: "Text Summarized",
        description: "Your text has been successfully summarized"
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to summarize text. Please try again."
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
              Meeting Summarizer
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4">
              <div className="flex gap-4">
                <Button
                  component="label"
                  variant="outline"
                  className="flex-1"
                >
                  <FileAudio className="mr-2 h-4 w-4" />
                  Upload Audio
                  <input
                    type="file"
                    hidden
                    accept="audio/*"
                    onChange={handleFileUpload}
                  />
                </Button>
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => document.getElementById('file-text')?.click()}
                >
                  <FileText className="mr-2 h-4 w-4" />
                  Upload Text
                  <input
                    id="file-text"
                    type="file"
                    hidden
                    accept=".txt"
                    onChange={handleFileUpload}
                  />
                </Button>
              </div>
              <Textarea
                placeholder="Enter or paste your meeting text here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[200px] bg-white/5 border-gray-700 text-white"
              />
              <Button
                onClick={handleSummarize}
                disabled={loading || !text}
                className="w-full bg-purple-600 hover:bg-purple-700"
              >
                <Upload className="mr-2 h-4 w-4" />
                Summarize
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Summarizer;
