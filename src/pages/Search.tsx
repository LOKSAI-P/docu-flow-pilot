
import { useState } from "react";
import { Search as SearchIcon } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

const Search = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch("/search/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          top_k: 5,
          base_url: process.env.CONFLUENCE_URL,
          space_key: process.env.CONFLUENCE_SPACE_KEY,
          auth_token: process.env.CONFLUENCE_AUTH_TOKEN
        })
      });

      if (!response.ok) throw new Error("Search failed");

      toast({
        title: "Search completed",
        description: "Results have been fetched successfully"
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to perform search. Please try again."
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
              Semantic Search Assistant
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-4">
              <Input
                placeholder="Enter your search query..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 bg-white/5 border-gray-700 text-white"
              />
              <Button 
                onClick={handleSearch} 
                disabled={loading || !query}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <SearchIcon className="mr-2 h-4 w-4" />
                Search
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results section will be added here in future updates */}
        <div className="grid gap-4">
          {/* Placeholder for search results */}
          <Card className="bg-white/5 backdrop-blur-sm border-gray-800">
            <CardContent className="p-6">
              <p className="text-gray-400">
                Enter a search query above to see semantic search results
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Search;
