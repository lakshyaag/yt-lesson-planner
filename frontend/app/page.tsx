"use client";
import SearchForm from "@/components/search-form";
import LessonPlanDisplay from "@/components/lesson-plan";
import { useLoadingStore } from "@/store/useLoadingStore";
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect, useState } from "react";
import { Progress } from "@/components/ui/progress";

export default function Home() {
  const loading = useLoadingStore((state) => state.loading);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setProgress((prev: number) => (prev >= 95 ? 5 : prev + 5));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [loading]);

  return (
    <div>
      <main className="flex flex-col items-center justify-center py-8">
        <h1 className="text-4xl font-bold text-center ">Welcome to YouNiversity!</h1>
        <p className="mt-4 text-lg text-center">
          Create detailed lesson plans from YouTube content tailored to your search queries with ease.
        </p>
        <div className="mt-8 w-full max-w-md">
          <SearchForm />
        </div>
        {loading ? (
          <div className="flex flex-col space-y-3 mt-4">
            <Progress value={progress} />
            <Skeleton className="h-[225px] w-[350px] rounded-xl" />
            <div className="space-y-2">
              <Skeleton className="h-4 w-[250px]" />
              <Skeleton className="h-4 w-[200px]" />
            </div>
          </div>
        ) : (
          <LessonPlanDisplay />
        )}
      </main>
    </div>
  );
}
