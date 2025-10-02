// frontend/components/ReviewAnalyzer.tsx

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { StarRating } from "./StarRating";
import { Loader2, MessageSquare, TrendingUp, AlertCircle } from "lucide-react";
import { toast } from "@/hooks/use-toast";

const apiUrl = import.meta.env.VITE_API_URL;


interface AnalysisResult {
  score: number;
  sentiment: "positive" | "negative" | "neutral";
  issues: string[];
  response: string;
}

export const ReviewAnalyzer = () => {
  const [reviewText, setReviewText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const analyzeReview = async () => {
    if (!reviewText.trim()) {
      toast({
        title: "Please enter a review",
        description: "Enter some text to analyze the sentiment.",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ review: reviewText }),
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const data = await response.json();
      setResult({
        score: data.score,
        sentiment: data.sentiment,
        issues: data.issues ?? [],
        response: data.response ?? "",
      });

      toast({
        title: "Analysis Complete",
        description: `Sentiment: ${data.sentiment}`,
      });
    } catch (error) {
      console.error(error);
      toast({
        title: "Analysis Failed",
        description: "Unable to connect to sentiment analysis API. Make sure the backend is running.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-3">
          <MessageSquare className="w-10 h-10 text-primary" />
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-hotel-gold bg-clip-text text-transparent">
            Hotel Review Sentiment Analyzer
          </h1>
        </div>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Analyze the sentiment of hotel reviews using advanced AI. Get instant ratings and insights.
        </p>
      </div>

      {/* Input Section */}
      <Card className="shadow-lg border-0 bg-gradient-to-br from-card to-secondary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-primary" />
            Review Analysis
          </CardTitle>
          <CardDescription>
            Paste a hotel review below to analyze its sentiment and get a positivity rating
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <Textarea
            placeholder="Enter hotel review text..."
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            className="min-h-32 resize-none border-2 focus:border-primary/50 bg-background"
          />
          <Button
            onClick={analyzeReview}
            disabled={isAnalyzing || !reviewText.trim()}
            className="w-full bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-white font-semibold py-3 shadow-lg"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing Sentiment...
              </>
            ) : (
              <>
                <TrendingUp className="w-5 h-5 mr-2" />
                Analyze Review
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <Card className="shadow-xl border-2 border-primary/20 bg-gradient-to-br from-card via-card to-primary/5">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-2xl">
              <AlertCircle className="w-7 h-7 text-hotel-gold" />
              Sentiment Analysis Results
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Rating */}
            <div className="p-6 bg-gradient-to-r from-secondary/30 to-hotel-gold/20 rounded-lg border">
              <h3 className="text-lg font-semibold mb-2">Overall Rating</h3>
              <StarRating rating={result.score} size="lg" />
            </div>

            {/* Sentiment & Issues */}
            <div className="p-6 bg-gradient-to-r from-background to-muted/50 rounded-lg border">
              <h3 className="text-lg font-semibold mb-3">Analysis Summary</h3>
              <p className="text-muted-foreground leading-relaxed mb-2">{result.response}</p>
              {result.issues.length > 0 && (
                <ul className="list-disc list-inside text-sm text-foreground">
                  {result.issues.map((issue) => (
                    <li key={issue}>{issue}</li>
                  ))}
                </ul>
              )}
              <div className="mt-4 flex items-center gap-4 text-sm">
                <div className={`px-3 py-1 rounded-full font-medium ${
                  result.sentiment === "positive" ? "bg-sentiment-positive/10 text-sentiment-positive border border-sentiment-positive/20" :
                  result.sentiment === "negative" ? "bg-sentiment-negative/10 text-sentiment-negative border border-sentiment-negative/20" :
                  "bg-sentiment-neutral/10 text-sentiment-neutral border border-sentiment-neutral/20"
                }`}>
                  {result.sentiment.charAt(0).toUpperCase() + result.sentiment.slice(1)} Sentiment
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
