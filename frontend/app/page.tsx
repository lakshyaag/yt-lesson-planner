"use client";
import SearchForm from "@/components/search-form";
import LessonPlanDisplay from "@/components/lesson-plan";
import { useLoadingStore } from "@/store/useLoadingStore";
import { Skeleton } from "@/components/ui/skeleton";

export default function Home() {
  const loading = useLoadingStore((state) => state.loading);

  return (
    <div>
      <main className="flex flex-col items-center justify-center py-8">
        <h1 className="text-4xl font-bold">Welcome to YT Lesson Planner</h1>
        <p className="mt-4 text-lg text-gray-700">
          Generate comprehensive lesson plans from YouTube videos based on your
          queries.
        </p>
        <div className="mt-8 w-full max-w-md">
          <SearchForm />
        </div>
        {loading ? (
          <div className="flex flex-col space-y-3 mt-4">
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
