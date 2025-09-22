import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

interface StarRatingProps {
  rating: number;
  maxRating?: number;
  size?: "sm" | "md" | "lg";
  showScore?: boolean;
}

export const StarRating = ({ 
  rating, 
  maxRating = 5, 
  size = "md", 
  showScore = true 
}: StarRatingProps) => {
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-6 h-6", 
    lg: "w-8 h-8"
  };

  const textSizeClasses = {
    sm: "text-sm",
    md: "text-base",
    lg: "text-xl"
  };

  const getSentimentColor = (score: number) => {
    if (score >= 4) return "text-sentiment-positive fill-sentiment-positive";
    if (score >= 3) return "text-sentiment-neutral fill-sentiment-neutral";
    return "text-sentiment-negative fill-sentiment-negative";
  };

  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center gap-1">
        {Array.from({ length: maxRating }, (_, index) => {
          const starNumber = index + 1;
          const isFilledStar = rating >= starNumber;
          const isHalfStar = rating >= starNumber - 0.5 && rating < starNumber;
          
          return (
            <div key={index} className="relative">
              <Star 
                className={cn(
                  sizeClasses[size],
                  "text-muted-foreground"
                )}
              />
              {(isFilledStar || isHalfStar) && (
                <Star 
                  className={cn(
                    sizeClasses[size],
                    "absolute top-0 left-0",
                    getSentimentColor(rating),
                    isHalfStar && "clip-half"
                  )}
                  style={isHalfStar ? { clipPath: 'inset(0 50% 0 0)' } : undefined}
                />
              )}
            </div>
          );
        })}
      </div>
      {showScore && (
        <span className={cn(
          textSizeClasses[size],
          "font-semibold",
          getSentimentColor(rating)
        )}>
          {rating.toFixed(1)}/5
        </span>
      )}
    </div>
  );
};